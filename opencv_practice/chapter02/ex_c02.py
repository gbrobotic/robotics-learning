import os                                          # file ka folder nikalne ke liye
import cv2                                         # OpenCV

HERE = os.path.dirname(os.path.abspath(__file__))  # is script ka folder (chapter02/)
IMG_PATH = '/home/gagan/robotics-learning/opencv_robotics_course/code/data/shapes.png'

img = cv2.imread(IMG_PATH)                         # image padho -> NumPy array (BGR)
if img is None:                                    # file na mile to imread None deta hai, error nahi
    raise SystemExit(f"Image nahi mili: {IMG_PATH}")

# ===== EASY: print the BGR value of the bottom-right pixel of shapes.png. (Hint: the last row is height - 1.) =====
h, w, ch = img.shape                               # shape = (height, width, channels)
print("img.shape =", img.shape)                    # (480, 640, 3)

bottom_right_pixel = img[h - 1, w - 1]             # PEHLE y (row), PHIR x (column); same as img[-1, -1]
b, g, r = bottom_right_pixel                       # ek pixel = 3 numbers -> B, G, R mein todo
print(f"bottom-right pixel -> B={b} G={g} R={r}")  # white = 255 255 255

# ===== MEDIUM: crop the blue circle from shapes.png (centre (520, 115), radius 55) and save it. Predict roi.shape before running. =====
cx, cy, radius = 520, 115, 55                      # circle ka centre (x, y) aur radius ('r' nahi, woh red hai)
# my guess: roi.shape = (110, 110, 3)  -> side = 2 * radius
roi = img[cy - radius:cy + radius, cx - radius:cx + radius]  # crop: img[y1:y2, x1:x2], end wala include NAHI
print("roi.shape =", roi.shape)                    # (110, 110, 3)

out_path = os.path.join(HERE, 'blue_circle.png')   # chapter02/ mein save karo, chahe kahin se bhi run karo
cv2.imwrite(out_path, roi)                         # True return karta hai agar save hua
print("Saved", out_path)

# ===== ROBOT TASK: load arena.png, cut it into a left half and a right half with slicing, and save both. Print both shapes. (Hint: w // 2.) =====
arena_path = '/home/gagan/robotics-learning/opencv_robotics_course/code/data/arena.png'
arena = cv2.imread(arena_path)                      # arena.png padho
if arena is None:                                   # file na mile to imread None deta hai, error nahi
    raise SystemExit(f"Image nahi mili: {arena_path}")
h, w, ch = arena.shape                              # shape = (height, width, channels)
print("arena.shape =", arena.shape)                 # (720, 1280, 3)
left_half = arena[:, :w // 2]                       # left half: all rows, first half of columns
right_half = arena[:, w // 2:]                      # right half: all rows, second half of columns
print("left_half.shape =", left_half.shape)         # (720, 640, 3)
print("right_half.shape =", right_half.shape)       # (720, 640, 3)
left_path = os.path.join(HERE, 'arena_left.png')    # chapter02/mein save karo, chahe kahin se bhi run karo
right_path = os.path.join(HERE, 'arena_right.png')  # chapter02/mein save karo, chahe kahin se bhi run karo
cv2.imwrite(left_path, left_half)                   # True return karta hai agar save hua
cv2.imwrite(right_path, right_half)                 # True return karta hai agar save hua
print("Saved", left_path, "and", right_path)

# ===== MY MISTAKES =====
# 1. b, g, r = img.shape(-1)  -> GALAT. shape attribute hai, function nahi (no brackets).
#    Aur shape image ka SIZE batata hai, pixel ka colour nahi. Sahi: pixel = img[y, x]; b, g, r = pixel
# 2. pixel.shape socha [255 255 255] dega -> GALAT. (3,) deta hai = 3 numbers hain. Values ke liye print(pixel)  ||  pixel.shape agar pixel ek NumPy array hai, toh (3,) return karega — ye shape batata hai, BGR values nahi.
# 3. img[479, 640] socha kuch nahi hoga -> IndexError! width 640 hai to x sirf 0..639. Counting 0 se hoti hai.
# 4. img[465:575, 60:170] socha error aayega -> error NAHI aata. Slice image ke bahar jaye to NumPy chupchap
#    kaat deta hai -> (15, 110, 3), galat crop. Isliye hamesha [y, x] order check karo aur shape print karo.
# 5. cv2.imwrite('file.png') -> jis folder se run kiya wahan save hota hai, script ke folder mein nahi.
#    Fix: os.path.join(HERE, 'file.png')
# 6. print(...) ko # ke BAAD likh diya -> woh comment ban gaya, chala hi nahi. # ke baad sab ignore hota hai.
# 7. Comment mein shape guess karke likha (480, 320, 3) -> galat, woh shapes.png ka size tha, arena.png ka nahi.
#    Pehle run karo, phir comment mein sahi value likho.
# 8. img[:, ::-1] ->::-1 ulta karta hai (reverses), kaat-ta nahi (doesn't cut). Slot 1 = rows, slot 2 = columns.