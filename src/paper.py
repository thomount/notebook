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
	