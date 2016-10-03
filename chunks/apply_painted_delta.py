'''
Apply painted deformation of an orig model
to another with the same number of vertecies ID.
Use it for as a correction for blendshapes
transferred from one mesh to another

Andrey Sibiryakov
comcommac@gmail.com
2016.09.26
'''

import maya.cmds as cmds
import timeit
import sys

def check_selection(selection):
    if len(selection) > 1:
        sys.exit('more than one object selected')
    if len(selection) == 0:
        sys.exit('nothing selected')

'''
def select_orig(orig_name):
    '''Select original object if other selected,
    when 'save mod' button pressed.'''
    cmds.select(orig_name)
    print 'Selected %s' % orig_name
'''

def save_verts_to_dict(check=False):
    '''Check is for whether dicts got from the same object'''
    if check == True:
        orig_name = get_object_name(orig_verts_dict)
        '''
        mod_verts_dict = save_verts_to_dict()
        if len(orig_verts_dict) != len(mod_verts_dict):
            orig_name = get_object_name(orig_verts_dict)
            select_orig(orig_name)
        orig_name = get_object_name(orig_verts_dict)
        mod_name = get_object_name(mod_verts_dict)
        if orig_name != mod_name:'''
        cmds.select(orig_name)
    verts_dict = {}
    vert_list = []
    #Start timer
    #start_time = timeit.default_timer()
    selection = cmds.ls(sl = True)
    check_selection(selection)
    for head in selection:
        vert_list = cmds.ls(head + '.vtx[*]', fl = True)
    #Get dict of verts and their coord
    for vert in vert_list:
        vert_coord = cmds.xform(vert, q = True, t = True)
        verts_dict[vert] = vert_coord
    
    #print 'done in', (timeit.default_timer() - start_time)
    return verts_dict

def get_object_name(dict):
    for vert, coord in dict.iteritems():
        vert_list = vert.split('.')
        object_name = vert_list[0]
        break
    return object_name

def calculate_diff_dict(orig_verts_dict, mod_verts_dict):
    '''Return difference between original object vertex coordinates 
    before and after correction.'''
    if orig_verts_dict and mod_verts_dict:
        diff_verts_dict = {}
        for key in orig_verts_dict:
            x = ( mod_verts_dict[key][0] - orig_verts_dict[key][0] )
            y = ( mod_verts_dict[key][1] - orig_verts_dict[key][1] )
            z = ( mod_verts_dict[key][2] - orig_verts_dict[key][2] )
            diff_verts_dict[key] = [x, y, z]
    else:
        sys.exit('Either orig or mod dicts not exist')
    return diff_verts_dict

def calculate_sum_dict(diff_verts_dict, target_verts_dict):
    '''Return new coordinates dict with diff added to target object'''
    target_name = get_object_name(target_verts_dict)
    renamed_sum_verts_dict = {}
    for vert, coord in diff_verts_dict.iteritems():
        vert_list = vert.split('.')
        diff_vert_id = vert_list[1]
        renamed_vert = target_name + '.' + diff_vert_id
        x = ( target_verts_dict[renamed_vert][0] + diff_verts_dict[vert][0] )
        y = ( target_verts_dict[renamed_vert][1] + diff_verts_dict[vert][1] )
        z = ( target_verts_dict[renamed_vert][2] + diff_verts_dict[vert][2] )
        renamed_sum_verts_dict[renamed_vert] = [x, y, z]
    return renamed_sum_verts_dict

def load_verts():
    '''Apply collected dict of vertecies position to target object'''
    diff_orig_dict = calculate_diff_dict(orig_verts_dict, mod_verts_dict)
    target_head_list = cmds.ls(sl = True)
    check_selection(target_head_list)
    target_verts_dict = save_verts_to_dict()
    target_dict = calculate_sum_dict(diff_orig_dict, target_verts_dict)
    #start_time = timeit.default_timer()
    #Iterate through source dict and assign coords to target object
    for vert, coord in target_dict.iteritems():
        cmds.xform(vert, t = coord)
    #print 'done in', (timeit.default_timer() - start_time)

def save_orig():
    '''Get and declare global dicts: original and original modified'''
    global orig_verts_dict
    orig_verts_dict = save_verts_to_dict()

def save_mod():
    global mod_verts_dict
    mod_verts_dict = save_verts_to_dict(check=True)

def UI():   
    cmds.window('save load painted delta', width=250)
    cmds.columnLayout( adjustableColumn=True )
    cmds.button(label='save original', command='chunks.apply_painted_delta.save_orig()')
    cmds.button(label='save modyfied', command='chunks.apply_painted_delta.save_mod()')
    cmds.button(label='load on target', command='chunks.apply_painted_delta.load_verts()')
    cmds.showWindow()