import threading
from mem_main import main as DME_read_main

# Args for DME_read_main:
# Arg 0: Toggle between overlay-style and machine-friendly output
# Arg 1: Amount of times the output is refreshed every second
mem_thread = threading.Thread(target=DME_read_main, args=(False, 60))
mem_thread.start()

