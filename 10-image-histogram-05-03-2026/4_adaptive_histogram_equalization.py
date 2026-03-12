import cv2
img = cv2.imread('cameraman.tif', 0)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
clahe_img = clahe.apply(img)
cv2.imshow("CLAHE", clahe_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
