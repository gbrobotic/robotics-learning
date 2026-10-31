# ===== EASY: predict the OpenCV H of pure yellow (0, 255, 255), then check it with the 1×1 trick. =====
import cv2                                         # OpenCV 
import numpy as np                                 # NumPy  
yellow_bgr = np.uint8([[[0, 255, 255]]])            # pure yellow in BGR
yellow_hsv = cv2.cvtColor(yellow_bgr, cv2.COLOR_BGR2HSV  )  # convert to HSV
h, s, v = yellow_hsv[0, 0]                          # extract H
# my guess: H of pure yellow = 25
print(f"Predicted H of pure yellow = 25, actual H = {h}")
print(f"Predicted s of pure yellow = 255, actual s = {s}")
print(f"Predicted v of pure yellow = 255, actual v = {v}")

# ===== MEDIUM:Use the tuner (or the mouse inspector) to find a range for the green trapezoid only: not its vault, not the hexagon. Write your final numbers. =====
green_low  = np.array([50, 160, 130])    # H, S, V
green_high = np.array([70, 255, 255])

# ===== ROBOT TASK:Take a photo (phone or webcam) of 3 coloured objects on a table. Find an HSV range for each. Which one was hardest, and which channel solved it? =====
import os                                          # path banane ke liye
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')  # opencv_practice/data/

photo = cv2.imread(os.path.join(DATA, 'table_3objects.jpg'))    # original photo padho (1280 x 960)
if photo is None:                                  # file na mile to imread None deta hai, error nahi
    raise SystemExit("table_3objects.jpg nahi mili data/ mein")

small = cv2.resize(photo, None, fx=0.6, fy=0.6)    # 60% chhota: (WIDTH, HEIGHT) ki jagah scale do -> dono same ratio
print("photo.shape =", photo.shape, "-> small.shape =", small.shape)
cv2.imwrite(os.path.join(DATA, 'table_3objects_small.jpg'), small)  # chhoti copy save, original safe

# --- HSV ranges (tuner se mile, H S V order) ---
# Red ring: red hue circle ke dono end pe hai -> 2 ranges chahiye (0-10 aur 170-179)
red1_low,  red1_high  = np.array([0, 160, 55]),   np.array([10, 255, 255])    # red ka 0 wala end
red2_low,  red2_high  = np.array([170, 160, 55]), np.array([179, 255, 255])   # red ka 179 wala end
# Green strip: dark bluish green -> H ~78 (normal green 60 nahi), V kam (~58) -> V low bahut neeche
green_low, green_high = np.array([65, 60, 10]),   np.array([85, 255, 255])
# Blue cap: H ~107
blue_low,  blue_high  = np.array([102, 50, 40]),  np.array([115, 255, 255])

hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)       # BGR -> HSV
red_mask = cv2.inRange(hsv, red1_low, red1_high) | cv2.inRange(hsv, red2_low, red2_high)  # | = dono masks jodo
green_mask = cv2.inRange(hsv, green_low, green_high)  # range ke andar = 255, bahar = 0
blue_mask = cv2.inRange(hsv, blue_low, blue_high)
for name, m in [("red", red_mask), ("green", green_mask), ("blue", blue_mask)]:
    print(f"{name:5s} mask white pixels = {cv2.countNonZero(m)}")  # 0 aaye to range galat hai

# Hardest: middle wala green strip. H aur V ne solve kiya:
#   H -> uska H ~78 tha, normal green (55-65) wala range kaam nahi kiya
#   V -> strip dark hai (V ~58), isliye V low bahut kam (10) rakhna pada

# ===== MY MISTAKES =====
# Yellow ka H guess kiya 25 → asli 30. Rule: OpenCV H = degrees ÷ 2 (60° → 30).
#  (I guessed 25 for yellow's H, but it's 30, because OpenCV H = degrees ÷ 2.)
# Grey ka S = 255 socha → asli 0. Jab B = G = R → koi colour nahi → S = 0." (I thought grey had S = 255, but it's 0: when B = G = R there's no colour, so S = 0.)
# Red ring ke liye sirf 118–179 range diya → 1,126 pixels miss (H 0–10 wale). Red = hamesha 2 ranges." (For the red ring I used only 118–179, which missed 1,126 pixels with H 0–10. Red always needs 2 ranges.)