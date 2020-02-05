# The below script is used to make video from a single image and audio.
# For the input it uses a .TIF image and .wma audio file

import moviepy.editor as mpe
import os

from PIL import Image

temp = 'temp.jpg'
fps  = 24

# converts the .TIF image to .png in order to moviepy could work with it
def save_temp_image(image_path):
	image = Image.open(image_path)
	image.thumbnail(image.size)
	image.convert("RGB").save(temp, "JPEG", quality = 100)

# deletes the temporal image
def delete_temp_image():
	os.remove(temp)

def clean_up(name):
	os.remove(temp)
	os.remove(name)

# assembles the video
def assemble(image_path, sound_path, video_name):
	save_temp_image(image_path)

	sound = mpe.AudioFileClip(sound_path)
	video = mpe.ImageClip(temp, duration = sound.duration)

	video.set_audio(sound).write_videofile(video_name, codec = 'libx264', fps = fps)

	delete_temp_image()

if __name__ == "__main__":
	assemble("C:\\Users\\tsbot\\Desktop\\044A.TIF", "C:\\Users\\tsbot\\Desktop\\gyertyaszentelo.wma", "video.mp4")

