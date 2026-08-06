import pygame
import sys

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Startup City Builder")

clock = pygame.time.Clock()
GRID_SIZE =10
CELL_SIZE = 60

GRID_OFFSET_X = 50
GRID_OFFSET_Y = 50

selected_cell = None

running= True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            col = (mouse_x - GRID_OFFSET_X) // CELL_SIZE
            row = (mouse_y - GRID_OFFSET_Y) // CELL_SIZE

            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                selected_cell = (row, col)

                print(f"Clicked: Row {row}, Col {col}")
    screen.fill((30, 30, 40))

    #Draw grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):

            rect = pygame.Rect(
                GRID_OFFSET_X + col * CELL_SIZE,
                GRID_OFFSET_Y + row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE

            )

            pygame.draw.rect(screen, (100, 100, 120), rect, 1)

    if selected_cell:
        row, col = selected_cell
        rect = pygame.Rect(
            GRID_OFFSET_X + col* CELL_SIZE,
            GRID_OFFSET_Y + row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(screen, (0, 255, 0), rect, 3)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()
