import os
import math
from PIL import Image


# Creates a factory that YIELDs the info for an image one pixel at a time.
def gen_pix_factory(im):
	num_cols, num_rows = im.size
	r, c = 0, 0
	while r != num_rows:
		c = c % num_cols
		yield ((c, r), im.getpixel((c, r)))
		if c == num_cols - 1: r += 1
		c += 1


# Takes a byte and converts it into a list of bits we can save in a file.
def serialize_byte(byte):
	output = []
	num = ord(byte)

	for x in range(8):
		output.append(num % 2)
		num = num >> 1

	# Needed for bit order correctness
	output.reverse()

	return output


# Serialize the string into a string of bits
def convert_msg_to_bits(msg):
	output = []

	# for each character in the list generate the ASCII code of the character
	# serialize it into bits, and place in our output
	for curr in msg:
		output += serialize_byte(curr)

	return output


# Serializes file into a list of bits
def convert_file_to_bits(filename):
	output = []

	# iterate through the file
	with open(filename, "rb") as f:
		byte = f.read(1)
		while len(byte) != 0 and byte != "":
			output += serialize_byte(byte)

			byte = f.read(1)

	return output


# Encodes a series of bits into an given image (denoted by filename)
# returns resulting image
def encode(img_src, bits):
	# create our image object from img_src and convert to RGB
	img = Image.open(img_src)
	img = img.convert('RGB')

	cols, rows = img.size
	if len(bits) > cols * rows * 3:
		raise ValueError("Too much data to encode in image.")

	# initalize our output image
	out_img = Image.new('RGB', img.size)

	# initalize our generators
	gen_pix = gen_pix_factory(img)

	# initalize our first pixel of data
	colorMode = 0
	pix = next(gen_pix)
	coords, rgb = pix
	red, green, blue = rgb

	# now iterate through our list of bits to encode the data
	for bit in bits:
		# based on which color we're on change the least significant bit
		if colorMode == 0:
			red -= red % 2
			red += bit
			colorMode = 1
		elif colorMode == 1:
			green -= green % 2
			green += bit
			colorMode = 2
		elif colorMode == 2:
			blue -= blue % 2
			blue += bit
			colorMode = 3

		if colorMode >= 3:  # if we've iterated through all of the data on the bit place it in the output image and fetch our next bit
			out_img.putpixel(coords, (red, green, blue))
			colorMode = 0
			pix = next(gen_pix)
			coords, rgb = pix
			red, green, blue = rgb

	if colorMode != 0:
		out_img.putpixel(coords, (red, green, blue))

	for pix in gen_pix:
		coords, rgb = pix
		out_img.putpixel(coords, rgb)

	return out_img


# Encodes an ASCII image into an image.
def msgEncode(img_src, message):
	# first we turn our message into a list of bits to encode
	bits_to_encode = convert_msg_to_bits(message)

	# then encode it using the generic encoding function
	return encode(img_src, bits_to_encode)


# Encodes a file into an image
def fileEncode(img_src, filename):
	bits_to_encode = convert_file_to_bits(filename)

	return encode(img_src, bits_to_encode)


# Reads bytes from stegaonographic image and return as list
# Takes an input file name and length of expected message
# Presumes that image is in a lossless format (i.e. png) to preserve least-signficant pixel values
def decode(src, length):
	output = []

	img = Image.open(src)
	img.convert("RGB")
	gen_pix = gen_pix_factory(img)

	charAt = 0

	bitList = []

	for pix in gen_pix:
		coords, rgb = pix
		red, green, blue = rgb

		bitList.append(red % 2)
		bitList.append(green % 2)
		bitList.append(blue % 2)

		if len(bitList) >= 8:
			charData = bitList[0:8]
			current = 0
			for bit in charData:
				current = current << 1
				current += bit

			output.append(current)
			bitList = bitList[8:]
			charAt += 1

		if charAt >= length:
			break

	return output


# Decodes a message from a source image
# Takes an input file name and length of expected message in bytes
def decode_as_msg(src, length):
	msg = ""

	data = decode(src, length)

	for x in data:
		msg += chr(x)

	return msg


# Decodes a file from a source image.
# Takes an input file name and length of expected file in bytes
def decode_as_file(src, length, newFName):
	f = open(newFName, "wb")

	data = decode(src, length)

	for b in data:
		f.write(bytes([b]))

	f.close()

	return
