import glob
import os
import subprocess
import shutil
import stat
import re

import VCC_conf_IO
import repo_data
import gitop

#ref: https://docs.python.org/ja/3/library/shutil.html#rmtree-example
def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)

repo_paths = glob.glob("repos\\*\\")
home_path = os.getcwd() + "\\"
print("home: " + home_path)

for path in repo_paths:
    os.chdir(home_path + path)
    print("current: " + os.getcwd())
    no_tag = False
    
    #load config
    url = repo_data.get_url()
    branch = repo_data.get_branch()
    package_path = repo_data.get_path()
    ignore_past = repo_data.get_ignore_past()
    
    #print("get tags...")
    tags = gitop.get_remote_tags()
    #print(tags)
    if len(tags) == 0:
        print("tags are not set. get remote hash instead...")
        no_tag = True

    if no_tag:
        tags = gitop.get_latest_hash()
        print(tags)
    
    if ignore_past:
        tags = tags[-1:] #get only the last element
    
    tags_cloned = repo_data.get_cloned()
    tags = sorted( list( set(tags) - set(tags_cloned) ) ) #get tags not cloned yet
    if len(tags) == 0:
        continue
    
    print("cloning: ")
    print(tags)
    
    paths_verified = list()
    #clone each versions
    for tag in tags:
        if no_tag:
            subprocess.run(['git', 'clone', url, tag])
        else:
            subprocess.run(['git', 'clone', '-b', tag, url, tag])#clone in a dir named after the tag name
        print("verify " + tag)
        pkg_path =glob.glob(tag+"\\**\\package.json", recursive=True)
        verified = True if len( pkg_path ) > 0 else False
        print(glob.glob(tag+"\\**\\package.json", recursive=True))
        print("OK" if verified else "NG")
        if verified:
            ver_path = re.sub(r'\\package\.json$', '', pkg_path[0])
            paths_verified.append(home_path + path + ver_path)
        else:
            print("this version is not VPM compatible. delete it...")
            shutil.rmtree(tag, onerror=remove_readonly)
            
    print("Add these paths to VCC")
    print(paths_verified)
    VCC_conf_IO.add_package(paths_verified)

    #update list of versions
    with open("clones.lis", mode='a') as f:
        f.write('\n'.join([""] + tags))