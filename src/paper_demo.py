import pygame
import paper
import func
import pickle
import sys

BLACK = (0,0,0,1)
WHITE = (255,255,255)

pygame.init()
screen = pygame.display.set_mode((480, 640), 0, 32)
screen.fill(WHITE)

page = paper.Page()
status = paper.Status()

#f = open('log.')
#page.notes = pickle.load()
tick = 0

while True:
	tick += 1
	#page.show(screen)
	for event in pygame.event.get():
		#print(event.type)
		if event.type == pygame.QUIT:
			# 接收到退出时间后退出程序
			exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				f = open('log', 'rb')
				page.load(f)
				page.show(screen)
			if event.key == pygame.K_s:
				f = open('log', 'wb')
				page.save(f)
			if event.key == pygame.K_q:
				sys.exit(0)
		if event.type == pygame.MOUSEBUTTONDOWN:
			if status.clicked == False:
				#print('clicked')
				status.clicked = True
				status.last = [event.pos]
				status.t = []
				status.last_t = tick
		if event.type == pygame.MOUSEBUTTONUP:
			if status.clicked == True:
				status.t.append(func.getwidth(tick-status.last_t))
				pygame.draw.line(screen, BLACK,status.last[-1], event.pos, status.t[-1])
				status.last.append(event.pos)
				status.last_t = tick
				#print('released')
				log = paper.Log()
				log.data = {"line":status.last, "width": status.t}
				#print(log.data)
				log.type = "Line"
				status.clicked = False
				page.notes.append(log)
				#page.save(open('log', 'wb'))
		if event.type == pygame.MOUSEMOTION:
			if status.clicked == True:
				if func.dist(event.pos, status.last[-1]) > 5:
					#print('drawing', status.last[-1], event.pos)
					status.t.append(func.getwidth(tick-status.last_t))
					pygame.draw.line(screen, BLACK,status.last[-1], event.pos, status.t[-1])
					status.last.append(event.pos)
					status.last_t = tick
	pygame.display.update()


