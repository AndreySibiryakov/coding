'''
Code to call script from the shelf or script editor

import chunks.create_joints
reload(chunks.create_joints)
help(chunks.create_joints)
chunks.create_joints.create_joints()


HZrivet should be installed prior.
https://www.creativecrash.com/maya/script/hzrivet

Also HZrivet was modified 
to name locators according to mask LOC_0...

Current script creates joints on top of locators
created with HZrivet

To do:
Create dictionary for bones:subelementID
and store it in file as a preset to be able to apply later
on any other character with the same topology.
'''

import maya.cmds as cmds
import HZrivet.UI
import re

def create_joints():
	'''Subelements: vertecies, faces, edges should be selected'''
	# Get selected object name
	selection_list = cmds.ls(selection=True)
	for selection in selection_list:
		selected_object = selection.split('.')[0]
		break
	old_loc_list = cmds.ls('*LOC*', flatten=True)
	#Create locators constrained to subelements
	HZrivet.UI.HZrivet_finalCC()
	current_loc_list = cmds.ls('*LOC*', flatten=True)
	#Filter created locators
	new_loc_list = [loc for loc in current_loc_list if loc not in old_loc_list]
	# Get list of locators names and apply it as a prefix to a joint name
	loc_list = [loc for loc in new_loc_list if 'Shape' not in loc]
	root_joint = 'root'
	if not cmds.objExists(root_joint):
	    cmds.select(clear=True)
	    cmds.joint(name=root_joint)
	    root_p_constraint = cmds.pointConstraint(selected_object, root_joint)
	    root_o_constraint = cmds.orientConstraint(selected_object, root_joint)
	    cmds.delete(root_p_constraint, root_o_constraint)
	for loc in loc_list:
	    joint_prefix = re.sub("\D", "", loc)
	    joint_name = 'JNT_' + joint_prefix
	    cmds.select(clear=True)
	    cmds.joint(name=joint_name)
	    cmds.pointConstraint(loc, joint_name)
	    cmds.orientConstraint(loc, joint_name)
	    cmds.parent(joint_name, 'root') 
