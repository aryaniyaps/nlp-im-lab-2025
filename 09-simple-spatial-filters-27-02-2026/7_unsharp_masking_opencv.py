import cv2

img = cv2.imread("09-simple-spatial-filters-27-02-2026/cameraman.tif", 0)

blur = cv2.GaussianBlur(img, (5,5), 1.0)
sharp = cv2.addWeighted(img, 1.5, blur, beta=-0.5, gamma=0)

cv2.imshow("Unsharp Masking", sharp)
cv2.waitKey(0)
cv2.destroyAllWindows()