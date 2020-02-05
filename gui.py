from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
from tkinter import messagebox
from multiprocessing import Process
from threading import Thread

import os
import video_maker
import time

process = None
canceled = False

def load_image():
	image_path.delete(0, END)
	image_path.insert(0, askopenfilename(filetypes = [('Image files', ('.png', '.jpg', '.jpeg', '.tiff', '.TIF'))]))

def load_sound():
	sound_path.delete(0, END)
	sound_path.insert(0, askopenfilename(filetypes = [('Audio files', ('.mp3', '.wma', '.wav', '.flac'))]))

def check():
	if not(os.path.isfile(image_path.get())):
		messagebox.showinfo('Hiba', 'Nem megfelelő képfájl!')
		return False

	if not(os.path.isfile(sound_path.get())):
		messagebox.showinfo('Hiba', 'Nem megfelelő hangfájl!')
		return False

	if len(name_path.get()) == 0:
		messagebox.showinfo('Hiba', 'Nincs fájlnév megadva!')
		return False

	return True

def build(image, sound, name):
	video_maker.assemble(image, sound, name)

def submit():
	global process

	process = Process(target = build, args = (image_path.get(), sound_path.get(), name_path.get() + ".mp4"))
	process.start()
	process.join()
	process = None

	if not(canceled):
		done()

def start():
	if check():
		global canceled
		canceled = False

		image_button["state"] = "disabled"
		sound_button["state"] = "disabled"
		assemble_button["state"] = "disabled"
		cancel_button["state"] = "normal"
	
		thread = Thread(target = submit)
		thread.start()

		progress.start(10)

def cancel():
	global canceled
	canceled = True

	image_button["state"] = "normal"
	sound_button["state"] = "normal"
	assemble_button["state"] = "normal"
	cancel_button["state"] = "disabled"

	global process
	process.terminate()
	process.join()
	process = None

	progress.stop()

	video_maker.clean_up(name_path.get() + "TEMP_MPY_wvf_snd.mp3")

def done():
	image_button["state"] = "normal"
	sound_button["state"] = "normal"
	assemble_button["state"] = "normal"
	cancel_button["state"] = "disabled"

	progress.stop()

	messagebox.showinfo('Kész', 'A videó exportálva!')

def exit():
	if process == None:
		window.destroy()
	elif messagebox.askokcancel("Kilépés", "A videó exportálása folyamatban van. Ha kilép megszakad. Folytatja?"):
		cancel()
		window.destroy()

if __name__ == "__main__":
	window = Tk()
	
	window.title("VidAssembler")
	window.resizable(False, False)
	window.protocol("WM_DELETE_WINDOW", exit)
	
	image_label = Label(window, text = "Kép:", width = 5, font=("Arial", 12))
	image_label.grid(column = 0, row = 0, sticky = W, pady = 10, padx = 10)
	image_path = Entry(window, width = 30)
	image_path.grid(column = 1, row = 0, sticky = W, pady = 10, padx = 10)
	image_button = Button(window, text = "Tallózás", width = 10, command = load_image)
	image_button.grid(column = 2, row = 0, sticky = W, pady = 10, padx = 10)
	
	sound_label = Label(window, text = "Hang:", width = 5, font=("Arial", 12))
	sound_label.grid(column = 0, row = 1, sticky = W, pady = 10, padx = 10)
	sound_path = Entry(window, width = 30)
	sound_path.grid(column = 1, row = 1, sticky = W, pady = 10, padx = 10)
	sound_button = Button(window, text = "Tallózás", width = 10, command = load_sound)
	sound_button.grid(column = 2, row = 1, sticky = W, pady = 10, padx = 10)
	
	name_label = Label(window, text = "Név:", width = 5, font=("Arial", 12))
	name_label.grid(column = 0, row = 2, sticky = W, pady = 10, padx = 10)
	name_path = Entry(window, width = 30)
	name_path.grid(column = 1, row = 2, sticky = W, pady = 10, padx = 10)
	
	assemble_button = Button(window, text = "Indítás", width = 10, command = start)
	assemble_button.grid(column = 0, row = 3, sticky = W, pady = 10, padx = 10)
	progress = Progressbar(window, orient = HORIZONTAL, mode = 'indeterminate', length = 185) 
	progress.grid(column = 1, row = 3, sticky = W, pady = 10, padx = 10)
	cancel_button = Button(window, text = "Leállítás", width = 10, command = cancel)
	cancel_button.grid(column = 2, row = 3, sticky = W, pady = 10, padx = 10)
	
	cancel_button["state"] = "disabled"

	window.mainloop()	