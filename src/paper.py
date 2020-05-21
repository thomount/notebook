import pygame
import pickle
import sys
import func
BLACK = (0,0,0)
WHITE = (255,255,255)
CoverWidth = 12
EraserWidth = 5
class Status:
	def __init__(self):
		self.clicked = False
		self.last = []
		self.w = []
		self.last_t = 0
		self.type = None
		self.log = None
		self.shifted = False

class Note:
	pass
class Paper:
	def __init__(self, path, size):
		#print(path)
		#print('paper init')
		try:
			self.img = pygame.transform.scale(pygame.image.load(path), size)
			self.avc = pygame.transform.average_color(self.img)
			#print(self.avc)
			#print('load background success')
		except:
			self.img = None
			#print('load background failed')
	def show(self, screen):
		if self.img != None:
			screen.blit(self.img, (0,0))
		else:
			screen.fill(WHITE)

class Page:
	def __init__(self, path, paperpath, size):
		self.notes = []
		self.paper = Paper(paperpath, size)
		self.status = Status()
		#self.file = open()
		self.path = path
		self.load()
		self.tick = 0

	def show(self, screen):
		self.tick += 1
		self.paper.show(screen)
		for note in self.notes:
			note.show(screen, self.paper)

	def save(self):
		file=open(self.path, 'wb')
		pickle.dump(self.notes, file)
		file.close()

	def load(self):
		try:
			file = open(self.path, 'rb')
			self.notes = pickle.load(file)
			file.close()	
		except:
			pass	
	def isready(self):
		return self.status.clicked == False
	def event(self, e):
		if e.type == pygame.KEYDOWN:
			if self.status.clicked == False:
				if e.key == pygame.K_q:
					sys.exit(0)
				if e.key == pygame.K_c:
					self.status.type = 'cover'
				if e.key == pygame.K_e:
					self.status.type = 'eraser'
			if self.status.clicked == "inputing":
				if e.key != pygame.K_RETURN:
					if e.key != pygame.K_BACKSPACE:
						if e.key != pygame.K_LSHIFT and e.key != pygame.K_RSHIFT:
							self.status.log.data["content"] += func.getKey(self.status.shifted, e.key)
						else:
							self.status.shifted = True
					elif len(self.status.log.data["content"]) > 0:
						self.status.log.data["content"] = self.status.log.data["content"][:-1]
				else:
					self.save()
					self.status.clicked = False
		if e.type == pygame.KEYUP:
			if e.key == pygame.K_LSHIFT or e.key == pygame.K_RSHIFT:
				self.status.shifted = False
		if e.type == pygame.MOUSEBUTTONDOWN:
			if self.status.clicked == False:
				if e.button == 1:
					if self.status.type == 'cover':
						log = Log()
						log.type ='Cover'
						log.data = [e.pos, e.pos, CoverWidth]
						self.notes.append(log)
						self.status.log = log
						self.status.clicked = True
					elif self.status.type == 'eraser':
						log = Log()
						log.type ='Eraser'
						log.data = [e.pos]
						self.notes.append(log)
						self.status.log = log
						self.status.clicked = True
					else:								#line
						#print('clicked')
						self.status.type = "line"
						self.status.clicked = True
						self.status.last = [e.pos, e.pos]
						self.status.t = []
						self.status.last_t = self.tick
						log = Log()
						self.notes.append(log)
						log.type = "Line"
						log.data = {"line": [e.pos], "width":[]}
						self.status.log = log
				if e.button == 3:
					self.status.type = "word"
					self.status.clicked = True
					self.status.last = e.pos

		if e.type == pygame.MOUSEBUTTONUP:
			if self.status.clicked == True:
				if self.status.type == "line":
					self.status.log.data["width"].append(func.getwidth(self.tick-self.status.last_t))
					self.status.log.data["line"].append(e.pos)
					self.status.last_t = self.tick
					#print('released')
					self.status.clicked = False
					self.save()
					#page.save(open('log', 'wb'))
				if self.status.type == "word":
					dir = [self.status.last, e.pos]
					#print(dir)
					log = Log()
					log.type = "Word"
					log.data = {
						"font":pygame.font.get_default_font(), 
						"size":int(func.dist(dir[0], dir[1])), 
						"content": "", 
						"color":BLACK, 
						"angle":func.getdeg(dir[0], dir[1]), 
						"pos":self.status.last
					}
					self.status.log = log
					self.status.clicked = "inputing"
					#print('inputing')
					self.notes.append(log)
				if self.status.type == "cover":
					self.status.log.data[1] = e.pos
					self.status.clicked = False
					self.status.type = None
					self.save()
				if self.status.type == "eraser":
					self.status.log.data.append(e.pos)
					self.status.clicked = False
					self.status.type = None
					self.save()
		if e.type == pygame.MOUSEMOTION:
			if self.status.clicked == True and self.status.type == "line":
				if func.dist(e.pos, self.status.last[-1]) > 5:
					#print('drawing', status.last[-1], event.pos)
					self.status.log.data["width"].append(func.getwidth(self.tick-self.status.last_t))
					self.status.log.data["line"].append(e.pos)
					self.status.last_t = self.tick
			if self.status.clicked == True and self.status.type == "cover":
				self.status.log.data[1] = e.pos
			if self.status.clicked == True and self.status.type == "eraser":
				if func.dist(e.pos, self.status.log.data[-1]) > 5:
					self.status.log.data.append(e.pos)


class Log:
	def __init__(self):
		self.type = None
		self.data = []
	def show(self, screen, paper):
		if self.type == "Line":
			for i in range(len(self.data["line"])-1):
				pygame.draw.line(screen, BLACK,self.data["line"][i], self.data["line"][i+1], self.data["width"][i])
	
		if self.type == "Word":
			text = pygame.font.SysFont(self.data["font"], self.data["size"])
			text_fmt = text.render(self.data["content"], True, self.data['color'])
			#rint(text_fmt.get_width(), text_fmt.get_height())
			text_fmt = pygame.transform.rotate(text_fmt, self.data["angle"])
			#print(text_fmt.get_width(), text_fmt.get_height())
			x = self.data["pos"][0]
			y = self.data["pos"][1]
			if self.data["angle"] > 0:
				y -= text_fmt.get_height()
			if abs(self.data["angle"]) > 90:
				x -= text_fmt.get_width()
			screen.blit(text_fmt, (x, y))
		if self.type == 'Cover':
			pygame.draw.line(screen, WHITE, self.data[0], self.data[1], self.data[2])
		if self.type == 'Eraser':
			for pos in self.data:
				#print(pos)
				#print((pos[0]-EraserWidth, pos[1]-EraserWidth, pos[0]+EraserWidth, pos[1]+EraserWidth))
				#pygame.draw.rect(screen, (255,255,255,10), (pos[0]-EraserWidth, pos[1]-EraserWidth, EraserWidth<<1, EraserWidth<<1))
				rect = pygame.Surface((EraserWidth<<1, EraserWidth<<1), pygame.SRCALPHA, 32) 
				c = paper.avc
				rect.fill((c[0],c[1],c[2], 50)) 
				screen.blit(rect, (pos[0]-EraserWidth, pos[1]-EraserWidth)) 
			#pygame.draw.line(screen, BLACK, self.data[0], self.data[1], self.data[2])


class Book:
	def __init__(self, path, paperPath, Size, number):
		self.number = number
		self.current_number = 0
		self.path = path
		self.pages = [Page(path+"_"+str(i)+".log", paperPath, Size) for i in range(number)]
		self.current_page = None
		self.turn()
	def turn(self):
		self.current_page = self.pages[self.current_number]
	def event(self, e):
		page = self.current_page
		page.event(e)
		if page.isready() and e.type == pygame.KEYDOWN and (e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT):
			if e.key == pygame.K_LEFT:
				self.current_number = max(self.current_number - 1, 0)
			else:
				self.current_number = min(self.current_number + 1, self.number-1)
			#print("page to ", page_number)
			#page = paper.Page("page_"+str(page_number)+".log")
			self.turn()
	def show(self, screen):
		self.current_page.show(screen)
