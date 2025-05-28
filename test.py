import os
from PIL import Image

import steg

size = os.stat("test file.pdf").st_size * 8

remain = size % 3
pix_req = size / 3

if remain > 0:
	pix_req += 1

img = Image.open("test image.jpg")
img = img.convert('RGB')

print(pix_req, "pixels needed")

num_cols, num_rows = img.size

print("Image has", num_cols * num_rows, "pixels")

if pix_req > num_cols * num_rows:
	print("Image not big enough")
else:
	print("File can be encoded")

exit(0)

with open("test file.pdf", "rb") as f:
	byte = f.read(1)
	while byte != "":
		print(byte)
		byte = f.read(1)
