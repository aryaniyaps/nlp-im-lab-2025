import cv2
import numpy as np

img =  cv2.imread("09-simple-spatial-filters-27-02-2026/cameraman.tif", 0)
if img is None:
	raise FileNotFoundError("The image file 'cameraman.tif' was not found. Please check the file path.")

# 3 x 3 averaging filter
kernel = np.ones((3, 3), np.float32) / 9
lpf = cv2.filter2D(img, -1, kernel)
cv2.imshow("Low Pass Filter", lpf)
cv2.waitKey(0)
cv2.destroyAllWindows()
