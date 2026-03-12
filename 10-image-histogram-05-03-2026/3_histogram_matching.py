import cv2
from skimage import exposure
img = cv2.imread('cameraman.tif', 0)

ref = cv2.imread('coins.png', 0)
matched = exposure.match_histograms(img, ref)
cv2.imshow("Histogram Specification", matched.astype('uint8'))
cv2.waitKey(0)
cv2.destroyAllWindows()

