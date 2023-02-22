import re

import config_IO

VCC_path = config_IO.get_VCC_path()
VCC_setting_path = VCC_path + "\\settings.json"
package_header = '  "userPackageFolders": ['
indent = 0
pkg_start = 0
pkg_end = 0
pkg_empty = False

def load():
    with open(VCC_setting_path, mode='r', encoding='utf-8') as f:
        #get a setting per a line
        lines = [i.rstrip() for i in f.readlines()]
    
    #print(lines)
    for i in range(0, len(lines)):
        if lines[i].startswith(package_header):
            global pkg_start
            pkg_start = i
            break
    
    folders = list()
    #pick each lines in userpackagefolders
    for i in range(pkg_start, len(lines)):
        if lines[i].endswith("],"):
            global pkg_end
            pkg_end = i
            break
        folders.append(lines[i].replace("\\\\", "\\"))
    
    global pkg_empty
    if pkg_start != pkg_end:
        pkg_start += 1
        pkg_end -= 1
        folders = folders[1:]
        pkg_empty = False
    else:
        pkg_empty = True
        
    
    global indent
    indent = ( len(lines[pkg_start]) - len( lines[pkg_start].lstrip() ) )
    if pkg_empty:
        indent += 2
    #print(indent)
    #print(folders)
    
    return folders
    
def filter_conflict(additions_list):
    before = load()
    VCC_registered = set()
    #print(indent)
    for b in before:
        b = b[indent+1:]
        if b.endswith('",'):
            b = b[:-2]
        else:
            b = b[:-1]
        
        #print(b)
        VCC_registered.add(b)
        
    safe_list = list()
    for a in additions_list:
        if a not in VCC_registered:
            safe_list.append(a)
            
    #print(safe_list)
    return safe_list
    
def add_package(additions_list):
    global pkg_empty
    global pkg_start
    global pkg_end
    global indent
    write_list = filter_conflict(additions_list)
    if len(write_list) == 0: #error handling
        return
    
    #get vcc conf
    with open(VCC_setting_path, mode='r', encoding='utf-8') as f:
        #get a setting per a line
        VCC_lines = [i.rstrip() for i in f.readlines()]
    
    #resolve empty list first
    if pkg_empty:
        VCC_lines[pkg_start] = package_header
        pkg_start += 1
        VCC_lines.insert(pkg_start, ' '*indent + '"' + write_list[0].replace("\\", "\\\\") + '"')
        pkg_end += 1
        write_list = write_list[1:]
        pkg_empty = False
    
    #len(write_list) > 0
    while len(write_list) > 0:
        if VCC_lines[pkg_end].endswith('"'):
            VCC_lines[pkg_end] = VCC_lines[pkg_end] + ','
            
        pkg_end += 1
        VCC_lines.insert(pkg_end, ' '*indent + '"' + write_list[0].replace("\\", "\\\\") + '"')
        write_list = write_list[1:]
    print(VCC_lines)
    
    with open(VCC_setting_path, mode='w', encoding='utf-8') as f:
        #write a config per a line
        f.write('\n'.join(VCC_lines))

#add_package(list('abcdefg'))