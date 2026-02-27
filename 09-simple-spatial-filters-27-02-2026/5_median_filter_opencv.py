import cv2

img = cv2.imread("09-simple-spatial-filters-27-02-2026/cameraman.tif", 0)

g = cv2.medianBlur(img, 3)
cv2.imshow("Median Filter", g)

cv2.waitKey(0)
cv2.destroyAllWindows()