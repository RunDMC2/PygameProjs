import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1200, 600

BLACK = (0, 0, 0)
GREY = (200, 200, 200)
WHITE = (255, 255, 255)

FPS = 60
clock = pygame.time.Clock()

window = pygame.display.set_mode((WIDTH, HEIGHT))
window.fill(BLACK)
load_surface = pygame.Surface((100, 100))

arial_font = pygame.font.SysFont("arial", 40)

all_circles = []
min_speed = 0.5
max_speed = 3


class Button:
    def __init__(self, x, y, text):
        self.width = 120
        self.height = 40
        self.x = x
        self.y = y
        self.text = text
        self.mx, self.my = pygame.mouse.get_pos()

    def onButton(self):
        self.mx, self.my = pygame.mouse.get_pos()
        if self.x <= self.mx <= self.x + self.width and self.y <= self.my <= self.y + self.height:
            return True
        else:
            return False

    def draw_rect(self):
        if self.onButton():
            color = GREY
        else:
            color = WHITE
        pygame.draw.rect(window, color, (self.x, self.y, self.width, self.height))
        text_rect = arial_font.render(self.text, True, BLACK)
        window.blit(text_rect, (self.x + 7, self.y - 4))


class Circle:
    def __init__(self):
        self.radius = random.randint(2, 50) * 2
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

        # gives a velocity not too slow or fast then randomly assigns direction
        self.change_x = random.uniform(min_speed, max_speed)
        self.change_y = random.uniform(min_speed, max_speed)

        if random.randint(1, 2) == 1:
            self.change_x = -self.change_x

        if random.randint(1, 2) == 1:
            self.change_y = -self.change_y

        # assigns position relative to velocity direction
        temp_rand = random.randint(1, 4)

        if temp_rand == 1:  # left
            self.pos_x = 0 - self.radius * 2
            self.pos_y = random.randint(0, HEIGHT)

        elif temp_rand == 2:  # right
            self.pos_x = WIDTH
            self.pos_y = random.randint(0, HEIGHT)

        elif temp_rand == 3:  # top
            self.pos_x = random.randint(0, WIDTH)
            self.pos_y = 0 - self.radius * 2

        elif temp_rand == 4:  # bottom
            self.pos_x = random.randint(0, WIDTH) 
            self.pos_y = HEIGHT

        self.rect = pygame.rect.Rect((self.pos_x, self.pos_y, self.radius * 2, self.radius * 2))


class Player:
    def __init__(self):
        self.radius = 11
        self.pos_x, self.pos_y = pygame.mouse.get_pos()

        rect_tuple = (self.pos_x - self.radius, self.pos_y - self.radius, self.radius * 2, self.radius * 2)
        self.rect = pygame.rect.Rect(rect_tuple)

    def get_pos(self):
        self.pos_x, self.pos_y = pygame.mouse.get_pos()

        rect_tuple = (self.pos_x - self.radius, self.pos_y - self.radius, self.radius * 2, self.radius * 2)
        self.rect = pygame.rect.Rect(rect_tuple)

        return self.pos_x, self.pos_y


class Game:
    def __init__(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        pygame.mouse.set_visible(False)
        self.lose = False
        self.win = False
        self.score = 0
        self.playing = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if self.lose or self.win:
                    if restart_button.onButton():
                        self.playing = False

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def draw(self):
        window.fill(BLACK)

        # player
        if not self.lose:
            pygame.draw.circle(window, WHITE, player.get_pos(), player.radius)

        # circles
        for circle in all_circles[:]:
            center_tuple = (circle.rect.x + circle.radius, circle.rect.y + circle.radius)
            pygame.draw.circle(window, circle.color, center_tuple, circle.radius)

            # check collision
            if not self.lose:
                if pygame.sprite.collide_circle(circle, player):
                    if circle.radius < player.radius:
                        player.radius += 2
                        all_circles.remove(circle)
                        self.score += int(circle.radius / 2)
                        del circle
                        continue

                    else:
                        # lose
                        self.lose = True
                        pygame.mouse.set_visible(True)

            circle.rect.x += circle.change_x
            circle.rect.y += circle.change_y

            # check if off-screen
            if circle.rect.x < 0 - circle.radius * 2 or circle.rect.x > WIDTH:
                all_circles.remove(circle)
                del circle

            elif circle.rect.y < 0 - circle.radius * 2 or circle.rect.y > HEIGHT:
                all_circles.remove(circle)
                del circle

            text_rect = arial_font.render(f"{self.score}", True, WHITE)
            window.blit(text_rect, (WIDTH - 75, 20))

            if self.lose:
                temp_str = f"Mass: {self.score}"
                text_rect = arial_font.render("You Got Dead", True, WHITE)
                window.blit(text_rect, (WIDTH / 2 - 100, HEIGHT / 2 - 150))
                text_rect = arial_font.render(f"{temp_str : ^11}", True, WHITE)
                window.blit(text_rect, (WIDTH / 2 - 75, HEIGHT / 2 - 70))
                restart_button.draw_rect()

        if self.win:
            # win condition
            window.fill(WHITE)
            text_rect = arial_font.render(f"You ate the universe.", True, BLACK)
            window.blit(text_rect, (WIDTH / 2 - 140, HEIGHT / 2 - 70))
            pygame.mouse.set_visible(True)
            pygame.draw.rect(window, BLACK, (WIDTH / 2 - 61, HEIGHT / 2 - 21, 122, 42))
            restart_button.draw_rect()

    def main_loop(self):
        self.events()
        self.draw()


if __name__ == "__main__":

    while True:
        all_circles.clear()
        g = Game()
        player = Player()
        restart_button = Button(WIDTH / 2 - 60, HEIGHT / 2 - 20, "Restart")

        while g.playing:
            g.main_loop()
            pygame.display.update()
            clock.tick(FPS)

            if len(all_circles) >= 40:
                continue

            if g.score < 15000:
                all_circles.append(Circle())
                continue

            g.win = True
