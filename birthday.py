import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Happy Birthday NEELA ❤️")

font_big = pygame.font.SysFont("Arial", 60, bold=True)
font_small = pygame.font.SysFont("Arial", 30)

# Uncomment after adding a file named birthday.mp3
# pygame.mixer.music.load("birthday.mp3")
# pygame.mixer.music.play(-1)

hearts = []

for _ in range(35):
    hearts.append([
        random.randint(0, WIDTH),
        random.randint(HEIGHT, HEIGHT + 500),
        random.randint(2, 5)
    ])

fireworks = []

clock = pygame.time.Clock()

running = True
frame = 0

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((20, 10, 40))

    # Floating hearts
    for heart in hearts:
        pygame.draw.circle(screen, (255, 80, 120), (heart[0]-5, heart[1]), 10)
        pygame.draw.circle(screen, (255, 80, 120), (heart[0]+5, heart[1]), 10)
        pygame.draw.polygon(screen,
                            (255,80,120),
                            [(heart[0]-15,heart[1]),
                             (heart[0]+15,heart[1]),
                             (heart[0],heart[1]+22)])

        heart[1] -= heart[2]

        if heart[1] < -20:
            heart[1] = HEIGHT + random.randint(20,300)
            heart[0] = random.randint(0, WIDTH)

    # Cake
    pygame.draw.rect(screen,(255,228,196),(300,350,300,180))
    pygame.draw.rect(screen,(255,182,193),(300,330,300,25))

    # Candles
    for x in [360,450,540]:
        pygame.draw.rect(screen,(255,255,255),(x,280,8,50))
        flame = (255, random.randint(150,255), 0)
        pygame.draw.circle(screen, flame, (x+4,270),7)

    # Fireworks
    if frame % 25 == 0:
        fireworks.append([
            random.randint(100,800),
            random.randint(50,250),
            random.randint(20,40),
            (random.randint(0,255),
             random.randint(0,255),
             random.randint(0,255))
        ])

    for fw in fireworks[:]:
        for angle in range(0,360,15):
            x = fw[0] + math.cos(math.radians(angle))*fw[2]
            y = fw[1] + math.sin(math.radians(angle))*fw[2]
            pygame.draw.circle(screen,fw[3],(int(x),int(y)),3)

        fw[2] += 2

        if fw[2] > 80:
            fireworks.remove(fw)

    title = font_big.render("🎉 HAPPY BIRTHDAY 🎉", True, (255,255,0))
    screen.blit(title,(150,40))

    name = font_big.render("NEELA ❤️",True,(255,100,180))
    screen.blit(name,(300,120))

    msg = font_small.render(
        "May your life be filled with happiness, success and endless smiles!",
        True,
        (255,255,255)
    )

    screen.blit(msg,(70,560))

    pygame.display.flip()
    frame += 1

pygame.quit()
