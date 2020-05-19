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
	screen.fill(WHITE)
	page.show(screen)
	pygame.display.update()
	for event in pygame.event.get():
		#print(event.type)
		if event.type == pygame.QUIT:
			# 接收到退出时间后退出程序
			exit()
		if event.type == pygame.KEYDOWN:
			if status.clicked == False:
				if event.key == pygame.K_r:
					f = open('log', 'rb')
					page.load(f)
					page.show(screen)
				if event.key == pygame.K_s:
					f = open('log', 'wb')
					page.save(f)
				if event.key == pygame.K_q:
					sys.exit(0)
			if status.clicked == "inputing":
				if event.key != pygame.K_RETURN:
					if event.key != pygame.K_BACKSPACE:
						status.log.data["content"] += chr(event.key)
					elif len(status.log.data["content"]) > 0:
						status.log.data["content"] = status.log.data["content"][:-1]
				else:
					status.clicked = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if status.clicked == False:
				if event.button == 1:
					#print('clicked')
					status.type = "line"
					status.clicked = True
					status.last = [event.pos]
					status.t = []
					status.last_t = tick
					log = paper.Log()
					page.notes.append(log)
					log.type = "Line"
					log.data = {"line": [event.pos], "width":[]}
					status.log = log
				if event.button == 3:
					status.type = "word"
					status.clicked = True
					status.last = event.pos

		if event.type == pygame.MOUSEBUTTONUP:
			if status.clicked == True and status.type == "line":
				status.log.data["width"].append(func.getwidth(tick-status.last_t))
				status.log.data["line"].append(event.pos)
				status.last_t = tick
				#print('released')
				status.clicked = False
				#page.save(open('log', 'wb'))
			if status.clicked == True and status.type == "word":
				dir = [status.last, event.pos]
				print(dir)
				log = paper.Log()
				log.type = "Word"
				log.data = {
					"font":pygame.font.get_default_font(), 
					"size":int(func.dist(dir[0], dir[1])), 
					"content": "", 
					"color":BLACK, 
					"angle":func.getdeg(dir[0], dir[1]), 
					"pos":status.last
				}
				status.log = log
				status.clicked = "inputing"
				print('inputing')
				page.notes.append(log)
		if event.type == pygame.MOUSEMOTION:
			if status.clicked == True and status.type == "line":
				if func.dist(event.pos, status.last[-1]) > 5:
					#print('drawing', status.last[-1], event.pos)
					status.log.data["width"].append(func.getwidth(tick-status.last_t))
					status.log.data["line"].append(event.pos)
					status.last_t = tick
	pygame.display.update()


