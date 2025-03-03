import time
import sys 

idx = 0
while True:
    print(f"from tool 1 - line {idx}")
    idx += 1
    sys.stdout.flush()
    time.sleep(0.1)

