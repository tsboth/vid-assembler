# The below script is used to make video from a single image and audio with the help of the moviepy module
# It needs to be installed with command: pip install moviepy
# For the input usual it uses a .TIF image and .wma audio file (only with those was tested)

import moviepy.editor as mpe
import os
import sys

from PIL import Image
from os.path import expanduser

temp_image = 'temp.jpg'
temp_audio = None
fps  = 24

# converts the .TIF image to .png in order to moviepy could work with it
def save_temp_image(image_path):
	image = Image.open(image_path)
	image.thumbnail(image.size)
	image.convert("RGB").save(temp_image, "JPEG", quality = 100)

# cleans up the remaining files
def clean_up(name):
	if (os.path.exists(temp_image)):
		os.remove(temp_image)

	if (os.path.exists(name)):
		os.remove(name)

# assembles the video
def assemble(image_path, sound_path, video_name):
	save_temp_image(image_path)

	sound = mpe.AudioFileClip(sound_path)
	video = mpe.ImageClip(temp_image, duration = sound.duration)
	# putting the video on the desktop
	desktop = os.path.join(expanduser("~"), "Desktop")

	video.set_audio(sound).write_videofile(os.path.join(desktop, video_name), codec = 'libx264', fps = fps)

	clean_up(None)

def print_usage():
	print("Usage: python vid_assembler image_path sound_path video_name")

# can be used for command line too
if __name__ == "__main__":
	if (len(sys.argv) < 4):
		print("Error: Too few parameters")
		print_usage()
		sys.exit()

	if (len(sys.argv) > 4):
		print("Error: Too many parameters")
		print_usage()
		sys.exit()

	if (not(os.path.exists(sys.argv[1]))):
		print("Error: Wrong image_path")
		print_usage()
		sys.exit()

	if (not(os.path.exists(sys.argv[2]))):
		print("Error: Wrong sound_path")
		print_usage()
		sys.exit()

	assemble(sys.argv[1], sys.argv[2], sys.argv[3])
