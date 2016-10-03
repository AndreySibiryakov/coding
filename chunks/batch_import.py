import maya.cmds as cmds

def batch_import(type=''):
	'''Import all files of the same type from a specified folder'''
	if file_type == '':
		file_type = "obj"

	folder_path_list = cmds.fileDialog2(fm=3)
	folder_path = folder_path_list[0] + '/'

	files = cmds.getFileList(folder=folder_path, filespec='*.%s' % file_type)
	if len(files) == 0:
	    cmds.warning("No files found")
	else:
	    for f in files:
	        cmds.file(folder_path + f, i=True)
        