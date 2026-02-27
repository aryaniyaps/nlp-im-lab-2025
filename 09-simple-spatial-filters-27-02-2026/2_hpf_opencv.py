import cv2
import numpy as np

img = cv2.imread("09-simple-spatial-filters-27-02-2026/cameraman.tif", 0)

kernel = np.array([
    [-1,-1,-1],
    [-1,8,-1],
    [-1,-1,-1]
])

hpf = cv2.filter2D(img, -1, kernel)

cv2.imshow("High Pass Filter", hpf)
cv2.waitKey(0)
cv2.destroyAllWindows()