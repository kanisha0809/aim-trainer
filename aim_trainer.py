import math
import random
import time
import pygame
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_SPAWN_INTERVAL = 400
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30

BACKGROUND_COLOR = (0, 25, 40)
MAX_LIVES = 3
TOP_BAR_HEIGHT = 50

FONT = pygame.font.SysFont("comicsans", 24)


class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.is_growing = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.is_growing = False

        if self.is_growing:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(window, self.SECOND_COLOR,
                           (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(window, self.SECOND_COLOR,
                           (self.x, self.y), self.size * 0.4)

    def check_collision(self, x, y):
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return distance <= self.size


def draw_window(window, targets):
    window.fill(BACKGROUND_COLOR)

    for target in targets:
        target.draw(window)


def format_time(seconds):
    milliseconds = math.floor(int(seconds * 1000 % 1000) / 100)
    seconds = int(round(seconds % 60, 1))
    minutes = int(seconds // 60)

    return f"{minutes:02d}:{seconds:02d}.{milliseconds}"


def draw_top_bar(window, elapsed_time, targets_hit, misses):
    pygame.draw.rect(window, "grey", (0, 0, SCREEN_WIDTH, TOP_BAR_HEIGHT))
    time_label = FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "black")

    speed = round(targets_hit / elapsed_time, 1)
    speed_label = FONT.render(f"Speed: {speed} t/s", 1, "black")

    hits_label = FONT.render(f"Hits: {targets_hit}", 1, "black")

    lives_label = FONT.render(f"Lives: {MAX_LIVES - misses}", 1, "black")

    window.blit(time_label, (5, 5))
    window.blit(speed_label, (200, 5))
    window.blit(hits_label, (450, 5))
    window.blit(lives_label, (650, 5))


def end_game_screen(window, elapsed_time, targets_hit, clicks):
    window.fill(BACKGROUND_COLOR)
    time_label = FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "white")

    speed = round(targets_hit / elapsed_time, 1)
    speed_label = FONT.render(f"Speed: {speed} t/s", 1, "white")

    hits_label = FONT.render(f"Hits: {targets_hit}", 1, "white")

    accuracy = round(targets_hit / clicks * 100, 1)
    accuracy_label = FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    window.blit(time_label, (get_middle(time_label), 100))
    window.blit(speed_label, (get_middle(speed_label), 200))
    window.blit(hits_label, (get_middle(hits_label), 300))
    window.blit(accuracy_label, (get_middle(accuracy_label), 400))

    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()


def get_middle(surface):
    return SCREEN_WIDTH / 2 - surface.get_width() / 2


def main():
    running = True
    targets = []
    clock = pygame.time.Clock()

    targets_hit = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_SPAWN_INTERVAL)

    while running:
        clock.tick(60)
        clicked = False
        mouse_position = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, SCREEN_WIDTH - TARGET_PADDING)
                y = random.randint(
                    TARGET_PADDING + TOP_BAR_HEIGHT, SCREEN_HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if clicked and target.check_collision(*mouse_position):
                targets.remove(target)
                targets_hit += 1

        if misses >= MAX_LIVES:
            end_game_screen(WINDOW, elapsed_time, targets_hit, clicks)

        draw_window(WINDOW, targets)
        draw_top_bar(WINDOW, elapsed_time, targets_hit, misses)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
