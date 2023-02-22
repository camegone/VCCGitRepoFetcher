import subprocess

def is_name_running(name):
    tasks = subprocess.run(['tasklist'], capture_output=True, text=True).stdout
    tasks = tasks.split('\n')
    is_exist = False
    for t in tasks:
        if t.startswith(name):
            is_exist = True
    
    return is_exist