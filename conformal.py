import pygame
import numpy
import cmath
import sys
import threading
import time

running = True

#the function that we're trying to map
myfunc = lambda z: z
win_size = (400,400)
default_scale = (1,1)

def coords_to_num(coords, max_coords, scale=default_scale):
	#first, we want to transform coords so that 0,0 represents the center
	#also, we want a positive y value to represent being higher up
	new_coords = list(coords)
	new_coords[1] *= -1
	new_coords = [new_coords[0] - max_coords[0]/2., new_coords[1] + max_coords[1]/2]
	#now, we rescale our new coordinates
	new_coords = [2*new_coords[i]/max_coords[i] for i in range(2)]
	return (new_coords[0]*scale[0])+(new_coords[1]*scale[1]*1j)

def num_to_coords(num, max_coords, scale=default_scale):
	#coords_to_num, but in reverse
	new_coords = [num.real/scale[0], num.imag/scale[1]]
	new_coords = [max_coords[i]*new_coords[i]/2. for i in range(2)]
	new_coords = [new_coords[0] + max_coords[0]/2., new_coords[1] - max_coords[1]/2]
	new_coords[1] *= -1
	return new_coords

def thread_loop():
	global myfunc, original, running #yay, globals! and in a thread to boot
	while running:
		new_func = input()
		if new_func == "quit":
			running = False
			return
		try:
			myfunc = lambda z: eval(new_func) #yay, unsafe evals!
		except:
			print("Some error happened.")
		original = False
		plot()

#dumb pygame initialization stuff
pygame.init()
window = pygame.display.set_mode(win_size)
pygame.display.set_caption("conformal mapper")
pygame.display.set_icon(pygame.Surface((32,32),pygame.SRCALPHA))
screen = pygame.display.get_surface()

#load the image that we'll map, conformally
my_image = "think.png"
try: my_image = sys.argv[1]
except IndexError: pass
base_image = pygame.image.load(my_image).convert()
base_image = pygame.transform.scale(base_image, win_size)

#now, check if the user wants to tile their images
tiling = False
try: 
	if sys.argv[2] == "-t": tiling = True
except IndexError: pass

console_thread = threading.Thread(target=thread_loop)

def transform(coords):
	old_pixel = base_image.get_at(coords)
	new_num = myfunc(coords_to_num(coords, win_size))
	new_pixel = num_to_coords(new_num, win_size)
	try:
		color = base_image.get_at(tuple(map(int, new_pixel)))
	except IndexError:
		if not tiling: color = (0,0,0)
		else:
			new_pixel = tuple(map(int, new_pixel))
			new_pixel = [new_pixel[0] % win_size[0], new_pixel[1] % win_size[1]]
			color = base_image.get_at(new_pixel)
	screen.set_at(coords, color)
	return (new_num, new_pixel)

def plot():
	begin_time = time.time()
	screen.fill((0,0,0))
	for x in range(0, win_size[0]):
		for y in range(0, win_size[1]):
			transform((x,y))
	print(time.time() - begin_time)
	pygame.display.flip()

plot()
pygame.display.flip()

pressed = False
original = False

console_thread.start()

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			quit()
	if pygame.mouse.get_pressed()[0] and not pressed:
		pressed = True
		if original:
			screen.fill((0,0,0))
			plot()
			original = False
		else:
			screen.blit(base_image, [0,0])
			pygame.display.flip()
			original = True
	elif not pygame.mouse.get_pressed()[0]: pressed = False
