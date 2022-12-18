import pygame, sys, math
	
width = 1024
height = 720
radius = 300.0
Tom = 0.0
Jerry_x = 0.1 
Jerry_y = 0.0
Jerry_speed = 1.0
Tom_speeds = [3.5, 4.0, 4.2, 4.4, 4.6]
Tom_speed_ix = 0
speed_mult = 3.0
clicking = False

def restart():
	global Tom, Jerry_x, Jerry_y, clicking
	Tom = 0.0
	Jerry_x = 0.1 
	Jerry_y = 0.0
	clicking = False

pygame.init()
window = pygame.display.set_mode((width, height)) 

def clear():
	radius_mult = Jerry_speed / Tom_speeds[Tom_speed_ix]

	window.fill((0,80,0))
	pygame.draw.circle(window, (0,0,128), (int(width/2), int(height/2)), int(radius*1.00), 0)
	pygame.draw.circle(window, (200,200,200), (int(width/2), int(height/2)), int(radius*radius_mult), 1)

def redraw(draw_text=False,win=False):
	clear()

	pygame.draw.circle(window, (255,255,255), (int(width/2 + Jerry_x),int(height/2 + Jerry_y)), 6, 2)
	pygame.draw.circle(window, (255,0,0), (int(width/2 + radius*math.cos(Tom)),int(height/2 + radius*math.sin(Tom))), 6, 0)

	if draw_text:
		font = pygame.font.Font(None, 72)
		if win:
			text = font.render("Jerry has Escaped!", 1, (255, 255, 255))
		else:
			text = font.render("Jerry was Eaten", 1, (255, 0, 0))
		textpos = text.get_rect()
		textpos.centerx = window.get_rect().centerx
		textpos.centery = height/2
		window.blit(text, textpos)

	font = pygame.font.Font(None, 48)
	text = font.render("Tom Speed: " + str(Tom_speeds[Tom_speed_ix]), 1, (255, 255, 255))
	textpos = text.get_rect()
	textpos.centerx = width/2
	textpos.centery = height - 20
	window.blit(text, textpos)
		
	pygame.display.flip()

def updateTom():
	global Tom
	Tom_speed = Tom_speeds[Tom_speed_ix]
	newang = math.atan2(Jerry_y, Jerry_x)
	diff = newang - Tom
	if diff < math.pi: diff += math.pi*2.0
	if diff > math.pi: diff -= math.pi*2.0
	if abs(diff)*radius <= Tom_speed * speed_mult:
		Tom = newang
	else:
		Tom += Tom_speed * speed_mult / radius if diff > 0.0 else -Tom_speed * speed_mult / radius
	if Tom < math.pi: Tom += math.pi*2.0
	if Tom > math.pi: Tom -= math.pi*2.0 

def moveJerry(x,y):
	global Jerry_x, Jerry_y
	dx = x - Jerry_x
	dy = y - Jerry_y
	mag = math.sqrt(dx*dx + dy*dy)
	if mag <= Jerry_speed * speed_mult:
		Jerry_x = x
		Jerry_y = y
	else:
		Jerry_x += Jerry_speed * speed_mult * dx/mag
		Jerry_y += Jerry_speed * speed_mult * dy/mag 
	
def detectWin():
	global Tom_speed_ix
	if Jerry_x*Jerry_x + Jerry_y*Jerry_y > radius*radius:
		diff = math.atan2(Jerry_y, Jerry_x) - Tom
		if diff < math.pi: diff += math.pi*2.0
		if diff > math.pi: diff -= math.pi*2.0
		while True:
			is_win = abs(diff) > 0.000001
			redraw(True, is_win)
			events = [event.type for event in pygame.event.get()]
			if pygame.QUIT in events: 
				sys.exit(0)
			elif pygame.MOUSEBUTTONDOWN in events:
				restart()
				if is_win:
					Tom_speed_ix += 1
				break

clock = pygame.time.Clock()
clear()
while True:
	x = None
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			sys.exit(0)
		clicking = pygame.mouse.get_pressed()[0]
		if pygame.mouse.get_pressed()[2]:
				restart()

	if clicking:
		x,y = pygame.mouse.get_pos()
		moveJerry(x - width/2, y - height/2)
	updateTom()
	detectWin()
	redraw()
	clock.tick(60) 
