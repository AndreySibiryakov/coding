# coding=1251

import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import re

class GetInfo():
    #print 'request = %s' % request
    # ������� ��� �������� �� ���� � ����������� � ����� ���������
    fullPathName = ''
    fullPathName = cmds.file(q = True, exn = True)
    fullPathName = fullPathName.split('/')
    fileName = fullPathName[-1]
    fileName = fileName[:-3]
    leftTrim = fileName.find('_')
    animName = fileName[(leftTrim + 1):]
    filePathList = fullPathName[:-1]    
    filePath = ''
    for filePathListItem in filePathList:
        filePath += filePathListItem + '/'    
    
    # ������� ��� ����� �������
    
    # �������� ����� �� ������� ��� ������� �� ���� ��������� �����
    # ���� ��� - ���������� ��� �������
    dDir = fullPathName[-3] + '\\'
    dName = fullPathName[-3]
    if '_' not in dDir:
        if filter(str.isdigit, str(dDir)) == '':
            # ������� ����, ���� �������� ��� ������� �����, 'case_dialogue'
            result = cmds.promptDialog(
            		title='working dir name',
            		message='add working dir',
            		button=['OK', 'Cancel'],
            		defaultButton='OK',
            		cancelButton='Cancel',
            		dismissString='Cancel')
            
            if result == 'OK':
                workingName = cmds.promptDialog(query=True, text=True)
                workingDirName = workingName.upper() + '\\'
            
            if result == 'Cancel':
                sys.exit('Cancelled')
    
    
    # ����� ������� ����
    workPath = 'e:\SH8\.dialogues\\'
    # ����� ����, ��� �������� .ma �������� lkz trax editor
    clipPath = 'z:\.src\shared\chr\_face\.clips\\'
    # ����� ����, ��� �������� ����� ��������
    atomPath = 'z:/.src/shared/chr/_face/.anims_atom/'
    # ������ ������ �� ������ ��������
    atomList = cmds.getFileList(fs = '*.atom', fld = atomPath)    
    # ����� ����, ��� �������� .avi, ����� ��� ��������� � ������ ��������
    animPreviewPath = 'z:/.src/shared/chr/_face/.anims_preview_database/'
    # ����� ������� ������� ��� ���������� ����������
    animChrPath = 'e:\SH8\.dialogues\.crhs\\'
    # ����� ��� character set
    charSet = 'default_character'
    # ����� ����, ��� �������� .fbx ��������
    animFBXDir = 'anims_FBX\\'
    # ����� ������� ������� ��� ���������� ����������
    refFbxDir = 'e:\SH8\.dialogues\.crhs\.fbx_ref\\'
    # ����� ����, ��� �������� .fbx ��������
    animMBDir = 'anims_MB\\'
    # ����� ��������� ��� �������� ref ��������
    refPrefix = '_face_10_fr_ref.fbx'
    
    vidRefsDir = 'vids_refs\\'
    
    workDirs = 'anims_FBX anims_MB vids_refs_UNREAL vids_refs_GOPRO vids_refs chr_MB chr_FBX'
    
    vidRefsPath = workPath + dDir + vidRefsDir
    # ��������� ������ ���� image sequence
    imgList = cmds.getFileList(fld = vidRefsPath)
    
    imgPath = vidRefsPath + fileName + '_001.jpeg'
    # ������ ������ �� ������, ��� �������� �� � .ma
    animCurvesList = cmds.ls(type='animCurve')
    # ������ ������ ��� ������� ������������
    ctrlsList = cmds.ls('*_ctrl')
    logHead = '\n---------- export log:----------\n'
    # ���� � �����, ��� ���������� ������ ��������
    animListPath = workPath + dDir + '_anim_list.txt'
    # ���� � ����� .fbx �������� �������� �������
    animFBXPath = workPath + dDir + animFBXDir
    # ���� � ����� .mb �������� �������� �������
    animMBPath = workPath + dDir + animMBDir
    
    # ��������� ������ �� ������, ���������� chr templates
    chrMBList = cmds.getFileList(fs = '*.mb', fld = animChrPath) 
    # ��������� ������ �� ������, .fbx ref �������� chr templates
    refAnimList = cmds.getFileList(fs = '*.fbx', fld = refFbxDir) 
    # ��������� ������ �� ������, .fbx ref �������� chr templates
    animMBList = cmds.getFileList(fs = '*.mb', fld = animMBPath) 
    # ������ ����������, ��� ����� �������� ������ � ����� timeline
    EndTime = cmds.playbackOptions( q=True, maxTime=True )
    StartTime = cmds.playbackOptions( q=True, minTime=True )    
    
def PromptDialogue(pdTitle, pdMessage):
    result = cmds.promptDialog(
        title = pdTitle,
        message = pdMessage,
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')
    
    if result == 'OK':
        input = cmds.promptDialog(query=True, text=True)
        return input
    
    if result == 'Cancel':
        sys.exit('Cancelled')
    
    
    
cmds.window(t = 'Face Animation Tools')
form = cmds.formLayout()
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )


child1 = cmds.columnLayout( columnAttach=('both', 10), rowSpacing=5, columnWidth=200 )
cmds.button(label="DIRs", h = 40, command = 'CreateDIRs()', bgc = (1,1,1,))
cmds.button(label="Anim Template Files", h = 40, command = 'CopyAnims()', bgc = (1,1,1,))
cmds.button(label="LOCs \nand Ctrls for Character", h = 40, command = 'PrepareChr()', bgc = (1,1,1,))
cmds.button(label="Iimage Plane", command = 'CreateImgPlane()', bgc = (1,1,1,))
cmds.button(label="Clip", h = 40, command = 'CreateClip()', bgc = (1,1,1,))
cmds.button(label="Import Clip", h = 40, command = 'ImportClip()', bgc = (1,1,0,))
cmds.button(label="Import Atom", h = 40, command = 'ImportAtom()', bgc = (1,1,0,))
cmds.button(label="AimConstraint on Eyes", command = 'EyeAimC()', bgc = (1,1,0,))
cmds.button(label="FOV = 85, NTSC", command = 'FovNtsc()', bgc = (1,1,0,))
cmds.button(label="Rename with suffix", command = 'Rename()', bgc = (1,1,0,))
cmds.setParent( '..' )

child2 = cmds.columnLayout( columnAttach=('both', 10), rowSpacing=5, columnWidth=200 )
cmds.button(label="Reset Attributes", command = 'ResetAttrs()', bgc = (1,1,1,))
cmds.button(label="Reset Attributes on Selected", command = 'ResetSelAttrs()', bgc = (1,1,1,))
cmds.button(label="Cut Keys on Selected", command = 'CutSelKeys()', bgc = (1,0,0,))
cmds.button(label="Delete Keys on LOCs", command = 'DelLOCKeys()', bgc = (1,1,1,))
cmds.button(label="Copy LOCs", h = 40, command = 'CopyPOs()', bgc = (1,1,0,))
cmds.button(label="Paste LOCs", command = 'PastePos()', bgc = (0,1,0,))
cmds.button(label="Paste Additive LOCs", command = 'PasteAdditivePose()', bgc = (1,0,0,))
cmds.button(label="Substract LOCs", command = 'SubstractPos()', bgc = (0,1,0,))
cmds.button(label="Paste Mirror LOCs", command = 'PasteMirrorPose()', bgc = (0,1,0,))
cmds.button(label="Paste Additive Mirror LOCs", command = 'PasteAdditiveMirrorPose()', bgc = (1,0,0,))
cmds.setParent( '..' )

child3 = cmds.columnLayout( columnAttach=('both', 10), rowSpacing=5, columnWidth=200 )
cmds.button(label=".py Scripts\n'SDK', 'FaceGraph'", h = 40, command = 'CollKeys()', bgc = (1,1,1,))
# cmds.button(label=".atom, .avi, .ma, .fbx", h = 40, command = 'AnimExport()', bgc = (1,1,0,))
# cmds.button(label=".fbx", h = 40, command = 'FbxExport()', bgc = (1,1,0,))
# cmds.button(label=".fbx batch", h = 40, command = 'BatchAnimExport()', bgc = (1,1,0,))
cmds.button(label="10 Frame Reference", command = 'RefAnimExport()', bgc = (1,1,0,))
cmds.button(label="Print Scene Duration", command = 'ScnDur()', bgc = (0,1,1,))
cmds.setParent( '..' )

cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Create'), (child2, 'Animate'), (child3, 'Export')) )

cmds.showWindow()

'''****************************************************************************************************'''

# ������ �������
def Rename():
    suffix = PromptDialogue('Add suffix to rename', 'suffix')
    cmds.file(rn = GetInfo.filePath + GetInfo.fileName + '_' + suffix + '.mb' )
    cmds.file(s = True)

'''****************************************************************************************************'''

def ImportAtom():
    if not cmds.objExists('eyes_aim_ctrl'):
        EyeAimC()
    # ������ ������ ������ .atom �������� �� �� ����������� ������
    countName = PromptDialogue('import .atom anim', 'type anim count name')
    
    cmds.select('*ctrl')
    for atomAnim in GetInfo.atomList:
        if countName in atomAnim:
            atomFilePath = GetInfo.atomPath + atomAnim
            mel.eval('loadPlugin atomImportExport')
            # mel.eval('file -import -type "atomImport" -ra true -namespace $atomAnim -options ";;targetTime=3;option=replace;match=hierarchy;;selected=selectedOnly;search=;replace=;prefix=;suffix=;mapFile=C:/Users/user/Documents/maya/projects/default/data/;" $atomFilePath;')
            mel.eval('file -import -type "atomImport" -ra true -options ";;targetTime=3;option=replace;match=hierarchy;;selected=selectedOnly;search=;replace=;prefix=;suffix=;mapFile=C:/Users/user/Documents/maya/projects/default/data/;" "%s";' % atomFilePath)
    
    ctrlsList = cmds.ls('*ctrl')
    timeKeyList = ''
    checkMax = []
    
    for ctrl in ctrlsList:
        attrsList = cmds.listAttr(ctrl, k = True)
        for attr in attrsList:
            timeKeyList = cmds.keyframe(ctrl + '.' + attr, q = True)
            if timeKeyList:
                checkMax.append(timeKeyList)
    
    animEnd =  int(max(checkMax)[-1])
    animStart = int(min(checkMax)[0])
    
    cmds.playbackOptions( minTime=animStart, maxTime=animEnd )
    
'''****************************************************************************************************'''

def FovNtsc():
    # ��������� ���������� fov ������ �����������
    cmds.camera('persp', fl=85, e=1)
    # ����� fps 30 ������ � �������
    cmds.currentUnit( time='ntsc' )

'''****************************************************************************************************'''

def EyeAimC():
    import FAT_AddEyeAimConstraint
    reload(FAT_AddEyeAimConstraint)

'''****************************************************************************************************'''

def CreateDIRs():
    workDirName = PromptDialogue('working dir name', 'add working dir')
    workDir = workDirName + '\\'
    
    # ������ ������������
    workDirList = GetInfo.workDirs.split()
    for dirName in workDirList:
        cmds.sysFile(GetInfo.workPath + workDir + dirName, md = True)
    
    # ������ ����, ������� ����� ��������� ������ ��������
    animListName = GetInfo.workPath + workDir + workDirName + '_anim_list.txt'
    animListFile = open(animListName, 'w')
    animListFile.close()
print '*'*100
def CopyAnims():
    import FAT_CopyChrToAnims
    reload(FAT_CopyChrToAnims)

def CreateClip():
    import FAT_CreateClip
    reload(FAT_CreateClip)

def ImportClip():
    mel.eval('doImportClipArgList 4 { "1","1" }')

'''****************************************************************************************************'''

def CreateImgPlane():
    # ������ ������ �� ������ image sequence
    propImgList = []
    
    # �������� ������, ����� ������ ���-�� ������
    for imgName in GetInfo.imgList:
        if GetInfo.fileName in imgName:
            propImgList.append(imgName)
            imgExists = True
    
    # ���� image sequence ���������� ��� ������� �����
    if imgExists == True:
    
        # ����� timeline range ������ ���-�� ������
        propImgList.sort()
        lastImg = propImgList[-1]
        lastImg = lastImg.split('.')
        lastImg = lastImg[0]
        maxTime = lastImg[-2-1:]
        
        cmds.playbackOptions( minTime=0, maxTime=maxTime )
    
        # ������ image plane
        myImagePlane = cmds.imagePlane(w = 22, h = 22)
        cmds.setAttr(myImagePlane[1] + '.type', 0)
        cmds.setAttr(myImagePlane[1] + '.frameOffset', 0)
        cmds.setAttr(myImagePlane[1] + '.useFrameExtension', 1)
        cmds.setAttr(myImagePlane[1] + '.imageName', GetInfo.imgPath, type = 'string')
        
    else:
        print 'Image reference not found'
        
    # ��������� image plane � ������ �����, ����� ������
    cmds.delete(cmds.pointConstraint('jaw_LOC', 'imagePlane1'))
    cmds.move(-16, 0, 0, r = True, ls = True, wd = True)

'''****************************************************************************************************'''

def RefAnimExport():
    import FAT_Export10FramesForReferenceAnim
    reload(FAT_Export10FramesForReferenceAnim)

def PrepareChr():
    import FAT_PrepareChr
    reload(FAT_PrepareChr)
    
def CollKeys():
    import FAT_CollectKeysFromTimeline
    reload(FAT_CollectKeysFromTimeline)    
    
def ResetAttrs():
    import FAT_ResetAttributesOnSelected
    reload(FAT_ResetAttributesOnSelected) 

def ScnDur():
    import FAT_PrintSceneDuration
    reload(FAT_PrintSceneDuration) 
    
# ������ �������
def ResetSelAttrs():
    selectedCtrls = cmds.ls(sl = True)
    for ctrl in selectedCtrls:
        attrs = cmds.listAttr(ctrl, k=True) #������� ������ ��������� ��� ������� �� ���������� ��������
        for attr in attrs: #��� ������� �������� �� ������ ���������
            if attr != "visibility": #���� �� �� ���������� 
                cmds.setAttr(ctrl + "." + attr, 0) #��� �������+�����+�������� �������� ��������� ����
            
def CutSelKeys():
    # coding=1251
    
    import maya.cmds as cmds
    
    selectedCtrls = cmds.ls(sl = True)
    cmds.cutKey(selectedCtrls)           

def DelLOCKeys():
    boneList = cmds.ls('*_LOC')
    cmds.cutKey(boneList)
    
def CopyPOs():
    # ������ ������, ��� ����� �������� ������ � ����
    setAttribList = []   
    global setAttribList
    # ������� ������ ����, ���������, �������� ���������� ��������
    locList = cmds.ls(sl = True)
    global locList
    for loc in locList:
        locListed = cmds.listAttr(loc, k = True)
        for locAttr in locListed:
            if locAttr != 'visibility':
                locAttrsValue = cmds.getAttr(loc + '.' + locAttr)
                # ������ �������, ���� ����� �������� ������� � ��������� � �������
                if 'e' in str(locAttrsValue):
                    locAttrsValue = str(locAttrsValue)[:-4]
                locAttrsValue = round(float(locAttrsValue), 5)
                setAttribList.append(loc + ' ' + locAttr + ' ' + str(locAttrsValue))  
    
def PastePos():
    # �������� ������������ �����
    for setAttrib in setAttribList:
        # �������� ������ �� ����������, ������� �������� ���
        splitKey = setAttrib.split()
        object = splitKey[0]
        attribute = splitKey[1]
        value = splitKey[2]
        cmds.setAttr(object + '.' + attribute, float(value))
    cmds.setKeyframe(locList) 

def SubstractPos():
    # paste copied and mirrored keys as additive to current pose
    for setAttrib in setAttribList:
        splitKey = setAttrib.split()
        object = splitKey[0]
        attribute = splitKey[1]
        value = splitKey[2]
        if not 'scale*' in attribute:
            currValue = cmds.getAttr(object + '.' + attribute)
            additiveValue = (currValue - float(value))
            cmds.setAttr(object + '.' + attribute, additiveValue)
    cmds.setKeyframe(locList)

def PasteMirrorPose():
    # ������ �������, ������� ��������� �������� �� '-'
    # � �������� ��� �� ���������������
    def MirrorChange(value):
        if '-' in value:
            value = value[1:]
        else:
            value = '-' + value
        return value
    
    # ����� ��������, �� ������� ������������, ������ ��� ����� �������
    lPref = 'l_'
    rPref = 'r_'
    
    # paste copied and mirrored keys
    for setAttrib in setAttribList:
        splitKey = setAttrib.split()
        object = splitKey[0]
        attribute = splitKey[1]
        value = splitKey[2]
        # �������� ������� �� ����� �������
        objPref = object[0:2]
        # ����� ������� ��� ����������� ����������� ��������
        if 'rotateY' in attribute:
            value = MirrorChange(value)
        if 'rotateZ' in attribute:
            value = MirrorChange(value)    
        if 'translateX' in attribute:
            value = MirrorChange(value)
        if rPref in objPref:
            object = lPref + object[2:]
        if lPref in objPref:
            object = rPref + object[2:]    
        cmds.setAttr(object + '.' + attribute, float(value))
    cmds.setKeyframe(locList)

def PasteAdditiveMirrorPose():
    # ������ �������, ������� ��������� �������� �� '-'
    # � �������� ��� �� ���������������
    def MirrorChange(value):
        if '-' in value:
            value = value[1:]
        else:
            value = '-' + value
        return value
    
    # ����� ��������, �� ������� ������������, ������ ��� ����� �������
    lPref = 'l_'
    rPref = 'r_'
    
    # paste copied and mirrored keys as additive to current pose
    for setAttrib in setAttribList:
        splitKey = setAttrib.split()
        object = splitKey[0]
        attribute = splitKey[1]
        value = splitKey[2]
        # �������� ������� �� ����� �������
        objPref = object[0:2]
        # ����� ������� ��� ����������� ����������� ��������
        if 'rotateY' in attribute:
            value = MirrorChange(value)
        if 'rotateZ' in attribute:
            value = MirrorChange(value)    
        if 'translateX' in attribute:
            value = MirrorChange(value)
        if rPref in objPref:
            object = lPref + object[2:]
        if lPref in objPref:
            object = rPref + object[2:]    
        if not 'scale*' in attribute:
            currValue = cmds.getAttr(object + '.' + attribute)
            additiveValue = (currValue + float(value))
            cmds.setAttr(object + '.' + attribute, additiveValue)
    cmds.setKeyframe(locList)

def PasteAdditivePose():
    
    # paste copied and mirrored keys as additive to current pose
    for setAttrib in setAttribList:
        splitKey = setAttrib.split()
        object = splitKey[0]
        attribute = splitKey[1]
        value = splitKey[2]
        if not 'scale*' in attribute:
            currValue = cmds.getAttr(object + '.' + attribute)
            additiveValue = (currValue + float(value))
            cmds.setAttr(object + '.' + attribute, additiveValue)
    cmds.setKeyframe(locList)

def AnimExport():
    if cmds.objExists('imagePlane1'):
        cmds.hide('imagePlane1')
    cmds.hide('*_LOC')
    
    # ����� ��������� ��������
    # ������ �� character set
    if cmds.objExists('default_character'):
        if cmds.objExists('*Source'):
            activeClipCheck = cmds.clip('default_character', active = True, q = True)
            if activeClipCheck != 'default':
                cmds.select(animName + 'Source')
                cmds.select(GetInfo.charSet + 'Clips1', add = True)
                cmds.select(GetInfo.animCurvesList, add = True)
    # ����� ������� clip � .ma
    cmds.file(GetInfo.clipPath + GetInfo.animName + '.ma', type='mayaAscii', exportSelected=True)
    
    # ����� ������� �������� � .atom
    maxTime = cmds.playbackOptions( q = True, maxTime = True)
    cmds.select(ctrlsList)
    mel.eval('string $animName = `python "animName"`;')
    mel.eval('string $maxTime = `python "maxTime"`;')
    mel.eval('loadPlugin atomImportExport')
    mel.eval('file -force -options "precision=8;statics=1;baked=0;sdk=0;constraint=0;animLayers=1;selected=selectedOnly;whichRange=1;range=1:$maxTime;hierarchy=none;controlPoints=1;useChannelBox=1;options=keys;copyKeyCmd=-animation objects -option keys -hierarchy none -controlPoints 1 " -typ "atomExport" -es ("z:/.src/shared/chr/_face/.anims_atom/" + $animName + ".atom");')
    
    # ������ �������� � ��� ����, ����� ��� ��������������� ��������� �������
    cmds.select(ctrlsList)
    cmds.scaleKey(iub = False, ts = 0.5, tp = 1, fs = 0.5, fp = 1, vs = 1, vp = 0)
    # ����� ����� ������� timeline
    maxTime = (cmds.playbackOptions( q = True, maxTime = True)/2)
    maxTime = round(maxTime)
    cmds.playbackOptions(maxTime = int(maxTime))
    # ����� ������� ����� ��� ���������
    cmds.playblast(fo = True, v= False, fmt = 'movie', f = 'z:/.src/shared/chr/_face/.anims_preview_database/' + animName + '.avi' )
    
    # ����� �������� �� �������, ������� �� �������� � ��������
    # ����� ������ ��� ������ ��������, �������� ������ ���� 2015
    if cmds.objExists('eyes_CTRL'):
        cmds.rename('eyes_CTRL', 'eyes_ctrl')
    
    # ������ ������ � �������� ������ �����
    # ��������, ���� �� �������� ��
    if cmds.objExists('tongue_1_GRP'):
        cmds.delete('tongue_1_GRP', 'tongue_2_GRP')
        
    # ������ ����������, ��� ����� �������� ������ � ����� timeline
    currEndTime = cmds.playbackOptions( q=True, maxTime=True )
    currStartTime = cmds.playbackOptions( q=True, minTime=True )
    
    # ������� ��� ������� �����������
    cmds.select(ctrlsList)
    
    cmds.currentTime(currStartTime, edit=True) 
    cmds.setKeyframe(ctrlsList)
    cmds.currentTime(currEndTime, edit=True)
    cmds.setKeyframe(ctrlsList)
    
    # ������ ����� �� 10 ������ ������ ������������ �� �������
    cmds.keyframe(edit=True, relative = True, timeChange = (0 + 10))
    
    # ����� ����� ������� timeline
    currEndTime += 20
    cmds.playbackOptions( minTime=0, maxTime=currEndTime )
    
    # ������ �������, ������� ������� ��� ������ �������� �� ������
    def SetKeysToZero():
        global ctrlsList
        for ctrl in ctrlsList:
            attrs = cmds.listAttr(ctrl, k=True) #������� ������ ��������� ��� ������� �� ���������� ��������
            for attr in attrs: #��� ������� �������� �� ������ ���������
                if attr != "visibility": #���� �� �� ���������� 
                    cmds.setAttr(ctrl + "." + attr, 0) #��� �������+�����+�������� �������� ��������� ����
    
    # ������ ������� ����� ������� ������������ ������� � ����� timeline
    cmds.currentTime(currStartTime, edit=True) 
    SetKeysToZero()
    cmds.currentTime(currEndTime, edit=True)
    SetKeysToZero()
    
    # ������� �������� �� timeline ��� ���� ������
    fullSkeletonList = cmds.ls(type = 'joint')
    cmds.select(fullSkeletonList)
    cmds.bakeResults(fullSkeletonList, t=(currStartTime,currEndTime), simulation=True, sb=1) 
    
    # �������� ���������� pytjon � mel
    mel.eval('string $animName = `python "animName"`;')
    mel.eval('string $animFBXPath = `python "animFBXPath"`;')
    
    # ����� ������� ���������� ������ � .fbx � ������ �����
    fullSkeletonList = cmds.ls(type = 'joint')
    cmds.select(fullSkeletonList)
    mel.eval('FBXExportConstraints -v 0')
    mel.eval('FBXLoadExportPresetFile -f "c:/Users/user/Documents/maya/FBX/Presets/2014.1/export/AnimationOnly.fbxexportpreset"')
    mel.eval('FBXExport -f ($animFBXPath + $animName + ".fbx") -s')
    
    # ������ ��� ������
    print '\n---------- export log:----------\n'
    if os.path.exists(atomPath + animName + '.atom'):
        print '.atom exported'
    else:
        print '.atom NOT exported'
    if os.path.exists(clipPath + animName + '.ma'):
        print '.ma exported'
    else:
        print '.ma NOT exported'
    if os.path.exists(animPreviewPath + animName + '.avi'):
        print '.avi exported'
    else:
        print '.avi NOT exported'
    if os.path.exists(animFBXPath + animName + '.fbx'):
        print '.fbx exported'
    else:
        print '.fbx NOT exported'


def BatchAnimExport():
    '''
    �������� ������ �������, ������� ������� ref ���� ��� ����������
    ���������, ���������� �� ref .fbx
    ���� �� 
        �������� .fbx � ������ �����
    ���� ���
        ������� .fbx
        �������� � ������� �����
    '''
    
    # coding=1251
    
    import maya.cmds as cmds
    import maya.mel as mel
    import os
    import re
    import sys
    
    # ������� ����, ���� �������� ��� ������� �����, 'case_dialogue'
    result = cmds.promptDialog(
    		title='working dir name',
    		message='add working dir',
    		button=['OK', 'Cancel'],
    		defaultButton='OK',
    		cancelButton='Cancel',
    		dismissString='Cancel')
    
    if result == 'OK':
        workingName = cmds.promptDialog(query=True, text=True)
        workingDirName = workingName.upper() + '\\'
    
    if result == 'Cancel':
        sys.exit('Cancelled')
    
    # ����� ������� �������
    workDirPath = 'e:\SH8\.dialogues\\'
    # ����� ������� ������� ��� ���������� ����������
    animChrPath = 'e:\SH8\.dialogues\.crhs\\'
    # ����� ������� ������� ��� ���������� ����������
    refFbxDir = 'e:\SH8\.dialogues\.crhs\.fbx_ref\\'
    # ����� ����, ��� �������� .fbx ��������
    animFBXDir = 'anims_FBX\\'
    # ����� ����, ��� �������� .fbx ��������
    animMBDir = 'anims_MB\\'
    # ����� ��������� ��� �������� ref ��������
    refPrefix = '_face_10_fr_ref.fbx'
    
    log = '\n---------- export log:----------\n'
    
    # ������������� �������
    animListDir = workDirPath + workingDirName
    # ���� � �����, ��� ���������� ������ ��������
    animListName = animListDir + workingName + '_anim_list.txt'
    # ���� � ����� .fbx �������� �������� �������
    animFBXPath = workDirPath + workingDirName + animFBXDir
    # ���� � ����� .mb �������� �������� �������
    animMBPath = workDirPath + workingDirName + animMBDir
    # ��������� ������ �� ������, ���������� chr templates
    chrMBList = cmds.getFileList(fs = '*.mb', fld = animChrPath) 
    # ��������� ������ �� ������, .fbx ref �������� chr templates
    refAnimList = cmds.getFileList(fs = '*.fbx', fld = refFbxDir) 
    # ��������� ������ �� ������, .fbx ref �������� chr templates
    animMBList = cmds.getFileList(fs = '*.mb', fld = animMBPath) 
    # ������ ������ ��� ������� ������������
    ctrlsList = cmds.ls('*_ctrl')
    
    # ������� ����� ������ �������� ��� �������� ���-�� ���������� ��������
    animListForLen = open(animListName,'r')
    animLenLines = animListForLen.readlines()
    animListLen = len(animLenLines)
    animListForLen.close()
    
    # �������, ������� ����������, ����� ��������� ������������ � ������� �� anim_list.txt � ������ chr templates
    def CompareLists(searchInList, searchForList):
        searchList = ''
        for searchInString in searchInList:
            for searchForString in searchForList:
                searchForString = searchForString.split('.')
                if searchForString[0].lower() in searchInString:
                    if not searchForString[0].lower() in searchList:
                        if searchList == '':
                            searchList += searchForString[0].lower()
                        else:
                            searchList += ' ' + searchForString[0].lower()
        return searchList
    
    # �������� ��������� � ����������
    crhsInDialogue = CompareLists(animLenLines, chrMBList)
    
    # ������� � ������ .fbx ����� .fbx ref anims
    for chr in crhsInDialogue.split(' '):
        if os.path.exists(refFbxDir + chr + refPrefix):
            cmds.sysFile(refFbxDir + chr + refPrefix, cp = animFBXPath + chr + refPrefix)
        # ���� .fbx ref anim �� ����������, ������ ���
        if not os.path.exists(refFbxDir + chr + refPrefix):
            cmds.file(animChrPath + chr + '.mb', o = True, f = True)
            # ������� �������� �� timeline ��� ���� ������
            fullSkeletonList = cmds.ls(type = 'joint')
            cmds.select(fullSkeletonList)
            cmds.cutKey()
            cmds.bakeResults(fullSkeletonList, t=(0,10), simulation=True, sb=1) 
            # ����� ������� ���������� ������ � .fbx � ������ �����
            cmds.select(fullSkeletonList)
            mel.eval('string $refFbxDir = `python "refFbxDir"`;')
            mel.eval('string $chrName = `python "chr"`;')
            mel.eval('string $refPrefix = `python "refPrefix"`;')
            mel.eval('FBXExportConstraints -v 0')
            mel.eval('FBXLoadExportPresetFile -f "c:/Users/user/Documents/maya/FBX/Presets/2014.1/export/AnimationOnly.fbxexportpreset"')
            mel.eval('FBXExport -f ($refFbxDir + $chrName + $refPrefix) -s')
            cmds.sysFile(refFbxDir + chr + refPrefix, cp = animFBXPath + chr + refPrefix)        
    
    
    # export animation
    for animMB in animMBList:
        if '_face_' in animMB:
            animFBX = animMB[:-3]
            if not os.path.exists(animFBXPath + animFBX + '.fbx'):
                cmds.file(animMBPath + animMB, o = True, f = True)
                # ������� ��� �������� �� ���� � ����������� � ����� ���������
                fullPathName = cmds.file(q = True, exn = True)
                fullPathName = fullPathName.split('/')
                fileName = fullPathName[-1]
                fileName = fileName[:-3] 
                
                # ������ ����������, ��� ����� �������� ������ � ����� timeline
                currEndTime = cmds.playbackOptions( q=True, maxTime=True )
                currStartTime = cmds.playbackOptions( q=True, minTime=True )
                endTimeScaled = round(currEndTime/2)
                
                cmds.select('*_ctrl')
                cmds.currentTime(currStartTime, edit=True) 
                cmds.setKeyframe('*_ctrl')
                cmds.currentTime(currEndTime, edit=True)
                cmds.setKeyframe('*_ctrl')
        
                # ������ �������� � ��� ����, ����� ��� ��������������� ��������� �������
                cmds.select('*_ctrl')
                cmds.scaleKey(iub = False, ts = 0.5, tp = 1, fs = 0.5, fp = 1, vs = 1, vp = 0)
                cmds.playbackOptions(maxTime = int(endTimeScaled))
        
        
                # ������ ������ � �������� ������ �����
                # ��������, ���� �� �������� ��
                if cmds.objExists('tongue_1_GRP'):
                    cmds.delete('tongue_1_GRP', 'tongue_2_GRP')
            
        
        
                # ������� ��� ������� �����������
                cmds.select('*_ctrl')
                
                # ������ ����� �� 10 ������ ������ ������������ �� �������
                cmds.keyframe(edit=True, relative = True, timeChange = (0 + 10))
        
                # ����� ����� ������� timeline
                currEndTime = cmds.playbackOptions( q=True, maxTime=True )
                currEndTime += 20
                cmds.playbackOptions( minTime=0, maxTime=currEndTime )
        
                # ������ �������, ������� ������� ��� ������ �������� �� ������
                def SetKeysToZero():
                    cmds.select('*_ctrl')
                    ctrlsList = cmds.ls(sl = True)
                    for ctrl in ctrlsList:
                        attrs = cmds.listAttr(ctrl, k=True) #������� ������ ��������� ��� ������� �� ���������� ��������
                        for attr in attrs: #��� ������� �������� �� ������ ���������
                            if attr != "visibility": #���� �� �� ���������� 
                                cmds.setAttr(ctrl + "." + attr, 0) #��� �������+�����+�������� �������� ��������� ����
        
                # ������ ������� ����� ������� ������������ ������� � ����� timeline
                cmds.currentTime(currStartTime, edit=True) 
                SetKeysToZero()
                cmds.currentTime(currEndTime, edit=True)
                SetKeysToZero()
        
                # ������� �������� �� timeline ��� ���� ������
                fullSkeletonList = cmds.ls(type = 'joint')
                cmds.select(fullSkeletonList)
                cmds.bakeResults(fullSkeletonList, t=(currStartTime,currEndTime), simulation=True, sb=1) 
        
                # �������� ���������� pytjon � mel
                mel.eval('string $animName = `python "fileName"`;')
                mel.eval('string $animFBXPath = `python "animFBXPath"`;')
                
                # ����� ������� ���������� ������ � .fbx � ������ �����
                fullSkeletonList = cmds.ls(type = 'joint')
                cmds.select(fullSkeletonList)
                mel.eval('FBXExportConstraints -v 0')
                mel.eval('FBXLoadExportPresetFile -f "c:/Users/user/Documents/maya/FBX/Presets/2014.1/export/AnimationOnly.fbxexportpreset"')
                mel.eval('FBXExport -f ($animFBXPath + $animName + ".fbx") -s')
        
                # ������ ��� ������
                
                if os.path.exists(animFBXPath + fileName + '.fbx'):
                    log += fileName + '.fbx exported \n'
                else:
                    log += fileName + '.fbx NOT exported \n'
    
    print log
    
def FbxExport():
    # coding=1251
    
    import maya.cmds as cmds
    import maya.mel as mel
    import os
    import sys
    
    # ����� ������� ����
    workPath = 'e:\SH8\.dialogues\\'
    # ����� ����, ��� �������� .fbx ��������
    animFBXDir = 'anims_FBX\\'
    # ����� ����, ��� �������� .ma �������� lkz trax editor
    clipPath = 'z:\.src\shared\chr\_face\.clips\\'
    # ����� ����, ��� �������� ����� ��������
    atomPath = 'z:/.src/shared/chr/_face/.anims_atom/'
    # ����� ����, ��� �������� .avi, ����� ��� ��������� � ������ ��������
    animPreviewPath = 'z:/.src/shared/chr/_face/.anims_preview_database/'
    # ����� ��� character set
    charSet = 'default_character'
    # ������� ������ ������� � �����, ��� ������� ������ .avi
    if cmds.objExists('imagePlane1'):
        cmds.hide('imagePlane1')
    cmds.hide('*_LOC')
    # ������ ������ �� ������, ��� �������� �� � .ma
    animCurvesList = cmds.ls(type='animCurve')
    # ������ ������ ��� ������� ������������
    ctrlsList = cmds.ls('*_ctrl')
    
    # ������� ��� �������� �� ���� � ����������� � ����� ���������
    fullPathName = cmds.file(q = True, exn = True)
    fullPathName = fullPathName.split('/')
    fileName = fullPathName[-1]
    fileName = fileName[:-3]
    leftTrim = fileName.find('_')
    animName = fileName[(leftTrim + 1):]
    
    # ������� ��� ����� �������
    dialoguePath = fullPathName[-3] + '\\'
    dialogueDir = fullPathName[-3]
    animFBXPath = workPath + dialoguePath + animFBXDir
    
    # ������� �������, ������� ����� � ������� rkbgf .ma
    # ������ ������� ��� ������, ���� ������ ����� ���������, ���� ��������� ��� ������
    # �� ����, ����������, � ��������, ��� � ������ ����� ���� ��������, clip
    
    # ������ �������� � ��� ����, ����� ��� ��������������� ��������� �������
    cmds.select(ctrlsList)
    cmds.scaleKey(iub = False, ts = 0.5, tp = 1, fs = 0.5, fp = 1, vs = 1, vp = 0)
    # ����� ����� ������� timeline
    maxTime = (cmds.playbackOptions( q = True, maxTime = True)/2)
    maxTime = round(maxTime)
    cmds.playbackOptions(maxTime = int(maxTime))
    # ����� ������� ����� ��� ���������
    
    # ����� �������� �� �������, ������� �� �������� � ��������
    # ����� ������ ��� ������ ��������, �������� ������ ���� 2015
    if cmds.objExists('eyes_CTRL'):
        cmds.rename('eyes_CTRL', 'eyes_ctrl')
    
    # ������ ������ � �������� ������ �����
    # ��������, ���� �� �������� ��
    if cmds.objExists('tongue_1_GRP'):
        cmds.delete('tongue_1_GRP', 'tongue_2_GRP')
        
    # ������ ����������, ��� ����� �������� ������ � ����� timeline
    currEndTime = cmds.playbackOptions( q=True, maxTime=True )
    currStartTime = cmds.playbackOptions( q=True, minTime=True )
    
    # ������� ��� ������� �����������
    cmds.select(ctrlsList)
    
    cmds.currentTime(currStartTime, edit=True) 
    cmds.setKeyframe(ctrlsList)
    cmds.currentTime(currEndTime, edit=True)
    cmds.setKeyframe(ctrlsList)
    
    # ������ ����� �� 10 ������ ������ ������������ �� �������
    cmds.keyframe(edit=True, relative = True, timeChange = (0 + 10))
    
    # ����� ����� ������� timeline
    currEndTime += 20
    cmds.playbackOptions( minTime=0, maxTime=currEndTime )
    
    # ������ �������, ������� ������� ��� ������ �������� �� ������
    def SetKeysToZero():
        global ctrlsList
        for ctrl in ctrlsList:
            attrs = cmds.listAttr(ctrl, k=True) #������� ������ ��������� ��� ������� �� ���������� ��������
            for attr in attrs: #��� ������� �������� �� ������ ���������
                if attr != "visibility": #���� �� �� ���������� 
                    cmds.setAttr(ctrl + "." + attr, 0) #��� �������+�����+�������� �������� ��������� ����
    
    # ������ ������� ����� ������� ������������ ������� � ����� timeline
    cmds.currentTime(currStartTime, edit=True) 
    SetKeysToZero()
    cmds.currentTime(currEndTime, edit=True)
    SetKeysToZero()
    
    # ������� �������� �� timeline ��� ���� ������
    fullSkeletonList = cmds.ls(type = 'joint')
    cmds.select(fullSkeletonList)
    cmds.bakeResults(fullSkeletonList, t=(currStartTime,currEndTime), simulation=True, sb=1) 
    
    # �������� ���������� pytjon � mel
    mel.eval('string $animName = `python "fileName"`;')
    mel.eval('string $animFBXPath = `python "animFBXPath"`;')
    
    # ����� ������� ���������� ������ � .fbx � ������ �����
    fullSkeletonList = cmds.ls(type = 'joint')
    cmds.select(fullSkeletonList)
    mel.eval('FBXExportConstraints -v 0')
    mel.eval('FBXLoadExportPresetFile -f "c:/Users/user/Documents/maya/FBX/Presets/2014.1/export/AnimationOnly.fbxexportpreset"')
    mel.eval('FBXExport -f ($animFBXPath + $animName + ".fbx") -s')






























