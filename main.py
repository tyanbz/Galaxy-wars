import pygame
from pygame.locals import *
import random
import math
from pygame import mixer #модуль работает со звуками и музыкой

#clock = pygame.time.Clock()
WINDOW_SIZE = (800,600)
screen = pygame.display.set_mode(WINDOW_SIZE) #инициализация окна
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
# добавляем фоны
# https://freepik.com
background = pygame.image.load("bg.png")

pygame.init() # инициализация модуля

pygame.display.set_caption("Галактический войны")

# фоновая музыка
mixer.music.load("background.wav")
mixer.music.play(-1)

# создаем игрока
# размер персонажа 64x64
# https://editor.0lik.ru/photoshop-online-new.html
player_img = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# создаем пришельцев
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
	#делаем разных пришельцев
	if i%2 == 0:
		enemy_img.append(pygame.image.load("enemy1.png"))
	else:
		enemy_img.append(pygame.image.load("enemy2.png"))

	enemyX.append(random.randint(0, 735))
	enemyY.append(random.randint(50, 150))
	enemyX_change.append(2)
	enemyY_change.append(40)

# создаем пулю размером 32х32
# состояния пули:
# ready - пулю не видно
# fire - пуля летит во врага
bullet_img = pygame.image.load("bullet.png")
bulletX = 0 
bulletY = 480
bulletX_change = 0 
bulletY_change = 6
bullet_state = "ready"

# рекорды
# скачать шрифт: http://dafont.com/
score_value = 0
font = pygame.font.Font("Chocolate-Valentine.otf", 40)
textX = 10
textY = 10

# game over текст
game_over_font = pygame.font.Font("Chocolate-Valentine.otf", 10)

def game_over_text():
	game_over_font = font.render("GAME OVER", True, (0, 191, 255)) # функция отрисовывает текст на экране
	screen.blit(game_over_font, (200, 250))

def show_score(x,y):
	score = font.render("Score: " + str(score_value), True, (0, 191, 255)) # функция отрисовывает текст на экране
	screen.blit(score, (x, y))

# запускаем персонажа
def player(x, y):
	screen.blit(player_img, (x, y)) # появиться на экране

# запускаем 1 пришельца
# размер должен быть 64х64
def enemy(x, y, i):
	screen.blit(enemy_img[i], (x, y)) # появиться на экране

# запуск пули
def bullet_fire(x, y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bullet_img, (x+16, y+6)) 

# делаем попадение
# расстояние между точками и центром:
# под корнем [(x2 - x1)кв + (y2 - y1)кв]
def isCollision(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
	if distance < 27:
		return True
	else:
		return False

# главный игровой цикл
isPlay = True
while isPlay: 
	# заливка фона окна
	# https://colorscheme.ru/html-colors.html
	screen.fill((25, 25, 112))
	# обновляем фон картинкой
	screen.blit(background, (0,0))

	# все события клавиатуры находятся в этом цикле
	for event in pygame.event.get():
		if event.type == QUIT:
			isPlay = False

		# проверяем события нажатий в стороны и стрелял
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -5
				#print("Нажата стрелка влево. Самолет свинулся влево.")
			if event.key == pygame.K_RIGHT:
				playerX_change = 5
				#print("Нажата стрелка вправо. Самолет свинулся вправо.")
			if event.key == pygame.K_UP:
				playerY_change = -3
				#print("Нажата стрелка вверх. Самолет свинулся вверх.")
			if event.key == pygame.K_DOWN:
				playerY_change = 3
				#print("Нажата стрелка вниз. Самолет свинулся вниз.")
			if event.key == pygame.K_SPACE:
				if bullet_state is "ready":
					# создаем звук пули
					bullet_sound = mixer.Sound("laser.wav")
					bullet_sound.play()
					# получаем текущие координаты пули
					bulletX = playerX
					bullet_fire(bulletX, bulletY)
					print("Огонь.")
				else: print("Пуля уже летит. Пробел не работает.")

		# проверяем события если кнопки отжаты
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == K_RIGHT:
				playerX_change = 0
				playerY_change = 0
				print("Кнопки отжаты")

	# смещаем персонажа по X
	playerX += playerX_change
	playerY += playerY_change
	# делаем ограничения по границам экрана для персонажа
	if playerX <= 0:
		playerX = 0
	elif playerX >= 736:
		playerX = 736
	if playerY <= 300:
		playerY = 300
	elif playerY >= 530:
		playerY = 530

	# множественное передвижение пришельцев
	for i in range(num_of_enemies):
		# game over
		if enemyY[i] > 150:
			# опускаем всех прицельцев
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over_text()
			break
		# смещаем пришельцев по X
		enemyX[i] += enemyX_change[i]
		# делаем ограничения по границам экрана для пришельца
		if enemyX[i] <= 0:
			enemyX_change[i] = 2
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 736:
			enemyX_change[i] = -2
			enemyY[i] += enemyY_change[i]

		# дистанция
		collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
		if collision == True:
			# создаем звук попадания
			explosion_sound = mixer.Sound("explosion.wav")
			explosion_sound.play()
			bulletY = playerY
			bullet_state = "ready"
			score_value += 1
			print("Убитых прицельцев:", score_value)
			# создаем нового пришельца
			enemyX[i] = random.randint(0, 735)
			enemyY[i] = random.randint(50, 150)

		# запускаем пришельцев
		enemy(enemyX[i], enemyY[i], i)

	# делаем проверку состояния пули
	if bulletY <= 0:
		bulletY = playerY
		bullet_state = "ready"

	if bullet_state is "fire":
		bullet_fire(bulletX, bulletY)
		bulletY -= bulletY_change
	
	# запускаем персонажа		
	player(playerX, playerY)
	# показываем рекорды
	show_score(textX, textX)
	# обновление экрана
	pygame.display.update()