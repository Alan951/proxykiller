import schedule
import time
import threading
from disableproxy import DisableProxyTask

banner = '''
██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗██╗  ██╗██╗██╗     ██╗     ███████╗██████╗ 
██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝██║ ██╔╝██║██║     ██║     ██╔════╝██╔══██╗
██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ █████╔╝ ██║██║     ██║     █████╗  ██████╔╝
██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  ██╔═██╗ ██║██║     ██║     ██╔══╝  ██╔══██╗
██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   ██║  ██╗██║███████╗███████╗███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
                                                                v0.5          by Coke         
'''

task = DisableProxyTask()

print(banner)

def runTask():
    proxy, script = task.startTask()

    if not proxy: 
        print('[ProxyKiller]  - Proxy is dead.')
    if not script:
        print('[ScriptKiller] - Script is dead.')


def enterListening():
    while True:
        input()
        print('[ManualKiller]')
        runTask()
        

def init():
    runTask()
    
    schedule.every(2).minutes.do(task.startTask)

    threading.Thread(target=enterListening).start()
    
    while True:
        schedule.run_pending()
        time.sleep(1)

init()
