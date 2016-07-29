import maya.cmds as cmds
import timeit
import sys


def object_qnty_check(object):
    
    if len(object) > 1:
        print 'more than one object selected'
        return sys.exit()
    if len(object) == 0:
        print 'no one object selected'
        return sys.exit()
        
vertDict = {}

# Check for qnty of choosen objects, get list of verts
def SaveVert(Args):
    
    vertDict.clear() 
    vertLIst = []
    start_time = timeit.default_timer()
    headObj = cmds.ls(sl=True)
    object_qnty_check(headObj)
    if len(headObj) == 1:
        for head in headObj:
            vertList = cmds.ls(head+'.vtx[*]', fl=True)

    # Get dict of verts and their coord
    for vert in vertList:
        vertCoord = cmds.xform(vert, q=True, t=True)
        vertDict[vert] = vertCoord

    print(timeit.default_timer() - start_time)
    print "Saved"

# Create UI
def createUI( pWindowTitle, LoadVert ):
    
    windowID = 'myWindowID'
    # Check UI window qnty 
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )
        
    cmds.window( windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True )
    # UI window structure
    form = cmds.formLayout()
    t = cmds.text(l='Choose object to SAVE or')
    t2 = cmds.text(l="   LOAD  verts")
    cmds.formLayout( form, edit=True, attachForm=[(t, 'top', 10), (t, 'right', 10), (t, 'left', 10), 
                                                  (t2, 'top', 25), (t2, 'right', 10), (t2, 'left', 10)])  

    cmds.rowColumnLayout( numberOfColumns=3, 
                          columnWidth=[ (1,75), (2,10), (3,75) ],
                          columnOffset=[ (1, 'left', 20), (3, 'right', 20) ] )

    cmds.separator( h=50, style='none' )
    cmds.separator( h=50, style='none' )
    cmds.separator( h=50, style='none' )
    cmds.button( label='  LOAD  ', command=vertTransfer )
    cmds.separator( h=10, style='none' )
    cmds.button( label='  SAVE  ', command=SaveVert )
    cmds.separator( h=10, style='none' )
    cmds.showWindow()
    

# Vert transformation function - transfer saved verts on object
def vertTransfer(Args):
    
    start_time = timeit.default_timer()
    headObj = cmds.ls(sl=True)
    vertDictNew={}
    object_qnty_check(headObj)
    if len(headObj) == 1:
        for head in headObj:
            for i in vertDict:
                 old_vert_split = i.split('[')
                 new_vert_name = ".vtx["+old_vert_split[-1]
                 vertDictNew[head+new_vert_name] = vertDict[i]
    
    for head in headObj:
        for vert, value in vertDictNew.iteritems():
            cmds.xform(vert, t=value)
    print(timeit.default_timer() - start_time)
    print "Loaded"

# Start UI-script
createUI( 'My Title', vertTransfer )



        for vert, value in vertDictNew.iteritems():
            cmds.xform(vert, t=value)