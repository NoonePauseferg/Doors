import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def frame_conversion(img, x):
    return cv.resize(img, (img.shape[1]//x, img.shape[0]//x))

def find_corners_on_img(img):
    gray = np.float32(cv.cvtColor(cv.dilate(img, np.ones((5,5))), cv.COLOR_BGR2GRAY))
    #gray = cv.GaussianBlur(gray, (7,7), 1)
    gray = cv.Canny(np.uint8(gray),100,200)
    coordinates = cv.cornerHarris(gray,2,3,0.04)
    dst = cv.dilate(coordinates, None)
    img[dst>0.01*dst.max()]=[0,0,255]


def try_floodfill(img, startPixel):
    mask = np.zeros((img.shape[0]+2, img.shape[1]+2), np.uint8)
    diff = (2,2,2)
    retval = cv.floodFill(img, mask, startPixel, (255,255,255), diff,diff)

def try_goodFeatures(img):
    corners = np.int0(cv.goodFeaturesToTrack(cv.cvtColor(img[0:100,0:100],cv.COLOR_BGR2GRAY), 6, 0.1, 2))
    for i in corners:
        x,y = i.ravel()
        cv.circle(img,(x,y),5,(0,0,255),-1)
    return corners

if __name__ == "__main__":
    corn, dist = [], []
    cap = cv.VideoCapture('left.mp4')
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            frame = cv.blur(frame_conversion(frame, 3), (2,2))
            gf = try_floodfill(frame, (53,375))
            print(np.sum(frame))
            if np.sum(frame) < 109010000:
                print("open")
            else:
                print("closed")
            cv.imshow("Door", frame)
            cv.moveWindow("Door", 710,-300)
        if cv.waitKey(25) & 0xFF == ord('q'):
             break

    cap.release()
    cv.destroyAllWindows()

