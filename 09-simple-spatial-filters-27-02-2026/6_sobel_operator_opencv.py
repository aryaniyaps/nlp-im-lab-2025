"""Sobel Operator (Gradient based HPF)"""
import cv2

img = cv2.imread("09-simple-spatial-filters-27-02-2026/cameraman.tif", 0)

gx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
gy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

g = cv2.magnitude(gx, gy)
g = cv2.normalize(g, None, 0, 255, cv2.NORM_MINMAX)

cv2.imshow("Sobel HPF", g.astype("uint8"))

cv2.waitKey(0)
cv2.destroyAllWindows()