import wrap
import os


path = wrap.openFileDialog()
target_scan_dir = os.path.dirname(path) + "/"
print 'choosed dir - ' + target_scan_dir

#target_scan_dir = 'd:/Cthulhu/3d_scanning/Leha_phomens/neutral_uni_nonrigid_generate/'
neutral_name = 'neutral_uni'

def get_file_path(name, mesh_list, type = 'obj'):  
    for mesh_name in mesh_list:  
        if name + '.' + type in mesh_name:  
            print 'got ' + name + '.' + type  
            return mesh_name  
 
def generate_points_name(name, target_scan_dir, prefix='_nonrigid'):  
    file_name = target_scan_dir + name + prefix + '.points'
    return file_name

def get_rigid_aligned_name(file_path, type = 'obj'):  
    file_path_list = file_path.split('.obj')
    aligned_path = file_path_list[0] + '_aligned.obj'  
    return aligned_path  
  
def get_scan_names(scan_files_list, neutral = True):  
    scan_names_list = []  
    split_names_list = []  
    for path in scan_files_list:
        if '.obj' in path:
            split_path = path.split('/')  
            split_name = split_path[-1].split('.')  
            split_names_list.append(split_name[0])  
        
    scan_names_list = list(set(split_names_list))  
    if neutral == False:
        scan_names_list.remove(neutral_name)  
    return scan_names_list  
     
scan_files_list = [] 
for path, dirs, file_names in os.walk(target_scan_dir):
    for file_name in file_names:
        if not '_aligned' in file_name:
            full_file_path = os.path.join(path, file_name) 
            scan_files_list.append(full_file_path)
        else:
            print file_name + " not added to list"

scan_names = get_scan_names(scan_files_list, neutral=False)  

# load mesh for nonrigid points
neutral_mesh = get_file_path(neutral_name, scan_files_list, type = 'obj')  
neutral_mesh_texture = get_file_path(neutral_name, scan_files_list, type = 'jpg')  
neutral_mesh_points_path = generate_points_name(neutral_name, target_scan_dir, prefix='_nonrigid')
neutral_mesh = wrap.Geom(neutral_mesh)  
neutral_mesh.wireframe = False  
neutral_mesh.texture = wrap.Image(neutral_mesh_texture)  
neutral_mesh.texture.show()  

for scan_name in scan_names: 
    print scan_name
    scan_mesh = get_file_path(scan_name, scan_files_list, type = 'obj')  
    scan_mesh_texture = get_file_path(scan_name, scan_files_list, type = 'jpg')  
    scan_mesh_points_path = generate_points_name(scan_name, target_scan_dir, prefix='_nonrigid')
    scan_mesh = wrap.Geom(scan_mesh)  
    scan_mesh.wireframe = False  
    scan_mesh.texture = wrap.Image(scan_mesh_texture)  
    scan_mesh.texture.show()  
    #scan_mesh_points = wrap.selectPoints(scan_mesh)
    neutral_check = False
    scan_check = False
    if os.path.isfile(neutral_mesh_points_path) == True:
        neutral_mesh_points = wrap.loadPoints(neutral_mesh_points_path)
        neutral_check = True
    if os.path.isfile(scan_mesh_points_path) == True:
        scan_mesh_points = wrap.loadPoints(scan_mesh_points_path)
        scan_check = True
    # 
    if (neutral_check == True and scan_check == True):
        (scan_mesh_points, neutral_mesh_points) = wrap.selectPoints(scan_mesh, neutral_mesh, 
                                                                    pointsRight=neutral_mesh_points,
                                                                    pointsLeft=scan_mesh_points)
    elif (neutral_check == False and scan_check == True):
        (scan_mesh_points, neutral_mesh_points) = wrap.selectPoints(scan_mesh, neutral_mesh, 
                                                                    pointsLeft=scan_mesh_points)
    elif (neutral_check == True and scan_check == False):
        (scan_mesh_points, neutral_mesh_points) = wrap.selectPoints(scan_mesh, neutral_mesh, 
                                                                    pointsRight=neutral_mesh_points)
    else:
        (scan_mesh_points, neutral_mesh_points) = wrap.selectPoints(scan_mesh, neutral_mesh)
    wrap.savePoints(scan_mesh_points, scan_mesh_points_path)        
    wrap.savePoints(neutral_mesh_points, neutral_mesh_points_path)