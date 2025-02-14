import pygame
import random
import math

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Click to Create Balls")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

BALL_RADIUS = 15
GRAVITY = 0.5
DAMPING = 0.8

balls = []

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        self.velocity_y += GRAVITY
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.velocity_y = -abs(self.velocity_y) * DAMPING
            self.velocity_x *= DAMPING

        if self.x - self.radius < 0:
            self.x = self.radius
            self.velocity_x = abs(self.velocity_x) * DAMPING
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.velocity_x = -abs(self.velocity_x) * DAMPING

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def collide_balls(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx**2 + dy**2)
    if distance < ball1.radius + ball2.radius:
        # Calculate angle of collision
        angle = math.atan2(dy, dx)
        # Calculate total mass
        total_mass = 1 + 1  # Assuming equal mass for simplicity

        # Calculate velocities along the line of collision
        v1 = (ball1.velocity_x * math.cos(angle) + ball1.velocity_y * math.sin(angle))
        v2 = (ball2.velocity_x * math.cos(angle) + ball2.velocity_y * math.sin(angle))

        # Calculate new velocities after collision (1D collision formula)
        new_v1 = (v1 * (1 - 1) + 2 * 1 * v2) / total_mass
        new_v2 = (v2 * (1 - 1) + 2 * 1 * v1) / total_mass

        # Update velocities in x and y directions
        ball1.velocity_x += (new_v1 - v1) * math.cos(angle)
        ball1.velocity_y += (new_v1 - v1) * math.sin(angle)
        ball2.velocity_x += (new_v2 - v2) * math.cos(angle)
        ball2.velocity_y += (new_v2 - v2) * math.sin(angle)

        # Separate the balls to prevent sticking
        overlap = 0.5 * (ball1.radius + ball2.radius - distance)
        ball1.x -= overlap * math.cos(angle)
        ball1.y -= overlap * math.sin(angle)
        ball2.x += overlap * math.cos(angle)
        ball2.y += overlap * math.sin(angle)


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                new_ball = Ball(x, y)
                balls.append(new_ball)

    for i in range(len(balls)):
        balls[i].update()
        for j in range(i + 1, len(balls)):
            collide_balls(balls[i], balls[j])

    screen.fill(BLACK)

    for ball in balls:
        ball.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()