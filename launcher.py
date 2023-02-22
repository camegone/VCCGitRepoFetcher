import subprocess
import time
import modules.process_check as process_check
import modules.config_IO as config_IO

interval = config_IO.get_interval()
while True:
    if process_check.is_name_running('CreatorCompanion'):
        print('VCC is running. please end it if you want to fetch...')
    else:
        print('launch fetcher')
        subprocess.run(['python', 'modules\\clonerepo.py'])
        print('fetch compleated')
    if interval is None:
        print('exit')
        break
    print('sleep ' + str(interval) + ' mins...')
    time.sleep(interval * 60)