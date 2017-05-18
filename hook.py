import numpy as np
import time
import os
from PIL import Image
import pyxhook
from resizeimage import resizeimage
from mss import mss
import os

#instantiate HookManager class
new_hook=pyxhook.HookManager()


for i in list(range(4))[::-1]:
		print(i+1)
		time.sleep(1)

count = 0
current_key = 0
#this function is called everytime a key is pressed.
def OnKeyPress(event):
	global current_key
	current_key = event.Ascii
	#saveData(key)


def getImage():
	with mss() as sct:
		# The screen part to capture
		mon = {'top': 65, 'left': 50, 'width': 1020, 'height': 720}
		sct.get_pixels(mon)
		img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
	return img

def saveData(key):
	last_time=time.time()
	#screen = pyautogui.screenshot(region=(65,50, 1020, 720))
	screen = getImage()
	#screen.save("test.png")
	screen = screen.convert('L')
	screen = resizeimage.resize_cover(screen, [160, 120], validate=False)
	screen = np.array(screen)
	output = keys_to_output(key)
	print(output)
	training_data.append([screen,output])
	print("time="+str(time.time()-last_time))
	if len(training_data) % 1000 == 0:
		print("length of data:")
		print(len(training_data))
		np.save(file_name,training_data)

#listen to all keystrokes
new_hook.KeyDown=OnKeyPress
#hook the keyboard
new_hook.HookKeyboard()
#start the session
new_hook.start()
	



def keys_to_output(keys): 
	output = [0,0,0]
	if keys == 100: #right
		output[0] = 1
	elif keys == 97:
		output[1] = 1
	else:
		output[2] = 1
	return output


file_name = 'data/training_data.npy'

if os.path.isfile(file_name):
	print('File exists, loading previous data!')
	training_data = list(np.load(file_name))
else:
	print('File does not exist, starting fresh!')
	training_data = []

def main():

	global current_key
	paused = False;
	while True:
		if paused == True:
			if current_key == 112:
				paused = False
				time.sleep(1)
				print("resumed")
				current_key = 0
		else:
			if current_key == 112:
				paused = True
				time.sleep(1)
				print("paused")
				current_key = 0
			else:
				saveData(current_key)
			





main()
