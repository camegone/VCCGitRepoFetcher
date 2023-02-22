import os
import subprocess
import re
import modules.config_IO as config_IO

repo_prefix="repos\\"

#check if config is exist
if not config_IO.is_exist():
    print("Config not found. Lauch setup...")
    subprocess.run(["python", "redo_setup.py"])

#ask name of repo wanna create
name = input("What the name do you want to add?")
#check if it already exist in subdirectory
repodir = repo_prefix + name
if os.path.isdir(repodir):
    print("error: Specified name is already exist.")
else:
    print("Create repo on: " + repodir)
    os.mkdir(repodir)
    repoconf = list()
    repoconf.append("--version")
    repoconf.append("1")
    url = ''
    #get url
    args = input("Enter URL...")
    args = args.split()
    branch = False
    branch_name = ''
    #parse args
    for a in args:
        if branch:
            branch_name = a
            branch = False
        if a.startswith('http'):
            url = a
        if a.startswith('-b'):
            branch = True
    #get branch name from UPM link
    url = url.split('#')
    print(url)
    if len(url) > 1:
        branch_name = url[1]
    url_raw = url[0]
    #get UPM package.json path
    url = re.sub(r'\?path=.*', '', url_raw)
    pack_path = re.sub(url, '', url_raw )
    #write down
    repoconf.append("--url")
    repoconf.append(url)
    repoconf.append("--branch")
    repoconf.append(branch_name)
    repoconf.append("--path")
    repoconf.append(pack_path)
    
    confirm = input("Ignore past releases? [y/n]")
    confirm = False if re.match("n|N", confirm) is not None else True #default off
    repoconf.append("--fetchmode")
    if confirm:
        repoconf.append("IgnorePast")
    else:
        repoconf.append("GetAll")
    
    os.chdir(repodir)
    subprocess.run(['git', 'init'])
    subprocess.run(['git', 'remote', 'add', 'origin', repoconf[3]])
    with open("repo.cnf", mode='w') as f:
        f.write('\n'.join(repoconf))
    with open("clones.lis", mode='w') as f:
        f.write('')

#end
input("Hit enter key...")