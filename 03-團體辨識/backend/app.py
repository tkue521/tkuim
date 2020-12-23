from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from io import BytesIO
from PIL import Image
import re, base64
from imutils.video import VideoStream
from imutils.video import FPS
from random import randint
import face_recognition, argparse, imutils, pickle, time, cv2, platform


app = Flask(__name__)

# Adding Cross Origin Resource Sharing to allow requests made from the front-end
# to be successful.
CORS(app)

##########################################################
# Menu of loaded groceries, and their respective prices. #
##########################################################


students = {'name' : {
    '406500578':'閆立中',
    '609450100':'葉欲晟'
    }
}

##################################################
# Utilities
##################################################
print('Loading Model...')
#G Read the graph definition file
data = pickle.loads(open('./encodings.pickle', "rb").read())
detector = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
print('Done.')

def getFrameFromBase64(uri):
    """ Convert image from a base64 bytes stream to an image. """
    base64_data = re.sub(b'^data:image/.+;base64,', b'', uri)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    image = Image.open(image_data)
    img = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
    # print(type(img))
    # frame = np.asarray(bytearray(byte_data), dtype="uint8")
    # frame = imutils.resize(frame, width=500)
    return img

##################################################
# REST API Endpoints For Web App
##################################################


@app.route('/')
def homepage():
    return 'This backend serves as a REST API for the React front end. Try running npm start from the self-checkout folder.'


@app.route('/detection', methods=['POST'])
def detection():
    request.get_data()
    
    # Load in an image to object detect and preprocess it
    img_data = getFrameFromBase64(request.data)
    gray = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(img_data, cv2.COLOR_BGR2RGB)

    # detect faces in the grayscale frame
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    # OpenCV returns bounding box coordinates in (x, y, w, h) order
    # but we need them in (top, right, bottom, left) order, so we
    # need to do a bit of reordering
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    # compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(rgb, boxes)
    IDs = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
            encoding, tolerance=0.46)
        ID = ""

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIds = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIds:
                ID = data["names"][i]
                counts[ID] = counts.get(ID, 0) + 1

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            ID = max(counts, key=counts.get)
        
        # update the list of student IDs
        IDs.append(ID)

    studentList=[]

    for i in range(len(IDs)):
        new_student = {}
        student_ID = str(IDs[i])
        student_name = students['name'][student_ID]
        new_student = { 'Id': student_ID, 'Name': student_name }
        studentList.append(new_student)
           
    print("Results are: ")
    print(len(studentList))
    print(studentList)
    return jsonify(studentList)


##################################################
# Starting the server
##################################################


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
