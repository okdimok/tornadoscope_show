import os, sys
from time import sleep
file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, file_path)
sys.path.insert(0, file_path + "/..")
sys.path.insert(0, file_path + "/../svetlitsa_virtualenv/Lib/site-packages")
parent_path = os.path.dirname(file_path)

# print(sys.path)

def scripts_path(): return file_path

def get_default_ip():
    return "192.168.123.59"

def sleep_show(secs):
    print(f"Waiting for {secs} seconds")
    for _ in range(secs):
        sleep(1)
        print(".", end="", flush=True)
    print("", flush=True)
