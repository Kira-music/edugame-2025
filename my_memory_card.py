import sys
import random
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSpinBox, QPushButton, QVBoxLayout
from components.timer.timer import GameTimer

mwidth, mheight = 10, 10  
tsize = 100 


win_width = 700
win_height = 500


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

win_width = 700
win_height = 500

back = pygame.image.load('trava.jpg')
back = pygame.transform.scale(back, (mwidth * tsize, mheight * tsize))

brick = pygame.image.load('tree.jpg')
brick = pygame.transform.scale(brick, (tsize, tsize))

gamer = pygame.image.load('player.png')
gamer = pygame.transform.scale(gamer, (tsize, tsize))

spider = pygame.image.load('spider.png')
spider = pygame.transform.scale(spider, (tsize, tsize))

candy = pygame.image.load('candy.png')
candy = pygame.transform.scale(candy, (tsize, tsize))


# Классы 
class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.score = 0 

    def move(self, dx, dy, game_map):
        x = self.x + dx
        y = self.y + dy
        if 0 <= x < mwidth and 0 <= y < mheight and game_map[y][x] != 1:
            self.x, self.y = x, y

class Bot(Player):
    def move_random(self, game_map):
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(moves)
        for dx, dy in moves:
            x = self.x + dx
            y = self.y + dy
            if 0 <= x < mwidth and 0 <= y < mheight and game_map[y][x] != 1:
                self.x, self.y = x, y
                break
#создание карты
def generate_map(buildings, pops):
    game_map = [[0] * mwidth for _ in range(mheight)]

    for _ in range(buildings):
        x, y = random.randint(0, mwidth - 1), random.randint(0, mheight - 1)
        game_map[y][x] = 1

    item_positions = []
    for _ in range(pops):
        while True:
            x, y = random.randint(0, mwidth - 1), random.randint(0, mheight - 1)
            if game_map[y][x] == 0:
                game_map[y][x] = 2
                item_positions.append((x, y))
                break
    return game_map, item_positions

def start_game(buildings, pops, num_bots):
    pygame.init()
    screen = pygame.display.set_mode((mwidth * tsize, mheight * tsize))
    pygame.display.set_caption("Сбор предметов")

    
    game_map, item_positions = generate_map(buildings, pops)

    player = Player(random.randint(0, mwidth - 1), random.randint(0, mheight - 1), BLUE)


    bots = [Bot(random.randint(0, mwidth - 1), random.randint(0, mheight - 1), RED) for _ in range(num_bots)]
    pops = [Bot(random.randint(0, mwidth - 1), random.randint(0, mheight - 1), GREEN) for _ in range(pops)]
    clock = pygame.time.Clock()

    timer = GameTimer(duration=90)
    timer.init_timer()

    pygame.mixer.init()
    pygame.mixer.music.load('sound.mp3')
    pygame.mixer.music.play()
    
    lose = pygame.mixer.Sound('lose.mp3')
    win = pygame.mixer.Sound('win.mp3')


    running = True
    game_over = False
    game_win = False
    font = pygame.font.SysFont('arial', 48)
    score =0

    while running:
        screen.blit(back, (0, 0))
        if game_over:
            game_over_text = font.render("Вы были съедены пауком! Вы проиграли!", True, RED)
            lose.play()
            screen.blit(game_over_text, (90, 400))
            pygame.display.flip()
            pygame.time.delay(2000) 
            running = False
            break

        if game_win:
            win_text = font.render("Ура!Вы победили!", True, (255, 255, 255))
            win.play()
            screen.blit(win_text, (275, 400))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.move(0, -1, game_map)
                elif event.key == pygame.K_s:
                    player.move(0, 1, game_map)
                elif event.key == pygame.K_a:
                    player.move(-1, 0, game_map)
                elif event.key == pygame.K_d:
                    player.move(1, 0, game_map)

        for bot in bots:
            bot.move_random(game_map)

        for bot in bots:
            if player.x == bot.x and player.y == bot.y:
                game_over = True
                print('Hello')

        # счетчик
        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))


        for pop in pops:
            if player.x == pop.x and player.y == pop.y:
                print('hello')
                pops.remove(pop)
                score +=1
                print(f'счет: {score}')
                screen.blit(score_surface, (10, 10))
                if not pops:
                    game_win = True
                    pygame.display.flip()
                break

        for pos in item_positions[:]:
            if (player.x, player.y) == pos:
                player.score += 1
                item_positions.remove(pos)


        for bot in bots:
            if (bot.x, bot.y) == pos:
                bot.score += 1
                item_positions.remove(pos)
                continue


        # карта
        for y in range(mheight):
            for x in range(mwidth):
                rect = pygame.Rect(x * tsize, y * tsize, tsize, tsize)
                if game_map[y][x] == 1:
                    screen.blit(brick, rect)

        # Рисуем игрока и ботов
        screen.blit(gamer, (player.x * tsize, player.y * tsize))
        for bot in bots:
            screen.blit(spider, (bot.x * tsize, bot.y * tsize))

        for pop in pops:
            screen.blit(candy, (pop.x * tsize, pop.y * tsize))

        time_left = timer.get_time_left()
        time_surface = font.render(f"Time: {time_left}", True, (255, 255, 255))
        screen.blit(time_surface, (10, 50))

        if timer.is_finished():
            game_over = True
            game_over_text = font.render("Ваше время закончилось! Вы проиграли!", True, RED)

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройки карты")
        self.setGeometry(100, 100, 300, 200)

        self.label_buildings = QLabel("Количество построек:")
        self.spin_buildings = QSpinBox()
        self.spin_buildings.setRange(5, 20)
        self.spin_buildings.setValue(5)

        self.label_pops = QLabel("Количество предметов:")
        self.spin_pops = QSpinBox()
        self.spin_pops.setRange(1, 15)
        self.spin_pops.setValue(5)

        self.label_bots = QLabel("Количество ботов:")
        self.spin_bots = QSpinBox()
        self.spin_bots.setRange(1, 5)
        self.spin_bots.setValue(2)

        self.start_button = QPushButton("Начать игру")
        self.start_button.clicked.connect(self.start_game)

        layout = QVBoxLayout()
        layout.addWidget(self.label_buildings)
        layout.addWidget(self.spin_buildings)
        layout.addWidget(self.label_pops)
        layout.addWidget(self.spin_pops)
        layout.addWidget(self.label_bots)
        layout.addWidget(self.spin_bots)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

    def start_game(self):
        buildings = self.spin_buildings.value()
        pops = self.spin_pops.value()
        num_bots = self.spin_bots.value()
        self.close()
        start_game(buildings, pops, num_bots)

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добро пожаловать")
        self.setGeometry(100, 100, 600, 300)

        welcome_text = (
            "Добро пожаловать. Волшебный маг превратил вас в лилипута, "
            "и вы попали в мир насекомых. Вам нужно собрать все конфеты, при этом не попасться паукам, "
            "чтобы вернуть свой прежний облик. Быстрее нажимайте кнопку "
            "продолжить и выбирайте критерии игры!"
        )
        self.label = QLabel(welcome_text)
        self.label.setWordWrap(True)

        self.continue_button = QPushButton("Продолжить")
        self.continue_button.clicked.connect(self.on_continue)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.continue_button)
        self.setLayout(layout)
        
    def on_continue(self):
        self.close()
        self.settings_window = SettingsWindow()
        self.settings_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec_())
