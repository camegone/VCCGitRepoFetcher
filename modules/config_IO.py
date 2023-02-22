import os
import subprocess

#default path for config should exist
default_path = "repofetcher.cnf"
#read function. returns list of config or None
def get_lines(path=default_path):
    if os.path.isfile(path):
        config = list()
        with open(path, mode='r') as f:
            #get a config per a line
            lines = [i.strip() for i in f.readlines()]
            #first line is string VCC_path
            config.append(lines[0])
            #second line is int fetch_interval
            interval = int(lines[1])
            interval = interval if interval > 0 else None
            config.append(interval)
        return config
    else:
        return None

def is_exist(path=default_path):
    if get_lines(path) is not None:
        return True
    else:
        return False

def get_VCC_path(path=default_path):
    VCC = get_lines(path)
    VCC = VCC[0]
    return VCC

def get_interval(path=default_path):
    interval = get_lines(path)
    interval = interval[1]
    return interval

def is_auto_fetch(path=default_path):
    if get_interval(path) is not None:
        return True
    else:
        return False

def is_init(path=default_path):
    if not is_exist(path):
        print("Config not found. Lauch setup...")
        subprocess.run(["python", "setup.py"])

#write function.
def save(config, path=default_path):
    with open(path, mode='w') as f:
        #write a config per a line
        f.write('\n'.join(config))