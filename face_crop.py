import cv2
import base64


def face_detection_crop(path):
    
    #converting input image to grayscale
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #load Haar cascade algorithm and detect faces in the picture
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
    ) 

    #highlited lines under the faces
    for (x, y, w, h) in faces:
        x-=10
        y-=30
        h+=50
        w+=16
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), 2)
        roi_color = image[y:y + h, x:x + w] 
        image=cv2.imwrite('./pictures/face.jpg', roi_color)
        with open('./pictures/face.jpg', "rb") as f:
            im_b64 = base64.b64encode(f.read())
        return im_b64
