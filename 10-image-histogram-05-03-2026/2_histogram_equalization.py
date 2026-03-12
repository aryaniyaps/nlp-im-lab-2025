import cv2
img = cv2.imread('cameraman.tif', 0)

eq = cv2.equalizeHist(img)
cv2.imshow("Histogram Equalization", eq)
cv2.waitKey(0)
cv2.destroyAllWindows()
