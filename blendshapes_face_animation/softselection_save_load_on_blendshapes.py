# SoftSelected Delta Save-Load.py

import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.cmds as cmds
import timeit
import sys
import pickle
import copy
import os
from functools import partial
import datetime
import time


print '''\n-------------------------------------------MANUAL------------------------------------------
1) DO IT : If SoftSelection is ON  - choose verts, click DO IT and choose folder with Delta
           If SoftSelection is OFF - choose file to load SoftSelection
2) SAVE - Enter name for SoftSelection file, which will be saved in directory with Delta
-------------------------------------------------------------------------------------------\n'''


compOpacities = {} # Dict of Soft Selected verts and their weight on base model
vertListCompOKeys = [] # List of Soft Selected verts
baseVertDict = {} # Dict of Soft Selected verts and their coords on base model
targetVertDict = {} # Dict of verts(same as Soft Selected) and their coords on target model
adress = ""


#----------------------------------------------------------------------------------------------------------------------
# Check qnty of slected objects
def object_qnty_check(object):
    if len(object) > 1:
        print "More than one object is selected"
        return sys.exit()
    if len(object) == 0:
        print "Object isn't selected"
        return sys.exit()
        
#----------------------------------------------------------------------------------------------------------------------
# Set all BlendShape attributes to 0 
def set_BS_to_0():
    names = cmds.listAttr( "blendShape1", m=True, k=True )[1:] # List of blendshape attributes (without envelope)
    keyAttr = []
    nullAttr = ()
    for k in range( len(names) ):
        nullAttr = ( k, 0 )
        keyAttr.append( nullAttr )
    cmds.blendShape( 'blendShape1', edit=True, w=keyAttr )
   
  
#----------------------------------------------------------------------------------------------------------------------
# Create dialog window
def createUI( pWindowTitle ):
    
    windowID = 'myWindowID'
    
    # Check UI window qnty 
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )
    
    # UI window structure    
    cmds.window( windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True, w=244 )
    form = cmds.formLayout()
    t = cmds.text( l='    Read MANUAL in history window, please.')
    cmds.formLayout( form, edit=True, attachForm=[(t, 'top', 10), (t, 'right', 10), (t, 'left', 0)])  

    cmds.rowColumnLayout( numberOfColumns=3, 
                          columnWidth=[ (1,100), (2,30), (3,100) ],
                          columnOffset=[ (1, 'left', 20), (2, 'left', 10), (3, 'right', 10) ] )

    cmds.separator( h=35, style='none' )
    cmds.separator( h=35, style='none' )
    cmds.separator( h=35, style='none' )
               
    cmds.button( label='      DO IT       ', command=do_it)
    cmds.separator( h=30, style='none' )
    cmds.button( label='       SAVE       ', command=SaveSoftSelection)
    cmds.separator( h=10, style='none' )
    cmds.showWindow()

#----------------------------------------------------------------------------------------------------------------------

def LoadDelta(Args):

    global adress    
    # Open dialog window to choose directory to load delta        
    folder = cmds.fileDialog2( cap='Choose directory to load Delta', fm=3, dialogStyle=1 )
    adress = folder[0]+"\\"
    pathList_cleared = []    
    targetBlendDict = {}
    named_targetBlendDict = {}
    print "Loading Delta :)"
    # Getting .bsp files from choosen folder
    pathList = os.listdir( adress )
    if len(pathList) == 0:
        print "Folder is empty"
    for element in pathList:
        if '.bsp' in element:
            pathList_cleared.append( element )
        else:
            print 'wrong type - ', element
    pathList = pathList_cleared
    
    headObj = cmds.ls( sl=True )
    object_qnty_check(headObj)
    headObject = headObj[0]
    
    step = 25
    for i in range( len(pathList) ):
        start_time = timeit.default_timer()
        named_targetBlendDict.clear()
        path_name = open( adress+pathList[i],'r' )
        DeltaDict = pickle.load( path_name )
        targetBlendDict.clear()
        new_name = pathList[i].split('.')[0]
        cmds.duplicate( headObj[0], n=headObject+'_' + new_name )
        cmds.select( headObject+'_'+new_name )
        cmds.move( step, 0, 0 )
        step += 25
        for key in compOpacities:
            weight = compOpacities.get(key)
            x =  baseVertDict[key][0] + (DeltaDict[key][0] * weight)
            y =  baseVertDict[key][1] + (DeltaDict[key][1] * weight)
            z =  baseVertDict[key][2] + (DeltaDict[key][2] * weight)
            targetBlendDict[key] = [x, y, z]
        copy_headObj = cmds.ls( sl=True )
        for head in copy_headObj:
            for i in targetBlendDict:
                 named_targetBlendDict[head+'.vtx' + str(i)] = targetBlendDict[i]
        for head in copy_headObj:
           for vert, value in named_targetBlendDict.iteritems():
               cmds.xform( vert, t=value )
        print "Loading time - ", head, ( timeit.default_timer() - start_time )
    cmds.softSelect( sse=1 )
    names = cmds.listAttr( "blendShape1", m=True, k=True )[1:]
    fullNames = []
    for i in names:
    	fullNames.append( headObj[0] + '_' + i )
    cmds.blendShape( fullNames, headObj )
    cmds.delete( fullNames )

    return adress
    
#----------------------------------------------------------------------------------------------------------------------

def SaveSoftSelected(*Args):
    global compOpacities
    compOpacities.clear()
    global vertListCompOKeys
    global baseVertDict
    baseVertDict.clear()
    targetVertDict.clear()
    set_BS_to_0()    
    # Get dict with Soft Selected verts and their weight
    opacityMult = 1.0
    if cmds.softSelect(q=True, sse=True):
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
                    compOpacities['['+str(compFn.element(i))+']'] = weight.influence() * opacityMult
            except Exception, e:
                print e.__str__()
                print 'Soft selection appears invalid, skipping for shape "%s".' % shapeDag.partialPathName()
    # Load SoftSelection from file, if it is turned off
    else:
        ssd = open (cmds.fileDialog2( cap='Choose file with SoftSelected verts', fm=1, dialogStyle=1, ff='.ssd files (*.ssd)' )[0])
        compOpacities = pickle.load (ssd)
    # List of Soft Selected verts
    vertListCompOKeys = compOpacities.keys()
    cmds.softSelect(sse=0)
    # Selecting whole object 
    name = cmds.ls ( sl=True )
    if len(name) == 0:
        print "Object is not selected"
        sys.exit()
    main_name = name[0].split('.')
    cmds.select(main_name[0])

    # Get dict of Soft Selected verts and their coord    
    headObj = cmds.ls(sl=True)
    for head in headObj:
        for vert in vertListCompOKeys:
            head_vert = head + '.vtx' + str(vert)
            vertCoord = cmds.xform(head_vert, q=True, t=True)
            baseVertDict[vert] = vertCoord

    return compOpacities, vertListCompOKeys, baseVertDict
    
#----------------------------------------------------------------------------------------------------------------------

def SaveSoftSelection(*Args):
    global compOpacities
    global adress
    result = cmds.promptDialog(
                title='Enter Name',
                message='Enter Name:',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')

    if result == 'OK':
        text = cmds.promptDialog(query=True, text=True)
    # Save to file
    ssd = open( adress + text + '.ssd', 'w' )
    pickle.dump( compOpacities, ssd )
    ssd.close()
  
#----------------------------------------------------------------------------------------------------------------------  
def do_it(*Args):
    SaveSoftSelected()
    LoadDelta(*Args)
    

createUI('Blendmaker 01')  

