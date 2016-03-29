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
            cmds.select('*_ctrl')
            cmds.keyTangent( itt = 'auto', ott = 'auto')

            cmds.select(cl = True)
            for ctrl in ctrlsList:
                if 'eye' not in ctrl:
                    cmds.select(ctrl, add = True)
                    cmds.scaleKey(iub = False, ts = 1, tp = 1, fs = 1, fp = 1, vs = 0.66, vp = 0)
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
cmds.file(new = True, f = True)