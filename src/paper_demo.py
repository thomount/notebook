import pygame
import paper
import func
import pickle
import sys

BLACK = (0,0,0,1)
WHITE = (255,255,255)

pygame.init()
Size = (480, 640)
screen = pygame.display.set_mode(Size, 0, 32)
screen.fill(WHITE)

book = paper.Book("../data/page", "../mod/paper.jpg", Size, 8)

while True:
	screen.fill(WHITE)
	book.show(screen)
	pygame.display.update()
	for event in pygame.event.get():
		#print(event.type)
		if event.type == pygame.QUIT:
			# 接收到退出时间后退出程序
			exit()
		book.event(event)


