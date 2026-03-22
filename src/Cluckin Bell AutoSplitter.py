import pyautogui
import time
import math
import keyboard
#=============================================================================================
print(f"Autosplitter made by deathrow")
print(f"Youtube @BD Deathrow")
print(f"Discord dea1hrow")
#=============================================================================================
split_key = 'F1'
pixel_pos = (137, 1024)

target_color_1 = (215, 215, 215)
target_color_2 = (168, 168, 168)
target_color_3 = (163, 205, 227)
target_color_4 = (144, 182, 200)
target_color_5 = (122, 154, 170)
target_color_6 = (174, 219, 242)

cutscene_colors = [
    (69, 78, 85), (72, 85, 93), (73, 88, 96), (70, 82, 89),
    (67, 74, 81), (63, 68, 74), (60, 62, 67), (58, 59, 65),
    (61, 63, 70), (63, 67, 74), (64, 69, 77), (67, 75, 83),
    (41, 47, 52), (12, 14, 15), (25, 32, 35), (48, 61, 67),
    (75, 95, 105), (102, 129, 142)
]

blacklist_colors = [
    (215, 211, 196),
    (228, 224, 205),
    (171, 176, 152),
    (132, 167, 184),
    (133, 167, 185),
    (132, 166, 182),
    (132, 166, 183),
    (134, 169, 187),
    (132, 166, 184),
    (134, 168, 186),
    (166, 166, 151),
    (163, 166, 151),
    (170, 174, 156),
    (134, 188, 186),
    (131, 166, 183),
    (131, 165, 182),
    (214, 210, 196),
    (229, 223, 207)
]

play_button_color = (240, 200, 80)
play_button_pos = [(554, 582), (554, 545)]
loading_color = (0, 0, 0)

threshold = 20
check_interval = 0.05
split_on_failed_amount = 5
split_cooldown_seconds = 30

failed_checks = 0
last_split_time = 0
in_loading_screen = False
first_split_done = False
No_fails = 0
Total_red = 0
Total_green = 0
Total_blue = 0

def color_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

def color_matches(c1, c2, threshold=20):
    return color_distance(c1, c2) <= threshold

def is_blacklisted(color):
    return color in blacklist_colors  # Exact match

def matches_any_target(color):
    return any(color_matches(color, target, threshold) for target in [
        target_color_1, target_color_2, target_color_3,
        target_color_4, target_color_5, target_color_6
    ])

# === NEW: Exact match cutscene detection + near-match logging ===
def matches_cutscene_color(color):
    if color in cutscene_colors:
        return True
    # Debug log for near matches
    for c in cutscene_colors:
        dist = color_distance(color, c)
        if 0 < dist <= threshold:
            print(f"⚠️ Near cutscene color match ({color}) — distance {dist:.1f} from {c}")
    return False

def wait_for_play_button():
    print("⌛ Waiting for Play button...")
    while True:
        for pos in play_button_pos:
            color = pyautogui.pixel(*pos)
            if color_matches(color, play_button_color, threshold):
                print(f"🎮 Play button detected at {pos}.")
                return
        time.sleep(check_interval)

def wait_for_hud():
    print("⌛ Waiting for HUD...")
    while True:
        color = pyautogui.pixel(*pixel_pos)
        if matches_any_target(color):
            print(f"✅ HUD detected.     - {color}")
            return
        time.sleep(check_interval)

# === STARTUP WAIT ===
wait_for_play_button()
wait_for_hud()
keyboard.press_and_release(split_key)
print("▶️ First split done. Autosplitter active.")
last_split_time = time.time()
first_split_done = True

# === MAIN LOOP ===
try:
    while True:
        current_color = pyautogui.pixel(*pixel_pos)

        if color_matches(current_color, loading_color, threshold):
            if not in_loading_screen:
                print("🕓 Loading screen detected. Pausing checks...")
            in_loading_screen = True
            time.sleep(check_interval)
            continue

        if in_loading_screen:
            if matches_any_target(current_color):
                print("✅ Loading finished. Resuming checks.")
                in_loading_screen = False
            else:
                time.sleep(check_interval)
                continue

        if matches_cutscene_color(current_color):
            print(f"🎬 Cutscene color detected ({current_color}) — pausing checks.")
            time.sleep(check_interval)
            continue

        # ✅ Handle blacklist first
        if is_blacklisted(current_color):
            print(f"- Color: {current_color} - BLACKLISTED 🟦 (ignored)")
            time.sleep(check_interval)
            Total_blue += 1
            continue

        # ✅ Match check
        if matches_any_target(current_color):
            failed_checks = 0
            No_fails += 1
            Total_green += 1
            print(f"- Color: {current_color} - MATCH ✅ Proceeding ✅ ({Total_green} ✅ / {Total_red} ❌ / 🟦 {Total_blue})")
        else:
            No_fails = 0
            failed_checks += 1
            Total_red += 1
            print(f"- Color: {current_color} - NO MATCH ❌ ({failed_checks}/{split_on_failed_amount})")

            if failed_checks >= split_on_failed_amount:
                now = time.time()
                if now - last_split_time >= split_cooldown_seconds:
                    keyboard.press_and_release(split_key)
                    print("✔️✔️ LiveSplit Has Been Split ✔️✔️")
                    last_split_time = now
                    failed_checks = 0

                    wait_for_play_button()
                    wait_for_hud()
                    keyboard.press_and_release(split_key)
                    print("▶️ New mission started. Split again.")
                    last_split_time = time.time()

        time.sleep(check_interval)

except KeyboardInterrupt:
    print("\n🛑 Stopped by user.")
    print(f"🧾 Final Stats: Matches ✅ {Total_green} | Fails ❌ {Total_red}")
