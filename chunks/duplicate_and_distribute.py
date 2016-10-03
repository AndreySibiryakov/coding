'''
Duplicate blendshapes of the selected object 
and shift copies along X axis.
Blendshapes should be keyed on an every frame
and a timeline fit all keys.
'''

import maya.cmds as cmds
import sys

def check_selection():
    selection = cmds.ls(selection=True)
    if len(selection) > 1:
        sys.exit('more than one object selected')
    if len(selection) == 0:
        sys.exit('nothing selected')
    else:
        return selection[0]

def duplicate_distribute():
    '''Default X axis shift multiplier is 10 units'''
    select_to_duplicate = check_selection()

    min_time = int(cmds.playbackOptions(min=True, query=True))
    max_time = int(cmds.playbackOptions(max=True, query=True))

    x_shift_multiplier = 10
    x_axis_shift = 0
    for currFrame in range(min_time, (max_time+1)):
        cmds.currentTime(currFrame, edit=True)
        cmds.select(select_to_duplicate)
        duplicate_name = select_to_duplicate + '_' + str(currFrame)
        cmds.duplicate(name=duplicate_name)
        cmds.delete(ch = True)
        duplicate_translation = cmds.xform(duplicate_name, q=True, t=True)
        x_axis_shift += x_shift_multiplier
        cmds.xform(duplicate_name, 
            t=((duplicate_translation[0]+x_axis_shift),duplicate_translation[1],duplicate_translation[2]))
       