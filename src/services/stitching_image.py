import cv2
import imutils
import numpy as np

class StichingImage:
    def __init__(self, images):
        self.images = images
        self.read_image()
        self.stitcher = cv2.Stitcher_create()
    
    def stich_images(self):
        status, panorama = self.stitcher.stitch(self.images)
        if status == cv2.Stitcher_OK:
            stitched_image = cv2.copyMakeBorder(panorama, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))
            gray = cv2.cvtColor(stitched_image, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
            contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            areaOI = max(contours, key=cv2.contourArea)
            mask = np.zeros(gray.shape, dtype="uint8")
            x, y, w, h = cv2.boundingRect(areaOI)

            self.stitched_image = stitched_image[y:y+h, x:x+w]
            return self.stitched_image
        else:
            return None
        
    def read_image(self):
        self.images = [cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR) for image in self.images]
