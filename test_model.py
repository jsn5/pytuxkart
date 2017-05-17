import pyautogui
import numpy as np
import time
from PIL import Image
from resizeimage import resizeimage
from alexnet import alexnet
import pyxhook
from mss import mss


WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 10
MODEL_NAME = 'output/tuxcart.model'
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


def getImage():
	with mss() as sct:
		# The screen part to capture
		mon = {'top': 65, 'left': 50, 'width': 1020, 'height': 720}
		sct.get_pixels(mon)
		img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
	return img

def straight():
	pyautogui.keyDown('w')
	pyautogui.keyUp('a')
	pyautogui.keyUp('d')
	pyautogui.keyUp('s')
	pyautogui.keyUp('w')



def left():
	pyautogui.keyDown('a')
	pyautogui.keyUp('d')
	pyautogui.keyUp('s')
	pyautogui.keyUp('a')

def right():
	pyautogui.keyDown('d')
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



def main():
	for i in list(range(4))[::-1]:
		print(i+1)
		time.sleep(1)


	count=0
	while(True):
		if not paused:
			# 800x600 windowed mode
			avg_prediction = [0,0,0]
			screen = getImage()
			last_time = time.time()
			screen = screen.convert('L')
			screen = resizeimage.resize_cover(screen, [160, 120], validate=False)
			screen = np.array(screen)
			prediction = model.predict([screen.reshape(160,120,1)])[0]		
			fwd_threshold=0.9
			turn_threshold=0.5
			print(prediction)
			max_val = max(prediction)
			if prediction[0] >= turn_threshold:
				print("right")
				right()
			elif prediction[1] >= turn_threshold:
				left()
				print("left")
			elif prediction[2] >= fwd_threshold:
				straight()
				print("straight")
			else:
				back()
			nokey()
			
			print("fps="+str(time.time()-last_time))
			
				

main()


