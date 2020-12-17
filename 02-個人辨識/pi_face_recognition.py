# 指令用法
# python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle

# 匯入必要的套件
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import platform


# 設定引數說明
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
	help = "path to where the face cascade resides")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
args = vars(ap.parse_args())

# 載入處理過後的臉部資料集 + OpenCV的Haar特徵串聯分類器
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(args["encodings"], "rb").read())
detector = cv2.CascadeClassifier(args["cascade"])

# 初始化影像串流並讓攝影機預熱
print("[INFO] starting video stream...")
# if on raspberry pi use the pi camera
#if platform.system() == 'Linux':
#	vs = VideoStream(usePiCamera=True).start()
#else:
vs = VideoStream(src=0).start()

time.sleep(2.0)

# 開始FPS計數
fps = FPS().start()

# 循環影像串流的每一個影格
while True:
	# 取得影像串流中的影格並且調整大小至500px(為了加速影像處裡)
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	
	# 將影格從 (1) BGR 調整成灰接 (為了臉部「偵測」)
	#         (2) BGR 調整成 RGB (為了臉部「辨識」)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# 從灰階影格中偵測臉部
	rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)

	# OpenCV 回傳邊界框的座標順序為 (x, y, 寬, 高)
	# 但我們需要以 (上, 右, 下, 左) 的順序, 所以要做一些調整
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

	# 計算每個邊界框的臉部嵌入 <- 可以 Google "facial embeddings"
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []

	# 循環每個臉部嵌入
	for encoding in encodings:
		# 比對影格的臉部嵌入與我們先前處理好的臉部資料集
		matches = face_recognition.compare_faces(data["encodings"],
			encoding, tolerance=0.46)
		name = "Unknown"

		# 查看有沒有相符的
		if True in matches:
			# 將所有有符合的臉部資料集成一個字典
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# 取得最多符合數的配對作為結果
			name = max(counts, key=counts.get)
		
		# 將結果加入列表
		names.append(name)

	# 循環所有配對的臉部影格
	for ((top, right, bottom, left), name) in zip(boxes, names):
		# 畫上辨識框並標上名稱
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)

	# 將影格顯示到螢幕上
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# 如果按下 `q` 的話，停止串流
	if key == ord("q"):
		break

	# 更新 FPS 計數器
	fps.update()

# 停止計時器並顯示 FPS 資訊
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# 清理
cv2.destroyAllWindows()
vs.stop()
