import os                                          # file ka folder nikalne ke liye
import numpy as np                                 # NumPy: image = array
import cv2                                         # OpenCV

HERE = os.path.dirname(os.path.abspath(__file__))  # is script ka folder (chapter03/)

# ===== EASY: on a white 400×400 image draw a green filled circle in the centre and the text "BOT" under it. =====
img = np.full((400, 400, 3), 255, np.uint8)        # safed (white) image: har pixel = 255, 3 channels (BGR)

# circle(image, centre (x, y), radius, colour BGR, thickness)
cv2.circle(img, (200, 200), 100, (0, 255, 0), -1)  # -1 = andar se bhar do (filled); BGR mein (0,255,0) = green

# putText ka (x, y) = text ka BOTTOM-LEFT corner hai, centre nahi
cv2.putText(img, "BOT", (168, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)  # x=168 -> text ka middle ~200

cv2.imshow("Image", img)                           # window kholo
cv2.waitKey(0)                                     # key dabane tak ruko
cv2.destroyAllWindows()                            # window band

# ===== MEDIUM: draw a closed outline of a trapezoid with corners (100,100), (300,100), (350,250), (50,250) on a black 1-channel mask, thickness 2. Print np.unique. =====
mask = np.zeros((400, 400), np.uint8)              # kaala (black) mask: sirf (height, width), 1 channel
corners = np.array([[100, 100], [300, 100], [350, 250], [50, 250]], np.int32)  # (x, y) points, int32 zaroori

# isClosed=True -> last point (50,250) ko first point (100,100) se jodta hai (4th edge)
cv2.polylines(mask, [corners], isClosed=True, color=255, thickness=2)  # 1 channel -> colour sirf ek number

# my guess: [  0 255]  -> 0 = background, 255 = lines (clean mask mein sirf yahi 2 values)
print("np.unique(mask) =", np.unique(mask))

cv2.imshow("Trapezoid Mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ===== ROBOT TASK: on arena.png, draw a red arrow from the image centre to the orange trapezoid (about (1028, 264)) and write the distance in pixels next to it. (Hint: math.hypot(dx, dy).) =====
arena_path = '/home/gagan/robotics-learning/opencv_robotics_course/code/data/arena.png'  # full path, sirf naam nahi
arena = cv2.imread(arena_path)                     # arena.png padho (BGR)
if arena is None:                                  # file na mile to imread None deta hai, error nahi
    raise SystemExit(f"Image nahi mili: {arena_path}")

h, w = arena.shape[:2]                             # shape = (height, width, channels)
center = (w // 2, h // 2)                          # (x, y) = (width/2, height/2) -> (640, 360)
target = (1028, 264)                               # orange trapezoid ke kareeb

cv2.arrowedLine(arena, center, target, (0, 0, 255), 5)  # red arrow (BGR): centre se target tak

dx = target[0] - center[0]                         # x mein kitna door (388)
dy = target[1] - center[1]                         # y mein kitna door (-96, upar ki taraf)
distance = round(np.hypot(dx, dy))                 # sqrt(dx² + dy²) = 399.7 -> round = 400 (int() 399 deta)
print("distance =", distance, "px")

mid = ((center[0] + target[0]) // 2, (center[1] + target[1]) // 2)  # arrow ka beech wala point
cv2.putText(arena, f"{distance} px", (mid[0] - 60, mid[1] + 80),     # arrow ke neeche likho (trapezoid se door)
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

out_path = os.path.join(HERE, 'arena_arrow.png')   # chapter03/ mein save karo, chahe kahin se bhi run karo
cv2.imwrite(out_path, arena)
print("Saved", out_path)

cv2.imshow("Arena with Arrow", arena)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ===== MY MISTAKES =====
# 1. cv2.imread("arena.png") -> sirf file ka naam diya, file us folder mein nahi thi -> None mila
#    -> arena.shape pe crash (AttributeError: 'NoneType'). Hamesha full path + `if img is None` check.
# 2. int(399.7) = 399 -> int() decimal kaat deta hai, round nahi karta. Sahi value ke liye round().
# 3. cv2.putText() origin: Pehle org ko top-left samjha, lekin ye text ka bottom-left anchor point hota hai.
# 4. Polygon coordinates: Pehle points aur image dimensions ko lekar confusion tha. Polygon ke liye points
#    (x, y) order mein aur np.int32 format mein dene hote hain.
# 5. Mask dimensions: Saare polygon points image ke andar hone chahiye. Height aur width ka dhyan rakho.
# 6. Binary mask: cv2.LINE_AA anti-aliasing ke kaaran intermediate grey pixel values create kar sakta hai
#    (trapezoid pe 33 values aayi!) -> mask ke liye mat use karo.
# 7. Original image preservation: Agar original image ko unchanged rakhna hai, toh drawing se pehle img.copy() use karo.
# 8. Filled vs outline shapes: Thickness -1 shape ko fill karta hai; positive thickness sirf outline draw karta hai.
# 9. Image mein y NEECHE badhta hai (maths graph ka ulta). Isliye centre se upar wala point -> dy negative (-96).
# 10. arrowedLine(img, start, end): tip hamesha END pe banta hai. start/end swap -> arrow ulta.
