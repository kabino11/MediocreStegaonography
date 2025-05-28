This is an incredibly bare-bones image stegaonography implementation.

It basically takes your input, converts it into a list of bits, then encodes it into an image by modifying the LSB of each pixel value (RGB) with a single bit of the message to encode.

To use the app run frontend.py in python and go through the basic TUI menu to do what you want.  You have options to Encode/Decode basic ASCII messages, Encode/Decode files, and to query the length of a given file (note: the app will test whether the image is big enough to encode your file anyways, this query is so that you can know what number to put in to decode it.)

As for issues with this stegaonography implementation it will only work with lossless image formats and I wouldn't be surprised if the encoded data is obvious to someone who is actively looking for it.  To address this while my code will accept any image format (or any accepted by PIL's Image library) it will only output .pngs as output.

Also this is code that was originally written when I was back in college (circa 2017), while I have taken the liberty of somewhat cleaning it up and getting it working with modern python implementations a lot of the code is still formatted in a manner indicative of someone who has never worked in a production setting.  Additionally I wouldn't be surprised if this code only worked on linux (I tested it with Arch Linux using python 3.13.3-1.)
