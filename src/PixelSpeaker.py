import pyautogui
import time

# doc
# https://pyautogui.readthedocs.io/en/latest/

# ----------------
# | 0,0       n,0 |
# |    screen     |
# | 0,n       n,n |
# ----------------

# === CONFIG ===
screenWidth, screenHeight = pyautogui.size()
safezone_setting = 0 #todo, int

if round(screenWidth / screenHeight, 2) != round(16/9, 2):
    print("Your aspect ratiois currently not supported, configure manually")
    arrow_pixel_pos = (137, 1024)  # <- MANUALLY Replace with your player arrow's screen position
else: 
    # Assuming these are for 1920/1080, assumes the same safezone
    # Will not work if the safezone is different than the orignal ones, but lets not deal with that logic for now
    x = (137 / 1080) * screenWidth
    y = (1024 / 1920) * screenHeight
    arrow_pixel_pos = (x, y)

check_interval = 0.1  # Seconds between checks
seen_colors = set()

try:
    while True:
        r, g, b = pyautogui.pixel(*arrow_pixel_pos)
        color = (r, g, b)

        if color not in seen_colors:
            seen_colors.add(color)
            print(color)

        time.sleep(check_interval)
except KeyboardInterrupt:
    print("Stopped.")
