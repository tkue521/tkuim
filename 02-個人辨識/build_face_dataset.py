# 匯入必要的套件
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os

# 設定引數說明
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
    help="path to where the face cascade resides")
ap.add_argument("-o", "--output", required=True,
    help="path to output directory")
args = vars(ap.parse_args())

# 載入Haar特徵串聯分類器
detector = cv2.CascadeClassifier(args["cascade"])
# 初始化影像串流並讓攝影機預熱
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# 若不是用usb網路攝影機，而是用樹梅派板的攝影機模組，註解掉上面那一行並反註解下面這一行
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
total = 0

# 循環影像串流的每一個影格
while True:
    # 取得影像串流中的影格並複製一份(以防萬一我們想存它的話)
    # 並調整大小以加速影像處理
    frame = vs.read()
    orig = frame.copy()
    frame = imutils.resize(frame, width=400)
    # 從灰階影格中偵測臉部
    rects = detector.detectMultiScale(
        cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1,
        minNeighbors=5, minSize=(30, 30))
    # 循環每個臉部辨識並加上辨識框
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 將影格顯示在螢幕上
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # 如果按下 `k` 則儲存當下影格
    if key == ord("k"):
        p = os.path.sep.join([args["output"], "{}.png".format(
            str(total).zfill(5))])
        cv2.imwrite(p, orig)
        total += 1
    # 如果按下 `q` 的話，停止串流
    elif key == ord("q"):
        break
# 印出總共儲存的影像及執行清理
print("[INFO] {} face images stored".format(total))
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()
    
