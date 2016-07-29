# Delta Save-Load.py

import maya.cmds as cmds
import timeit
import sys
import pickle
import copy
import os
from functools import partial
import datetime
import time


# Working dir
path = "" 
if len( path ) == 0:
    path = cmds.fileDialog2( cap='Choose directory to save Delta', fm=3, dialogStyle=1 )
    os.chdir( path[0] )
    path = path[0]
    
path_draft = path+'/draft/'    # Dir for rought blendshape delta
path_fixed = path+'/fixed/'    # Dir for fixed blendshape delta
vertList = []                  # List of verts numbers


#-----------------------------------------------------------------------------------
# Check qnty of slected objects
def object_qnty_check(object):
    if len(object) > 1:
        print "More than one object is selected"
        return sys.exit()
    if len(object) == 0:
        print "Object isn't selected"
        return sys.exit()

#-----------------------------------------------------------------------------------
# Create dialog window
def createUI( pWindowTitle ):
    
    windowID = 'myWindowID'
    
    # Check UI window qnty 
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )
    
    # UI window structure    
    cmds.window( windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True, w=250 )
    form = cmds.formLayout()
    t = cmds.text( l='Choose object to SAVE' )
    t2 = cmds.text( l='or LOAD blendshape delta' )
    cmds.formLayout( form, edit=True, attachForm=[(t, 'top', 10), (t, 'right', 10), (t, 'left', 10), 
                                                  (t2, 'top', 25), (t2, 'right', 10), (t2, 'left', 10)])  

    cmds.rowColumnLayout( numberOfColumns=3, 
                          columnWidth=[ (1,80), (2,80), (3,80) ],
                          columnOffset=[ (1, 'left', 20), (2, 'left', 10), (3, 'right', 10) ] )

    cmds.separator( h=50, style='none' )
    cmds.separator( h=50, style='none' )
    cmds.separator( h=50, style='none' )
               
    cmds.button( label='   SAVE   ', command=partial(SaveDelta, path_draft))
    cmds.button( label='   LOAD   ', command=LoadDelta )
    cmds.button( label='SAVE FIXED', command=partial(SaveDelta, path_fixed ))
    cmds.separator( h=10, style='none' )
    cmds.showWindow()

#-----------------------------------------------------------------------------------    

def SaveDelta( pPath, *Args ):
    
    global vertList
     
    start_time = timeit.default_timer()
    name = cmds.listAttr( "blendShape1", m=True, k=True )[1:] # List of blendshape attributes (without envelope)

    # set all attributes to 0 and save vert coords for neutral mesh
    keyAttr=[]      
    nullAttr = ()
    vertList = []
    vertDict = {}
    for k in range( len(name) ):
        nullAttr = ( k, 0 )
        keyAttr.append( nullAttr )

    cmds.blendShape( 'blendShape1', edit=True, w=keyAttr )

    headObj = cmds.ls( sl=True )
    object_qnty_check(headObj)
    
    named_vertList = cmds.ls( '.vtx[*]', fl=True )
    
    for vert in named_vertList:
        vert_split = vert.split('[')
        vert_new = '[' + vert_split[-1]
        vertList.append( vert_new )

    for head in headObj:
        for vert in vertList:
            head_vert = head + '.vtx' + vert
            vertCoord = cmds.xform( head_vert, q=True, t=True )
            vertDict[vert] = vertCoord

    # set each (1 by 1) attr value to 1 and save verts coord
    keyAttrCopy = keyAttr[:]    
    vertDictMax = {}
    DeltaDict = {}
    folderName = datetime.datetime.now().strftime( ' %d_%m_%Y %H-%M-%S' )
    print "Preparation time - ", ( timeit.default_timer() - start_time )
    for k in range( len(name) ):
        start_time = timeit.default_timer()
        keyAttrCopy = keyAttr[:]
        keyAttrCopy[k] = ( k, 1 )
        cmds.blendShape( 'blendShape1', edit=True, w=keyAttrCopy )
        for head in headObj:
            for vert in vertList:
                head_vert = head + '.vtx' + vert
                vertCoord = cmds.xform( head_vert, q=True, t=True )
                vertDictMax[vert] = vertCoord
        for key in vertList:
            x = ( vertDictMax[key][0] - vertDict[key][0] )
            y = ( vertDictMax[key][1] - vertDict[key][1] )
            z = ( vertDictMax[key][2] - vertDict[key][2] )
            DeltaDict[key] = [x, y, z]
        if not os.path.exists( pPath+headObj[0]+folderName+'/' ):
            os.makedirs( pPath+headObj[0]+folderName+'/' )
        savedict = open( pPath+headObj[0]+folderName+'/'+str(name[k])+'.bsp', 'w' )
        pickle.dump( DeltaDict,savedict )
        savedict.close()
        print str( name[k] )+' saved'
        print "Saving time - ", ( timeit.default_timer() - start_time )
    return vertList   

#-----------------------------------------------------------------------------------

def LoadDelta(Args):
    # Create vertList if SaveDelta function wasn't used
    if len( vertList ) == 0:
        headObj = cmds.ls( sl=True )
        object_qnty_check(headObj)
        named_vertList = cmds.ls( '.vtx[*]', fl=True )
    
        for vert in named_vertList:
            vert_split = vert.split( '[' )
            vert_new = '[' + vert_split[-1]
            vertList.append( vert_new )
    # Open dialog window to choose directory to load delta        
    folder = cmds.fileDialog2( cap='Choose directory to load Delta', fm=3, dialogStyle=1 )
    adress = folder[0]+"\\"
    pathList_cleared = []    
    targetBlendDict = {}
    named_targetBlendDict = {}
    print "Loading Delta :)"
    # Getting .bsp files from choosen folder
    pathList = os.listdir( adress )
    for element in pathList:
        if '.bsp' in element:
            pathList_cleared.append( element )
        else:
            print 'wrong type - ', element
    pathList = pathList_cleared
    
    target_vertDict = {}
    headObj = cmds.ls( sl=True )
    object_qnty_check(headObj)
    named_target_vertList = cmds.ls( '.vtx[*]', fl=True )
    headObject = headObj[0]
        
    for head in headObj:
        for vert in vertList:
            head_vert = head + '.vtx' + vert
            vertCoord = cmds.xform( head_vert, q=True, t=True )
            target_vertDict[vert] = vertCoord
    k = 25
    for i in range( len(pathList) ):
        start_time = timeit.default_timer()
        named_targetBlendDict.clear()
        path_name = open( adress+pathList[i],'r' )
        DeltaDict = pickle.load( path_name )
        new_name = pathList[i].split('_')[-1].split('.')[0]
        cmds.duplicate( headObj[0], n=headObject+'_'+new_name )
        cmds.select( headObject+'_'+new_name )
        cmds.move( k, 35, 0 )
        k += 25
        for key in vertList:
            x = ( target_vertDict[key][0] + DeltaDict[key][0] )
            y = ( target_vertDict[key][1] + DeltaDict[key][1] )
            z = ( target_vertDict[key][2] + DeltaDict[key][2] )
            targetBlendDict[key] = [x, y, z]
        copy_headObj = cmds.ls( sl=True )  
        for head in copy_headObj:
            for i in targetBlendDict:
                 named_targetBlendDict[head+'.vtx' + str(i)] = targetBlendDict[i]
        for head in copy_headObj:
           for vert, value in named_targetBlendDict.iteritems():
               cmds.xform( vert, t=value )
        print "Loading time - ", head, ( timeit.default_timer() - start_time )
        


# Start UI-script
createUI( 'Delta' )



    