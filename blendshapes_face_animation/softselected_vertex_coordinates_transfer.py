import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.cmds as cmds
import maya.mel as mel
import timeit
import sys


compOpacities = {} # Dict of Soft Selected verts and their weight on base model
vertListCompOKeys = [] # List of Soft Selected verts
baseVertDict = {} # Dict of Soft Selected verts and their coords on base model
targetVertDict = {} # Dict of verts(same as Soft Selected) and their coords on target model


# Instruction
print '''\n----------------------MANUAL---------------------
1) Select verts with Soft Selection on base model
2) Click SAVE
3) Choose object for transformation
4) Click LOAD 
-------------------------------------------------\n'''

# Create UI
def createUI( pWindowTitle ):
    
    windowID = 'myWindowID'
    
    # Check UI window qnty 
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )
    
    # UI window structure    
    cmds.window( windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True, w=250 )
    form = cmds.formLayout()
    t = cmds.text( l='Choose area to SAVE verts' )
    t2 = cmds.text( l='and then object to LOAD' )
    cmds.formLayout( form, edit=True, attachForm=[(t, 'top', 10), (t, 'right', 10), (t, 'left', 10), 
                                                  (t2, 'top', 25), (t2, 'right', 10), (t2, 'left', 10)])  

    cmds.rowColumnLayout( numberOfColumns=3, 
                          columnWidth=[ (1,100), (2,10), (3,100) ],
                          columnOffset=[ (1, 'left', 50), (3, 'right', 20) ] )

    cmds.separator( h=50, style='none' )
    cmds.separator( h=50, style='none' )
    cmds.separator( h=50, style='none' )
               
    cmds.button( label='   SAVE   ', command=SaveVert )
    cmds.separator( h=10, style='none' )
    cmds.button( label='  LOAD  ', command=LoadVert )
    cmds.separator( h=10, style='none' )
    cmds.showWindow()

# Check qnty of selected objects
def object_qnty_check(object):
    if len(object) > 1:
        print "More than one object is selected"
        return sys.exit()
    if len(object) == 0:
        print "Object isn't selected"
        return sys.exit()

# Save Soft Selected verts, their weight and coords
def SaveVert(*Args):
    global compOpacities
    compOpacities.clear()
    global vertListCompOKeys
    global baseVertDict
    baseVertDict.clear()
    targetVertDict.clear()
    
        
    # Get dict with Soft Selected verts and their weight
    opacityMult = 1.0
    # If soft select isn't on, return
    if not cmds.softSelect(q=True, sse=True):
        print "Soft Selection is turned off"
        return sys.exit()
    richSel = OpenMaya.MRichSelection()
    try:
        # get currently active soft selection
        OpenMaya.MGlobal.getRichSelection(richSel)
    except RuntimeError:
        print "Verts are not selected"
        sys.exit()
    richSelList = OpenMaya.MSelectionList()
    richSel.getSelection(richSelList)
    selCount = richSelList.length()
    for x in xrange(selCount):
        shapeDag = OpenMaya.MDagPath()
        shapeComp = OpenMaya.MObject()
        try:
            richSelList.getDagPath(x, shapeDag, shapeComp)
        except RuntimeError:
	    	# nodes like multiplyDivides will error
            continue
		
        compFn = OpenMaya.MFnSingleIndexedComponent(shapeComp)
        try:
            # get the secret hidden opacity value for each component (vert, cv, etc)
            for i in xrange(compFn.elementCount()):
                weight = compFn.weight(i)
                compOpacities[compFn.element(i)] = weight.influence() * opacityMult
        except Exception, e:
            print e.__str__()
            print 'Soft selection appears invalid, skipping for shape "%s".' % shapeDag.partialPathName()
    
    # List of Soft Selected verts
    vertListCompOKeys = compOpacities.keys()
    
    # Selecting whole object 
    name = cmds.ls(sl=True)
    main_name = name[0].split('.')
    cmds.select(main_name[0])

    # Get dict of Soft Selected verts and their coord    
    headObj = cmds.ls(sl=True)
    for head in headObj:
        for vert in vertListCompOKeys:
            head_vert = head + '.vtx[' + str(vert) + ']'
            vertCoord = cmds.xform(head_vert, q=True, t=True)
            baseVertDict[vert] = vertCoord
    
    return compOpacities, vertListCompOKeys, baseVertDict

# Soft transformation of Soft Selected vetrs from base model to target model
def LoadVert(*Args):
    global vertListCompOKeys
    start_time = timeit.default_timer()
      
    # Get dict of verts (same as Soft Selected) and their coord on target model
    headObj = cmds.ls(sl=True)
    for head in headObj:
        for vert in vertListCompOKeys:
            head_vert = head + '.vtx[' + str(vert) + ']'
            vertCoord = cmds.xform(head_vert, q = True, t = True)
            targetVertDict[vert] = vertCoord
    
    # Dict of verts and coords for "Soft" transformation ( considering weight of Soft Selection) 
    SoftvertDict = {}
    for key in compOpacities:
        weight = compOpacities.get(key)
        x = (baseVertDict[key][0] - targetVertDict[key][0]) * weight + targetVertDict[key][0]
        y = (baseVertDict[key][1] - targetVertDict[key][1]) * weight + targetVertDict[key][1]
        z = (baseVertDict[key][2] - targetVertDict[key][2]) * weight + targetVertDict[key][2]
        SoftvertDict[key] = [x, y, z]
    print "SoftverDict creation time - ", (timeit.default_timer() - start_time)

    # Transformation function           
    def vertTransfer():
        start_time = timeit.default_timer()
        headObj = cmds.ls(sl = True)
        targetVertDict = {}
        object_qnty_check(headObj)
        if len(headObj) == 1:
           for head in headObj:
               for i in SoftvertDict:
                    targetVertDict[head+'.vtx[' + str(i) + ']'] = SoftvertDict[i]
        
        for head in headObj:
           for vert, value in targetVertDict.iteritems():
               cmds.xform(vert, t=value)
        print "Transformation time - ", (timeit.default_timer() - start_time)
        print "Loaded"
        
    vertTransfer()

# Start UI-script
createUI( 'Transformation' )
    