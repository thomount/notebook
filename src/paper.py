import pygame
import pickle
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

class Note:
	pass
class Paper:
	pass
class Page:
	def __init__(self):
		self.notes = []
		self.paper = Paper()
	def show(self, screen):
		for note in self.notes:
			note.show(screen)

	def save(self, file):
		pickle.dump(self.notes, file)
		file.close()
	def load(self, file):
		try:
			self.notes = pickle.load(file)
			file.close()	
		except:
			pass	
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

