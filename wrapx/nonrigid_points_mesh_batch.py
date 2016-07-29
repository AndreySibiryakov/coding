import wrap
import os

'''
path = wrap.openFileDialog()
target_scan_dir = os.path.dirname(path) + "/"
print 'choosed dir - ' + target_scan_dir'''

target_scan_dir = 'd:/Cthulhu/3d_scanning/Leha_phomens/selected_result/aligned/'
uni_topo_mesh_polygons_mask_path = 'd:/Cthulhu/3d_scanning/Leha_phomens/selected_result/aligned_nonrigid_transfer/mother_polygons.txt'


def get_file_path(name, mesh_list, type = 'obj'):  
    for mesh_name in mesh_list:  
        if name + '.' + type in mesh_name:  
            print 'got ' + name + '.' + type  
            return mesh_name  
 
def generate_points_name(name, target_scan_dir, prefix='_nonrigid'):  
    file_name = target_scan_dir + name + prefix + '.points'
    return file_name

def generate_universal_topology_name(name, target_scan_dir, prefix='_uni'):  
    file_name = target_scan_dir + name + prefix # + '.obj'
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
        scan_names_list.remove('neutral')  
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

for scan_name in scan_names: 
    uni_topo_name = 'neutral'
    uni_topo_mesh = get_file_path(uni_topo_name, scan_files_list, type = 'obj')  
    uni_topo_mesh_texture = get_file_path(uni_topo_name, scan_files_list, type = 'jpg')  
    uni_topo_mesh_points_path = generate_points_name(uni_topo_name, target_scan_dir, prefix='_nonrigid')
    uni_topo_mesh = wrap.Geom(uni_topo_mesh)  
    uni_topo_mesh.wireframe = False  
    uni_topo_mesh.texture = wrap.Image(uni_topo_mesh_texture)  
    uni_topo_mesh.texture.show()  

    scan_mesh = get_file_path(scan_name, scan_files_list, type = 'obj')  
    scan_mesh_texture = get_file_path(scan_name, scan_files_list, type = 'jpg')  
    scan_mesh_points_path = generate_points_name(scan_name, target_scan_dir, prefix='_nonrigid')
    scan_uni_topo_path = generate_universal_topology_name(scan_name, target_scan_dir, prefix='_uni')
    scan_mesh = wrap.Geom(scan_mesh)  
    scan_mesh.wireframe = False  
    scan_mesh.texture = wrap.Image(scan_mesh_texture)  
    scan_mesh.texture.show()  
    #scan_mesh_points = wrap.selectPoints(scan_mesh)
    if os.path.isfile(neutral_mesh_points_path) == True:
        if os.path.isfile(scan_mesh_points_path) == True:
            uni_topo_mesh_mesh_points = wrap.loadPoints(uni_topo_mesh_points_path)
            scan_mesh_points = wrap.loadPoints(scan_mesh_points_path)
            uni_topo_mesh_polygons_mask = wrap.selectPolygons(uni_topo_mesh_polygons_mask_path)
            scan_mesh = wrap.nonRigidRegistration(uni_topo_mesh, scan_mesh,
                                            uni_topo_mesh_mesh_points, scan_mesh_points,
                                            uni_topo_mesh_polygons_mask,
                                            minNodes = 15, #changed from 15
                                            initialRadiusMultiplier = 1.0, # changed from 1
                                            # smoothnessInitial = 0.1,
                                            smoothnessFinal = 0.1, # changed from 1
                                            maxIterations = 20) # changed from 30
            #
#            uni_topo_mesh.texture = wrap.transferTexture(scan_mesh, scan_mesh.texture,
#                                                    uni_topo_mesh,
#                                                    (2048,2048),
#                                                    maxRelativeDist = 3)
#            uni_topo_mesh.texture.extrapolate()
            #
            uni_topo_mesh.save(scan_uni_topo_path)
#            uni_topo_mesh.texture.save(scan_uni_topo_path)
