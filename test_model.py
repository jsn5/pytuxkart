import pyautogui
import numpy as np
import time
from PIL import Image
from resizeimage import resizeimage
from alexnet import alexnet
import pyxhook

WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 10
MODEL_NAME = 'tuxcart.model'
model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)

paused = False
#instantiate HookManager class
new_hook=pyxhook.HookManager()
#this function is called everytime a key is pressed.
def OnKeyPress(event):
  key = event.Ascii
  if(key == 112):
  		global paused
	  	if(paused):
	  		paused=False
	  		print("resume")
	  	else:
	  		paused=True
	  		print("pause")

#listen to all keystrokes
new_hook.KeyDown=OnKeyPress
#hook the keyboard
new_hook.HookKeyboard()
#start the session
new_hook.start()



def straight():
	pyautogui.keyDown('w')
	pyautogui.keyUp('a')
	pyautogui.keyUp('d')
	pyautogui.keyUp('s')
	pyautogui.keyUp('w')



def left():
	pyautogui.keyDown('a')
	pyautogui.keyDown('w')
	pyautogui.keyUp('d')
	pyautogui.keyUp('s')
	pyautogui.keyUp('a')

def right():
	pyautogui.keyDown('d')
	pyautogui.keyDown('w')
	pyautogui.keyUp('a')
	pyautogui.keyUp('s')
	pyautogui.keyUp('d')

def back():
	pyautogui.keyDown('s')
	pyautogui.keyUp('w')
	pyautogui.keyUp('a')
	pyautogui.keyUp('d')

def nokey():
	pyautogui.keyDown('w')
	pyautogui.keyUp('a')
	pyautogui.keyUp('s')
	pyautogui.keyUp('d')



def main():
	for i in list(range(4))[::-1]:
		print(i+1)
		time.sleep(1)

	count=0
	while(True):

		if not paused:

			# 800x600 windowed mode
			screen = pyautogui.screenshot(region=(65,50, 800, 600))
			last_time = time.time()
			screen = screen.convert('L')
			screen = resizeimage.resize_cover(screen, [160, 120], validate=False)
			screen = np.array(screen)
			prediction = model.predict([screen.reshape(160,120,1)])[0]
			print(prediction)
			turn_thresh = 0.6
			fwd_thresh = 0.6

			max_ = max(prediction)
			if prediction[0] > turn_thresh:
				print("right")
				right()
			elif prediction[1] > turn_thresh:
				left()
				print("left")
			elif prediction[2] == max_:
				straight()
				print("straight")
			else:
				nokey()
			
				

main()


