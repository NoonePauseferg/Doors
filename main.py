import cv2 as cv
import numpy as np


def frame_conversion(img, x):
    return cv.resize(img, (img.shape[1]//x, img.shape[0]//x))

def find_corners_on_img(img):
    """
    Parameters: img - np.ndarray
    -> detecting and rendering angles in an image
    """
    gray = np.float32(cv.cvtColor(cv.dilate(img, np.ones((5,5))), cv.COLOR_BGR2GRAY))
    gray = cv.Canny(np.uint8(gray),100,200)
    coordinates = cv.cornerHarris(gray,2,3,0.04)
    dst = cv.dilate(coordinates, None)
    img[dst>0.05*dst.max()]=[0,0,255]


def try_floodfill(img, startPixel):
    """
    Parameters: img - np.ndarray
                startPixel - tupl (x,y) coordinates

    -> a function that, like a fill, searches for an area around a specified point
       in which the color scheme of the image is similar and without borders
    """
    mask = np.zeros((img.shape[0]+2, img.shape[1]+2), np.uint8)
    diff = (2,2,2)
    cv.floodFill(img, mask, startPixel, (0,255,0), diff,diff)
    frame[frame < 255] = 0
    if np.sum(img) < 4772835:
        print("open")
    else:
        print("closed")

def try_inRange(img):
    """"
    Parameters: img - np.ndarray

    -> unction, which find image sections in exactly diapason of colors,
       work badly~
    """
    up = np.array([164,163,158])
    low = np.array([115,113,109])
    mask =  cv.inRange(img, low, up)
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    for contor in contours:
        area = cv.contourArea(contor)
        if area > 13000:
            print(area)
            cv.drawContours(img, contor, -1, (0,255,0),3)
        


if __name__ == "__main__":
    corn, dist = [], []
    cap = cv.VideoCapture('smth.mp4')
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            frame = cv.blur(frame_conversion(frame, 3), (1,1))
            try_floodfill(frame, (220,340))
            find_corners_on_img(frame)
            cv.imshow("Door", frame)
            cv.moveWindow("Door", 710,-300)
        if cv.waitKey(25) & 0xFF == ord('q'):
             break

    cap.release()
    cv.destroyAllWindows()

