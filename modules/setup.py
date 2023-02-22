import os
import re

import modules.config_IO as config_IO

config = list()

#check default data directory
appdata = os.environ["APPDATA"]
appdata = appdata.replace(r"\Roaming", r"\Local\VRChatCreatorCompanion")
is_VCC_found = os.path.isdir(appdata)
print("VCC " + ("found." if is_VCC_found else "not found.") )

#ask VRC Creator Companion installation path
while len(config) == 0:
    if is_VCC_found:
        confirm = input(appdata + " < set here as VCC data path? [y/n]")
        confirm = True if re.match("y|Y", confirm) is not None else False
        if confirm:
            #add config
            config.append(appdata)
            continue

    appdir = input("Enter the VCC data path...")
    if os.path.isdir(appdir):
        config.append(appdir)
    else:
        print("error: invalid directory")
        
#ask if auto fetch
while len(config) == 1:
        confirm = input("Enable auto fetch? [y/n]")
        confirm = True if re.match("y|Y", confirm) is not None else False
        if confirm:
            duration = input("Enter auto fetch interval minutes (whole number):")
            if duration.isdigit():
                config.append(duration)
            else:
                print("error: please enter a whole number...")
                continue
        
        else:
            config.append("-1")
            
#save config
config_IO.save(config)