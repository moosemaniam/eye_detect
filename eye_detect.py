#!/usr/bin/env python

import cv 
import cv2

def face_detect(imcolor):
  #  imcolor = cv.LoadImage('anush2.jpg') # input image
    haarFace = cv.Load('haarcascade_frontalface_default.xml')
    haarEyes = cv.Load('haarcascade_eye.xml')
    # running the classifiers
    storage = cv.CreateMemStorage()
    detectedFace = cv.HaarDetectObjects(imcolor, haarFace, storage)
    detectedEyes = cv.HaarDetectObjects(imcolor, haarEyes, storage)
    
    actual_faces=[]
    actual_eyes=[]
    # draw a green rectangle where the face is detected 
    # draw a purple rectangle where the eye is detected
    if detectedEyes:
     count=0
     for eye in detectedEyes:
         #Only detect eye if within face
         for face in detectedFace:
             if(eye[0][0] >= face[0][0]):
                 actual_eyes.append(eye)
   
   #Only actual face if , face has eye in it
     for face in detectedFace:
       eye_present=False
       for eye in actual_eyes:
            if((eye[0][0]>= face[0][0]) and  (eye[0][3]<= face[0][3])):
                eye_present = eye_present | True
        
       if(eye_present==True): 
           actual_faces.append(face)

     if detectedEyes:
         for eye in actual_eyes:
            cv.Rectangle(imcolor,(eye[0][0],eye[0][1]),
                       (eye[0][0]+eye[0][2],eye[0][1]+eye[0][3]),
                       cv.RGB(155, 55, 200),2)
     if detectedFace:
         for face in actual_faces:
           cv.Rectangle(imcolor,(face[0][0],face[0][1]),
                   (face[0][0]+face[0][2],face[0][1]+face[0][3]),
                   cv.RGB(155, 255, 25),2)
     
    cv.NamedWindow('Face Detection', cv.CV_WINDOW_AUTOSIZE)
    
    cv.ShowImage('Face Detection', imcolor) 

class Target:

    def __init__(self):
        self.capture = cv.CaptureFromCAM(0)
        #cv.NamedWindow("Target", 1)

    def run(self):
      # Capture first frame to get size
        frame = cv.QueryFrame(self.capture)
        frame_size = cv.GetSize(frame)
        color_image = cv.CreateImage(cv.GetSize(frame), 8, 3)

        while True:
            color_image = cv.QueryFrame(self.capture)
            face_detect(color_image)
            c = cv.WaitKey(7) % 0x100
            if c == 27:
                break

if __name__=="__main__":
    t = Target()
    t.run()
