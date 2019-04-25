import pygame
import random
import PyGameNextGen as ng
from PyGameNextGen import Stats

import warnings
warnings.filterwarnings("ignore")

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
yellow = (255, 255, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('NOVA SIMULATION')
clock = pygame.time.Clock()


def text_objects(text, font, color=white):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def md_game_name(text):
    text_type = pygame.font.SysFont('times new roman', 35)
    TextSurf, TextRect = text_objects(text, text_type)
    gameDisplay.blit(TextSurf, (display_width * .31, display_height * .01))

    pygame.display.update()


def md_key_trait(text):
    text_type = pygame.font.SysFont('times new roman', 22)
    TextSurf, TextRect = text_objects(text, text_type, yellow)
    gameDisplay.blit(TextSurf, (10, display_height * .07))

    pygame.display.update()


def md_weights_summary(text):
    text_type = pygame.font.SysFont('times new roman', 20)
    TextSurf, TextRect = text_objects(text, text_type)
    gameDisplay.blit(TextSurf, (10, display_height * .11))

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
    text_type = pygame.font.SysFont('times new roman', 31)
    TextSurf, TextRect = text_objects(text, text_type, yellow)
    gameDisplay.blit(TextSurf, (display_width * .10, display_height * .25))

    pygame.display.update()


def md_species(text):
    text_type = pygame.font.SysFont('times new roman', 45)
    TextSurf, TextRect = text_objects(text, text_type)
    gameDisplay.blit(TextSurf, (display_width * .13, display_height * .33))

    pygame.display.update()


def md_summary(text, i):
    text_type = pygame.font.SysFont('times new roman', 45)
    TextSurf, TextRect = text_objects(text, text_type)
    gameDisplay.blit(TextSurf, (display_width * .13, display_height * (.42 + ((i * 9) * .01))))

    pygame.display.update()


gameExit = False
print_every = 20
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

        md_game_name("NOVA SIMULATION V1")

        md_key_trait(key_trait)
        md_weights_summary(print_weights)
        md_gen(f"Gen {generation} |")
        md_dom_species(dom_species)
        md_counts(counts)

        max_len = 0
        for trait2 in traits:
            if max_len < len(trait2):
                max_len = len(trait2)

        md_species(" " * 4 + line1)
        print(line3)
        md_summary((traits[0] + " " * (11 - len(traits[0])) + line3[0]), 0)
        md_summary((traits[1] + " " * (17 - len(traits[1])) + line3[1]), 1)
        md_summary((traits[2] + " " * (14 - len(traits[2])) + line3[2]), 2)
        md_summary((traits[3] + " " * (13 - len(traits[3])) + line3[3]), 3)
        md_summary((traits[4] + " " * (12 - len(traits[4])) + line3[4]), 4)
        md_summary((traits[5] + " " * (11 - len(traits[5])) + line3[5]), 5)

    generation += 1

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
