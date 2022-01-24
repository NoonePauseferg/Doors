import cv2 as cv
import numpy as np

def frame_conversion(img, x):
    return cv.resize(img, (img.shape[1]//x, img.shape[0]//x))

def find_corners_on_img(img):
    gray = np.float32(cv.cvtColor(img, cv.COLOR_BGR2GRAY))
    coordinates = cv.cornerHarris(gray,2,3,0.04)
    #dst = cv.dilate(coordinates, None)
    img[coordinates>0.01*coordinates.max()]=[0,0,255]


if __name__ == "__main__":
    cap = cv.VideoCapture('right.mp4')
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            frame = frame_conversion(frame, 3)
            find_corners_on_img(frame)
            cv.imshow("Door", frame)
            cv.moveWindow("Door", 710,-300)

        if cv.waitKey(25) & 0xFF == ord('q'):
             break

    cap.release()
    cv.destroyAllWindows()
