import pygame
import os
import math
import random
from PyDictionary import PyDictionary


pygame.init()

# setting up a window
HEIGHT, WIDTH = 500, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")


#colors 
WHITE = (255,255,255)
BLACK = (0,0,0)

#loading images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

#game variable
hangman_status = 0
words = ["SCIENCE", "PYTHON", "DEVELOPER"]
word = random.choice(words)
guessed = []
try:
    meaning = PyDictionary(word)
    meaning = meaning.getMeanings()[word]['Noun'][0]
    print(meaning)
except:
    pass

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y,  chr(65 + i), True])


def draw():
	window.fill(WHITE)

	#title
	text = TITLE_FONT.render("HANGMAN", 1, BLACK)
	window.blit(text, (WIDTH/2 - text.get_width()/2, 20))

	#displaying words
	display_word = ""
	for letter in word:
		if letter in guessed:
			display_word += letter + " "
		else:
			display_word += "_ "
	
	text = WORD_FONT.render(display_word, 1, BLACK)
	window.blit(text, (400, 150))

	#circles
	for i in letters:
		x , y, letter, visible = i
		if visible:
			pygame.draw.circle(window, BLACK, (x,y), RADIUS, 3)
			text = LETTER_FONT.render(letter, 1, BLACK)
			window.blit(text, (x - text.get_width()//2, y - text.get_height()//2))
	
	window.blit(images[hangman_status], (150, 100))
	pygame.display.update()





#display message
def display_message(message):
	pygame.time.delay(1000)
	window.fill(WHITE)
	text = WORD_FONT.render(message, 1, BLACK)
	window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
	pygame.display.update()
	pygame.time.delay(3000)


clock = pygame.time.Clock()
run = True

# game loop
while run:
	clock.tick(60)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()
			exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			mx , my = pygame.mouse.get_pos()
			for i in letters:
				x , y , letter, visible = i
				if visible:
					d = math.sqrt((x - mx)**2 + (y - my)**2)
					if d < RADIUS:
						i[3] = False
						guessed.append(letter)
						if letter not in word:
							hangman_status += 1
		
		draw()
		won = True
		for letter in word:
			if letter not in guessed:
				won = False
				break
		
		if won:
			display_message("You WON!")
			run = False
			break
		
		if hangman_status == 6:
			display_message("You LOST!")
			run = False
			break
						

pygame.quit()
