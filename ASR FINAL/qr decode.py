import cv2
filename = "63710015010.png"
image = cv2.imread(filename)
detector = cv2.QRCodeDetector()
data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
if vertices_array is not None:
  a=data
  print(a)
else:
  print("There was some error")

