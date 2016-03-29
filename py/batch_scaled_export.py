'''
алгоритм работы скрипта, который создает ref позы для персонажей
проверяет, существует ли ref .fbx
если да 
    копирует .fbx в работу папку
если нет
    создает .fbx
    копирует в рабочую папку
'''

import maya.cmds as cmds
import maya.mel as mel
import os
import re
import sys

# вызываю окно, куда вписываю имя рабочей папки, 'case_dialogue'
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

'''
# calling for input substract value dialogue
result = cmds.promptDialog(
		#title='Add subrtact value:',
		message='Add value in percents',
		button=['OK', 'Cancel'],
		defaultButton='OK',
		cancelButton='Cancel',
		dismissString='Cancel')

if result == 'OK':
    perscVal = cmds.promptDialog(query=True, text=True)
    subVal = (100 - float(perscVal))/10
    multVal = float(perscVal)/100

if result == 'Cancel':
    sys.exit('Cancelled')
'''           

# задаю рабочий каталог
workDirPath = 'e:\SH8\.dialogues\\'
# задаю рабочий каталог для настроеных персонажей
animChrPath = 'e:\SH8\.dialogues\.crhs\\'
# задаю рабочий каталог для настроеных персонажей
refFbxDir = 'e:\SH8\.dialogues\.crhs\.fbx_ref\\'
# задаю путь, где хранятся .fbx анимации
animFBXDir = 'anims_FBX\\'
# задаю путь, где хранятся .fbx анимации
animMBDir = 'anims_MB\\'
# задаю приставку для названия ref анимаций
refPrefix = '_face_10_fr_ref.fbx'

log = '\n---------- export log:----------\n'

# папкарабочего диалога
animListDir = workDirPath + workingDirName
# путь к файлу, где содержится список анимаций
animListName = animListDir + workingName + '_anim_list.txt'
# путь к папке .fbx анимаций рабочего диалога
animFBXPath = workDirPath + workingDirName + animFBXDir
# путь к папке .mb анимаций рабочего диалога
animMBPath = workDirPath + workingDirName + animMBDir
# составляю список из файлов, настроеных chr templates
chrMBList = cmds.getFileList(fs = '*.mb', fld = animChrPath) 
# составляю список из файлов, .fbx ref анимаций chr templates
refAnimList = cmds.getFileList(fs = '*.fbx', fld = refFbxDir) 
# составляю список из файлов, .fbx ref анимаций chr templates
animMBList = cmds.getFileList(fs = '*.mb', fld = animMBPath) 
# создаю список для лицевых контроллеров
ctrlsList = cmds.ls('*_ctrl')

# получаю длину списка анимаций для проверки кол-ва выполненых действий
animListForLen = open(animListName,'r')
animLenLines = animListForLen.readlines()
animListLen = len(animLenLines)
animListForLen.close()

# функция, которая определяет, какие персонажи используются в диалоге по anim_list.txt и списку chr templates
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

# сохраняю результат в переменную
crhsInDialogue = CompareLists(animLenLines, chrMBList)

# копирую в рабочу .fbx папку .fbx ref anims
for chr in crhsInDialogue.split(' '):
    if os.path.exists(refFbxDir + chr + refPrefix):
        cmds.sysFile(refFbxDir + chr + refPrefix, cp = animFBXPath + chr + refPrefix)
    # если .fbx ref anim не сущетсвует, создаю его
    if not os.path.exists(refFbxDir + chr + refPrefix):
        cmds.file(animChrPath + chr + '.mb', o = True, f = True)
        # запекаю анимации на timeline для всех костей
        fullSkeletonList = cmds.ls(type = 'joint')
        cmds.select(fullSkeletonList)
        cmds.cutKey()
        cmds.bakeResults(fullSkeletonList, t=(0,10), simulation=True, sb=1) 
        # делаю экспорт выделенных костей в .fbx с именем файла
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
            # отделяю имя анимации от пути и расширенния и имени персонажа
            fullPathName = cmds.file(q = True, exn = True)
            fullPathName = fullPathName.split('/')
            fileName = fullPathName[-1]
            fileName = fileName[:-3] 
            
            # создаю переменные, где храню значение начала и конца timeline
            currEndTime = cmds.playbackOptions( q=True, maxTime=True )
            currStartTime = cmds.playbackOptions( q=True, minTime=True )
            
            if currStartTime < 0:
                cmds.select('*_ctrl')
                addTime = int(currStartTime)*-1
                cmds.keyframe(edit=True, relative = True, timeChange = (0 + addTime))
                currEndTime = currEndTime + addTime           
                cmds.playbackOptions( minTime = 0, maxTime = currEndTime)
            
            currStartTime = cmds.playbackOptions( q=True, minTime=True )
            cmds.select('*_ctrl')
            cmds.currentTime(currStartTime, edit=True) 
            cmds.setKeyframe('*_ctrl')
            cmds.currentTime(currEndTime, edit=True)
            cmds.setKeyframe('*_ctrl')
            
            # сжимаю анимацию в два раза, чтобы она соответствовала реальному времени
            cmds.select('*_ctrl')
            cmds.scaleKey(iub = False, ts = 0.5, tp = 1, fs = 0.5, fp = 1, vs = 1, vp = 0)
            
            currStartTime = cmds.playbackOptions( q=True, minTime=True )
            endTimeScaled = round(currEndTime/2)
            cmds.playbackOptions(maxTime = int(endTimeScaled))
            
            animAmplPath = 'z:\.src\shared\chr\_face\chr_anim_amplitude_list.txt'
            animAmplFile = open(animAmplPath,'r')
            animAmplFile.close
            
            chrNameList = animMB.split('_')
            chrName = chrNameList[0]
            
            perscVal = None
            
            for line in animAmplFile.readlines():
                if chrName in line:
                    chrValList = line.split()
                    if int(chrValList[1]) > 100:
                        sys.exit('Value is greater than 100')
                    else:
                        perscVal = int(chrValList[1])
                        log += '%s has %d percents of animation amplitude\n' % (chrName, perscVal)
            if perscVal == None:
                log += 'no value found for %s, using 100 percents\n' % chrName 
                perscVal = 100            
            
            multVal = float(perscVal)/100
            subVal = (100 - float(perscVal))/10
            
            if perscVal < 100:
                cmds.select(cl = True)
                for ctrl in ctrlsList:
                    if 'eye' not in ctrl:
                        cmds.select(ctrl, add = True)
                
                noEyesCtrlsList = cmds.ls(sl = True)
                
                for ctrl in noEyesCtrlsList:
                    attrsList = cmds.listAttr(ctrl, k = True)
                    for attr in attrsList:
                        timeKeyList = ''
                        valueKeyList = ''
                        timeKeyList = cmds.keyframe(ctrl + '.' + attr, q = True)
                        valueKeyList = cmds.keyframe(ctrl + '.' + attr, vc = True, q = True)
                        if timeKeyList:
                            for count in enumerate(valueKeyList):
                                    cmds.selectKey(ctrl + '.' + attr, k = True, t = (timeKeyList[count[0]],timeKeyList[count[0]]))
                                    if valueKeyList[count[0]] < 0 and valueKeyList[count[0]] < -3:
                                        operator = '+' + str(subVal)
                                        cmds.keyframe(an = 'keys', a = True, vc = (valueKeyList[count[0]] + float(operator)))
                                    if valueKeyList[count[0]] > 0 and valueKeyList[count[0]] > 3:
                                        operator = '-' + str(subVal)               
                                        cmds.keyframe(an = 'keys', a = True, vc = (valueKeyList[count[0]] + float(operator)))
                                    else:
                                        cmds.keyframe(an = 'keys', a = True, vc = (valueKeyList[count[0]]*float(multVal)))
                                    
            # Удаляю группу и локаторы костей языка
            # Временно, пока не настроил их
            if cmds.objExists('tongue_1_GRP'):
                cmds.delete('tongue_1_GRP', 'tongue_2_GRP')
            
            cmds.select('*_ctrl')
            cmds.keyframe(edit=True, relative = True, timeChange = (0 + 10))
            
            # задаю новые границы timeline
            currEndTime = cmds.playbackOptions( q=True, maxTime=True )
            currEndTime += 20
            cmds.playbackOptions( minTime=0, maxTime=currEndTime )
                
            # создаю функцию, которая обнуляю все каналы объектов из списка
            def SetKeysToZero():
                cmds.select('*_ctrl')
                ctrlsList = cmds.ls(sl = True)
                for ctrl in ctrlsList:
                    attrs = cmds.listAttr(ctrl, k=True) #создает список атрибутов для каждого из выделенных объектов
                    for attr in attrs: #для каждого атрибута из списка атрибутов
                        if attr != "visibility": #если он не называется 
                            cmds.setAttr(ctrl + "." + attr, 0) #имя объекта+точка+название атрибута равняется нулю
                
            # ставлю нулевые ключи лицевых контроллеров вначале и конце timeline
            
            cmds.currentTime(currStartTime, edit=True) 
            SetKeysToZero()
            cmds.currentTime(currEndTime, edit=True)
            SetKeysToZero()
            cmds.select('*_ctrl')
            cmds.keyTangent( itt = 'auto', ott = 'auto')
            # запекаю анимации на timeline для всех костей
            fullSkeletonList = cmds.ls(type = 'joint')
            cmds.select(fullSkeletonList)
            cmds.bakeResults(fullSkeletonList, t=(currStartTime,currEndTime), simulation=True, sb=1) 
            
            # делаю экспорт выделенных костей в .fbx с именем файла
            fullSkeletonList = cmds.ls(type = 'joint')
            cmds.select(fullSkeletonList)
            fbxAnimPath = animFBXPath + fileName + '.fbx'

            # перевожу переменные pytjon в mel
            mel.eval('string $animName = `python "fileName"`;')
            mel.eval('string $animFBXPath = `python "animFBXPath"`;')
                        
            #mel.eval('FBXExport -f ("%s") -s;' % fbxAnimPath)
            mel.eval('FBXExportConstraints -v 0')
            mel.eval('FBXLoadExportPresetFile -f "c:/Users/user/Documents/maya/FBX/Presets/2014.1/export/AnimationOnly.fbxexportpreset"')
            mel.eval('FBXExport -f ($animFBXPath + $animName + ".fbx") -s')
    
            # создаю лог работы
            
            if os.path.exists(animFBXPath + fileName + '.fbx'):
                log += fileName + '.fbx exported \n'
            else:
                log += fileName + '.fbx NOT exported \n'
        else:
            log += animFBX + '.fbx exists\n'

print log

logPath = animFBXPath + workingName + '_export_log.txt'
logFile = open(logPath, 'w')
logFile.write(log)
logFile.close()

cmds.file(new = True, f = True)