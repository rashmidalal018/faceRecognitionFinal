import os
import cv2
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancesystem-243a6-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendancesystem-243a6.appspot.com"
})

bucket = storage.bucket()

# boilerplate template for running a webcam

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# for importing all the image in our mode folder into list
folderModePath = "C:/Users/hp/Desktop/face/Resources/Modes"
# Check if the directory exists
if not os.path.exists(folderModePath):
    print(f"Error: Directory '{folderModePath}' not found.")
    exit()

modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

#Load the encoding file 
print("Loading Encoded File ....")
file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)    #only for testing
print("Encoded file loaded....")

modeType = 0
counter = 0
id = -1
imgStudent = []
while True:
    success, img = cap.read()
    # for overlapping webCam and background image
    
    imgS = cv2.resize(img, (0,0),None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceCurrFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS,faceCurrFrame)

    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

    if faceCurrFrame:  # if face is detecting in the frame 

        for encodeFace, faceLoc in zip(encodeCurrFrame,faceCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            # print("matches",matches)   #this will give the array for how much particular face matches with others
            # print("faceDis",faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index",matchIndex)

            if(matches[matchIndex]):
                # print("Known Face Detected")
                # print(studentIds[matchIndex])

                #rectange around face
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55+x1,162+y1,x2-x1,y2-y1
                imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
                
                id = studentIds[matchIndex]
                
                if counter == 0:
                    cvzone.putTextRect(imgBackground,"Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
        
            # else:
            #     print("No face matched")
            
        if counter != 0:
            if counter == 1:
                # get the data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                # get the image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # update data of attendence
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                "%Y-%m-%d %H:%M:%S")
                
                secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:   
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                # if marking attendence before time it will not be marked
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2
                imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

                if counter<=10:
                    # for adding attendence
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']),(861,125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
                    
                    cv2.putText(imgBackground, str(studentInfo['major']),(1006,550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
                    
                    cv2.putText(imgBackground, str(id),(1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
                    
                    cv2.putText(imgBackground, str(studentInfo['standing']),(910,625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                    
                    cv2.putText(imgBackground, str(studentInfo['year']),(1025,625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                    
                    cv2.putText(imgBackground, str(studentInfo['starting_year']),(1125,625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                    
                    # to put name into centre
                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']),(808+offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,50), 1)

                    # imgBackground[175:175+216, 909:909+216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

    # else no face is detected it will set modetype 
    else:
        modeType = 0
        counter = 0 
    # cv2.imshow('Face WebCam', img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
