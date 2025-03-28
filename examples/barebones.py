import pygame
import pygame_zer

pygame.init()
screen = pygame.display.set_mode((1280, 720))
zerdriver = pygame_zer.PygameDriver(screen)

pygame_zer.Circle(zerdriver, (100, 100), 25, fill="red")
pygame_zer.Circle(zerdriver, (200, 250), 15, fill="green")
pygame_zer.Circle(zerdriver, (200, 275), 15, fill="green", outline="red", outlineWidth=2)
pygame_zer.Rect(zerdriver, (300, 350, 15, 35))
pygame_zer.Rect(zerdriver, (550, 600, 75, 50), outline="blue")
pygame_zer.Line(zerdriver, (500, 400), (200, 780))

running = True
while running:
    for event in pygame.event.get():
        if zerdriver.handle_event(event):
            continue
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50, 50, 50))

    zerdriver.draw()

    pygame.display.flip()

pygame.quit()
