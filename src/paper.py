import pygame
import pickle
import sys
import func
BLACK = (0,0,0)
WHITE = (255,255,255)
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
	pass
class Page:
	def __init__(self, path):
		self.notes = []
		self.paper = Paper()
		self.status = Status()
		#self.file = open()
		self.path = path
		self.load()
		self.tick = 0

	def show(self, screen):
		self.tick += 1
		for note in self.notes:
			note.show(screen)

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
					#print('clicked')
					self.status.type = "line"
					self.status.clicked = True
					self.status.last = [e.pos]
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
			if self.status.clicked == True and self.status.type == "line":
				self.status.log.data["width"].append(func.getwidth(self.tick-self.status.last_t))
				self.status.log.data["line"].append(e.pos)
				self.status.last_t = self.tick
				#print('released')
				self.status.clicked = False
				self.save()
				#page.save(open('log', 'wb'))
			if self.status.clicked == True and self.status.type == "word":
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
		if e.type == pygame.MOUSEMOTION:
			if self.status.clicked == True and self.status.type == "line":
				if func.dist(e.pos, self.status.last[-1]) > 5:
					#print('drawing', status.last[-1], event.pos)
					self.status.log.data["width"].append(func.getwidth(self.tick-self.status.last_t))
					self.status.log.data["line"].append(e.pos)
					self.status.last_t = self.tick

class Log:
	def __init__(self):
		self.type = None
		self.data = []
	def show(self, screen):
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


class Book:
	def __init__(self, path, number):
		self.number = number
		self.current_number = 0
		self.path = path
		self.pages = [Page(path+"_"+str(i)+".log") for i in range(number)]
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
