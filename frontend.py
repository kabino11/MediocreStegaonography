import os

import steg

running = True

while running:
	print ("E: Encode Message")
	print ("D: Decode Message")
	print ("F: Encode File")
	print ("W: Decode File")
	print ("S: Query file size")
	print ("Q: Quit")

	response = input(">")

	if response.lower() == 'e':
		file_name = input("Filename of base image?: ")

		msg = input("Message?: ")
		print ("Now encoding...")

		img = steg.msgEncode(file_name, msg)

		print ("Done.\n")

		img.save("output.png")

	elif response.lower() == 'd':
		file_name = input("Name of file to decode?: ")

		char_num = int(input("How many characters do you want to decode?: "))
		print ("")

		print (steg.decode_as_msg(file_name, char_num), "\n")

	elif response.lower() == 'f':
		img_file = input("Filename of base image?: ")

		file_name = input("Name of file to encode?: ")
		print ("")

		img = steg.fileEncode(img_file, file_name)

		print ("Done.\n")

		img.save("fOutput.png")

	elif response.lower() == 'w':
		img_file = input("Filename of image to decode?: ")

		b_num = int(input("How many bytes do you want to decode?: "))

		f_out = input("Filename of output file?: ")

		print ("")

		steg.decode_as_file(img_file, b_num, f_out)

		print ("Done.\n")

	elif response.lower() == 's':
		filename = input("File name?: ")

		print ("The file has", os.stat(filename).st_size, "bytes.\n")

	elif response.lower() == 'q':
		running = False
		print ("Good-bye!")

	else:
		print ("Invalid response, please try again.\n")
