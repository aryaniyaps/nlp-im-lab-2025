import cv2
import matplotlib.pyplot as plt
img = cv2.imread('cameraman.tif', 0)
plt.figure()
plt.imshow(img, cmap='gray')
plt.title("Original Image")
plt.axis('off')
plt.figure()
plt.hist(img.ravel(), bins=256, range=[0,256])
plt.title("Histogram")
plt.show()
