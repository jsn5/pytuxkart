import pyautogui
from numba import jit
import numpy as np
import time
import os
import curses
from PIL import Image
import pyxhook
from resizeimage import resizeimage



#instantiate HookManager class
new_hook=pyxhook.HookManager()


for i in list(range(4))[::-1]:
		print(i+1)
		time.sleep(1)

count = 0
#this function is called everytime a key is pressed.
def OnKeyPress(event):
	key = event.Ascii
	paused = False
	# 800x600 windowed mode
	screen = pyautogui.screenshot(region=(65,50, 1020, 720))
	last_time = time.time()
	screen = screen.convert('L')
	screen = resizeimage.resize_cover(screen, [160, 120], validate=False)
	screen = np.array(screen)
	# resize to something a bit more acceptable for a CNN
	if key != 97 and key != 100:
		global count
		print("step "+str(count))
		count+=1
		output = keys_to_output(key)
		print(output)
		training_data.append([screen,output])
	
	
	if len(training_data) % 100 == 0:
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


file_name = 'training_data.npy'

if os.path.isfile(file_name):
	print('File exists, loading previous data!')
	training_data = list(np.load(file_name))
else:
	print('File does not exist, starting fresh!')
	training_data = []


