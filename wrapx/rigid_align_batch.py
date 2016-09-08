import os  

# êîñòûëü äëÿ âûáîðà ïàïêè (âûáèðàåì ëþáîé ôàéë èç íóæíîé íàì ïàïêè)
path = wrap.openFileDialog()
target_scan_dir = os.path.dirname(path) + "/"
print 'choosed dir - ' + target_scan_dir

def get_file_path(name, mesh_list, type = 'obj'):  
    for mesh_name in mesh_list:  
        if name + '.' + type in mesh_name:  
            print 'got ' + name + '.' + type  
            return mesh_name  
          
def get_rigid_aligned_name(file_path, type = 'obj'):  
    file_path_list = file_path.split('.obj')
    aligned_path = file_path_list[0] + '_aligned.obj'  
    return aligned_path  
  
def get_scan_names(scan_files_list):  
    scan_names_list = []  
    split_names_list = []  
    for path in scan_files_list:  
        split_path = path.split('/')  
        split_name = split_path[-1].split('.')  
        split_names_list.append(split_name[0])  
        
    scan_names_list = list(set(split_names_list))  
    scan_names_list.remove('neutral')  
    return scan_names_list  
     
# to do - add rule to ignore _aligned in path and to inform whether or not to process  
scan_files_list = [] 
for path, dirs, file_names in os.walk(target_scan_dir):
    for file_name in file_names:
        if not '_aligned' in file_name:
            full_file_path = os.path.join(path, file_name) 
            scan_files_list.append(full_file_path)
        else:
            print file_name + " not added to list"
scan_names = get_scan_names(scan_files_list)  

neutral_mesh = get_file_path('neutral', scan_files_list, type = 'obj')  
neutral_mesh_texture = get_file_path('neutral', scan_files_list, type = 'jpg')  
  
target_mesh = wrap.Geom(neutral_mesh)  
target_mesh.wireframe = False  
target_mesh.texture = wrap.Image(neutral_mesh_texture)  
target_mesh.texture.show()  

#  ïðîâåðêà íàëè÷èÿ òî÷åê íà íåéòðàë ìåøå è ñîçäàíèå + ñîõðàíåíèå â ñëó÷àå èõ îòñóòñòâèÿ
target_mesh_points_path = get_file_path('neutral', scan_files_list, type = 'txt')  
if not target_mesh_points_path:
    target_mesh_points = wrap.selectPoints(target_mesh)
    target_mesh_points_path = target_scan_dir + 'neutral.txt'
    print target_mesh_points_path
    wrap.savePoints(target_mesh_points, target_mesh_points_path)
 
for scan_name in scan_names:  
    scan_mesh = get_file_path(scan_name, scan_files_list, type = 'obj')  
    scan_mesh_texture = get_file_path(scan_name, scan_files_list, type = 'jpg')  
    scan_mesh_aligned = get_rigid_aligned_name(scan_mesh, type = 'obj')  
    scan_mesh_points = get_file_path(scan_name, scan_files_list, type = 'txt')
    base_mesh = wrap.Geom(scan_mesh)  
    base_mesh.wireframe = False  
    base_mesh.texture = wrap.Image(scan_mesh_texture)  
    base_mesh.texture.show()  
  # Çàãðóçêà, óñòàíîâêà, ñîõðàíåíèå òî÷åê äëÿ targetmesh è basemesh.
    if scan_mesh_points:
        (target_mesh_points, base_mesh_points) = wrap.selectPoints(target_mesh, base_mesh, wrap.loadPoints(target_mesh_points_path), wrap.loadPoints(scan_mesh_points))  
    else:
         (target_mesh_points, base_mesh_points) = wrap.selectPoints(target_mesh, base_mesh, wrap.loadPoints(target_mesh_points_path))   
    wrap.savePoints(target_mesh_points, target_mesh_points_path)
    base_mesh_points_path = target_scan_dir + scan_name + ".txt"
    wrap.savePoints(base_mesh_points, base_mesh_points_path)
         
    rigidTransformation = wrap.rigidAlignment(base_mesh,base_mesh_points,target_mesh,target_mesh_points,matchScale = True)  
    base_mesh.transform(rigidTransformation)  
    base_mesh.fitToView()  
  
    base_mesh.save(scan_mesh_aligned)  
    print 'saved', scan_mesh_aligned