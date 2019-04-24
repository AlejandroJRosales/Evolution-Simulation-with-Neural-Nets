import pygame
import random
import PyGameNextGen as ng
from PyGameNextGen import Stats

pygame.init()

pop_n = [10, 10, 10]  # Number of: Humans, Drackonians, Gritiss
weights = [random.random() for i in range(5)]
stats = Stats()
key_trait, print_weights = stats.weights_summary(weights)
generation = 0
population = ng.generate_population(pop_n)

traits = [
            'Score',
            'ft',
            'lbs',
            'IQ',
            'Speed',
            'Power'
        ]

display_width = 1000
display_height = int(display_width * .75)

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('MiniPop')
clock = pygame.time.Clock()


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def md_game_name(text):
    text_type = pygame.font.SysFont('times new roman', 35)
    TextSurf, TextRect = text_objects(text, text_type)
    gameDisplay.blit(TextSurf, (display_width * .4, display_height * .02))

    pygame.display.update()


def md_key_trait(text):
    text_type = pygame.font.SysFont('times new roman', 20)
    TextSurf, TextRect = text_objects(text, text_type)
    gameDisplay.blit(TextSurf, (10, display_height * .07))

    pygame.display.update()


def md_weights_summary(text):
    text_type = pygame.font.SysFont('times new roman', 20)
    TextSurf, TextRect = text_objects(text, text_type)
    gameDisplay.blit(TextSurf, (10, display_height * .10))

    pygame.display.update()


def md_gen(text):
    text_type = pygame.font.SysFont('times new roman', 20)
    TextSurf, TextRect = text_objects(text, text_type)
    gameDisplay.blit(TextSurf, (10, display_height * .15))

    pygame.display.update()


def md_dom_species(text):
    text_type = pygame.font.SysFont('times new roman', 20)
    TextSurf, TextRect = text_objects(text, text_type)
    gameDisplay.blit(TextSurf, (10, display_height * .18))

    pygame.display.update()


def md_counts(text):
    text_type = pygame.font.SysFont('times new roman', 20)
    TextSurf, TextRect = text_objects(text, text_type)
    gameDisplay.blit(TextSurf, (10, display_height * .21))

    pygame.display.update()


def md_species(text):
    text_type = pygame.font.SysFont('times new roman', 45)
    TextSurf, TextRect = text_objects(text, text_type)
    gameDisplay.blit(TextSurf, (display_width * .17, display_height * .28))

    pygame.display.update()


def md_summary(text, i):
    text_type = pygame.font.SysFont('times new roman', 45)
    TextSurf, TextRect = text_objects(text, text_type)
    gameDisplay.blit(TextSurf, (display_width * .17, display_height * (.35 + ((i * 9) * .01))))

    pygame.display.update()


gameExit = False
print_every = 10
while not gameExit:
    population = ng.evolve(population, weights)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                quit()

    if generation % print_every == 0 or generation == 0:
        dom_species, counts = stats.counting(population)
        line1, line2, line3 = stats.creatures_summary(population, weights)

        gameDisplay.fill(black)

        md_game_name("MiniPop v3")

        md_key_trait(key_trait)
        md_weights_summary(print_weights)
        md_gen(f"Gen {generation} |")
        md_dom_species(dom_species)
        md_counts(counts)

        md_species(" " * 4 + line1)
        for i in range(len(line3)):
            md_summary((traits[i] + " " * (len("Strngth") - len(traits[i])) + line3[i]), i)

    generation += 1

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
