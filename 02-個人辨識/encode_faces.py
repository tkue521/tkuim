# 用法
# 若在筆電、桌機、雲端上運算 (較慢、比較準確):
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method cnn
# 若在Raspberry Pi上運算 (較快、比較不準確):
# python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog

# 匯入必要的套件
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# 設定引數說明
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=False, default="/Volumes/MacBackup/PyImageSearch/pi-face-recognition/dataset",
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=False, default="/Volumes/MacBackup/PyImageSearch/pi-face-recognition/pr_encodings.pkl",
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# 取得影像資料集的資料夾路徑
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))

# 初始化已知編碼、已知名稱列表
knownEncodings = []
knownNames = []

# 循環影像路徑
for (i, imagePath) in enumerate(imagePaths):
	# 從路徑中分離出名稱
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	# 載入影像並將其從OpenCV的RGB順序轉成dlib的RGB順序
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# 檢測影像裡的臉部邊界框的(x, y)座標
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])

	# 計算每個邊界框的臉部嵌入 <- 可以 Google "facial embeddings"
	encodings = face_recognition.face_encodings(rgb, boxes)

	# 循環每個臉部嵌入
	for encoding in encodings:
		# 將編碼和名稱加入已知列表
		knownEncodings.append(encoding)
		knownNames.append(name)

# 把已知列表存回硬碟裡
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()