import pygame
import sys
from buildings.building_data import building_costs, building_names, building_income
pygame.init()

# -----------------------------
# GAME WINDOW
# -----------------------------

from config.settings import WIDTH, HEIGHT, GRID_SIZE, CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, HUD_BG, HUD_BORDER, HUD_TEXT, HUD_SECONDARY, FPS, GAME_TITLE, FONT_SIZE, SMALL_FONT_SIZE, BUTTON_FONT_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_TITLE)

clock = pygame.time.Clock()


# -----------------------------
# FONTS
# -----------------------------

font = pygame.font.SysFont(None, FONT_SIZE)
small_font = pygame.font.SysFont(None, SMALL_FONT_SIZE)
button_font = pygame.font.SysFont(None, BUTTON_FONT_SIZE)

# -----------------------------
# HUD COLORS
# -----------------------------

# -----------------------------
# GRID
# -----------------------------

from config.settings import WIDTH, HEIGHT, GRID_SIZE, CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y

# Reusable alpha surface for geometric 2.5D building shadows
building_shadow_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
campus_shadow_surf = pygame.Surface((CELL_SIZE * 2, CELL_SIZE * 2), pygame.SRCALPHA)
datacenter_shadow_surf = pygame.Surface((CELL_SIZE * 2, CELL_SIZE * 2), pygame.SRCALPHA)

# 0 = Empty
# 1 = Startup Office
# 2 = Marketing Hub
# 3 = R&D Lab
# 4 = Road
# 5 = Pathway
# 6 = Trees
# 7 = Streetlight
# 8 = Bench
# 9 = Flower Bed
# 10 = Tech Campus (2x2)
# 11 = Cloud Data Center (2x2)

grid = [
    [0 for _ in range(GRID_SIZE)]
    for _ in range(GRID_SIZE)
]

# Track multi-tile building origins: (row, col) -> (root_row, root_col)
building_origins = {}

# Configurable building footprint dimensions: building_id -> (width_in_tiles, height_in_tiles)
building_sizes = {
    1: (1, 1),
    2: (1, 1),
    3: (1, 1),
    4: (1, 1),
    5: (1, 1),
    6: (1, 1),
    7: (1, 1),
    8: (1, 1),
    9: (1, 1),
    10: (2, 2),
    11: (2, 2)
}

# -----------------------------
# PLAYER
# -----------------------------

money = 1000

employees = 0
users = 0
innovation = 0
reputation = 0
total_city_income = 0

selected_cell = None
current_building = 1

# -----------------------------
# INCOME SYSTEM
# -----------------------------

income_timer = 0
income_interval = 300

# -----------------------------
# BUILDING INFORMATION
# -----------------------------






building_employees = {
    1: 5,
    2: 0,
    3: 2,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 15,
    11: 8
}

building_users = {
    1: 0,
    2: 20,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 50,
    11: 120
}

building_innovation = {
    1: 1,
    2: 0,
    3: 10,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 20,
    11: 30
}

building_reputation = {
    1: 0,
    2: 2,
    3: 1,
    4: 0,
    5: 0,
    6: 2,
    7: 1,
    8: 1,
    9: 2,
    10: 5,
    11: 4
}

building_colors = {
    1: (0, 150, 255),
    2: (0, 200, 100),
    3: (180, 80, 220),
    4: (70, 70, 80),
    5: (195, 200, 195),
    6: (60, 150, 70),
    7: (240, 220, 100),
    8: (160, 110, 60),
    9: (230, 90, 140),
    10: (70, 130, 180),
    11: (40, 50, 65)
}

# -----------------------------
# BUILD MENU BUTTONS
# -----------------------------

office_button = pygame.Rect(680, 550, 135, 70)
marketing_button = pygame.Rect(835, 550, 135, 70)
rd_button = pygame.Rect(680, 630, 135, 60)

# -----------------------------
# GAME LOOP
# -----------------------------

running = True

while running:

    # -------------------------
    # INCOME SYSTEM
    # -------------------------

    income_timer += 1

    if income_timer >= income_interval:

        income_timer = 0

        total_income = 0

        for row in range(GRID_SIZE):

            for col in range(GRID_SIZE):

                building = grid[row][col]

                if building != 0:

                    # Count income strictly once at root tile for multi-tile buildings
                    if building_origins.get((row, col), (row, col)) == (row, col):
                        total_income += building_income.get(building, 0)

        total_city_income = total_income
        money += total_income

    # -------------------------
    # EVENTS
    # -------------------------

    for event in pygame.event.get():

        # Close game
        if event.type == pygame.QUIT:

            running = False

        # ---------------------
        # KEYBOARD
        # ---------------------

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:

                current_building = 1
                print("Selected: Startup Office")

            elif event.key == pygame.K_2:

                current_building = 2
                print("Selected: Marketing Hub")

            elif event.key == pygame.K_3:

                current_building = 3
                print("Selected: R&D Lab")

            elif event.key == pygame.K_4:

                current_building = 4
                print("Selected: Road")

            elif event.key == pygame.K_5:

                current_building = 5
                print("Selected: Pathway")

            elif event.key == pygame.K_6:

                current_building = 6
                print("Selected: Trees")

            elif event.key == pygame.K_7:

                current_building = 7
                print("Selected: Streetlight")

            elif event.key == pygame.K_8:

                current_building = 8
                print("Selected: Bench")

            elif event.key == pygame.K_9:

                current_building = 9
                print("Selected: Flower Bed")

            elif event.key == pygame.K_0:

                current_building = 10
                print("Selected: Tech Campus (2x2)")

            elif event.key == pygame.K_c or event.key == pygame.K_d:

                current_building = 11
                print("Selected: Cloud Data Center (2x2)")

        # ---------------------
        # MOUSE
        # ---------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos
            # Check Build Menu buttons
            if office_button.collidepoint(mouse_x, mouse_y):
                current_building = 1
                print("Selected: Startup Office")

            elif marketing_button.collidepoint(mouse_x, mouse_y):
                current_building = 2
                print("Selected: Marketing Hub")

            elif rd_button.collidepoint(mouse_x, mouse_y):
                current_building = 3
                print("Selected: R&D Lab")

            col = (mouse_x - GRID_OFFSET_X) // CELL_SIZE
            row = (mouse_y - GRID_OFFSET_Y) // CELL_SIZE

            # Check if clicked inside grid
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:

                selected_cell = (row, col)

                b_w, b_h = building_sizes.get(current_building, (1, 1))

                # Footprint boundary validation
                if row + b_h <= GRID_SIZE and col + b_w <= GRID_SIZE:

                    # Overlap validation across full footprint
                    can_place = True
                    for r in range(row, row + b_h):
                        for c in range(col, col + b_w):
                            if grid[r][c] != 0:
                                can_place = False
                                break
                        if not can_place:
                            break

                    if can_place:
                        cost = building_costs[current_building]

                        # Check money
                        if money >= cost:

                            # Place building across entire footprint and register origins
                            for r in range(row, row + b_h):
                                for c in range(col, col + b_w):
                                    grid[r][c] = current_building
                                    building_origins[(r, c)] = (row, col)

                            # Remove building cost strictly once
                            money -= cost

                            # Update startup statistics strictly once
                            employees += building_employees[current_building]
                            users += building_users[current_building]
                            innovation += building_innovation[current_building]
                            reputation += building_reputation[current_building]
                            total_city_income += building_income[current_building]

                            print(
                                f"Built {building_names[current_building]}"
                            )

                        else:

                            print("Not enough money!")

                    else:

                        print("Cannot build: space already occupied!")

                else:

                    print("Cannot build: building footprint extends outside grid!")

    # -------------------------
    # BACKGROUND
    # -------------------------

    screen.fill((30, 30, 40))

    # -------------------------
    # DRAW GRID
    # -------------------------

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):

            rect = pygame.Rect(
                GRID_OFFSET_X + col * CELL_SIZE,
                GRID_OFFSET_Y + row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            # Natural grass shade variations
            if (row + col) % 2 == 0:
                base_color = (48, 75, 65)
            else:
                base_color = (53, 82, 70)

            shade_offset = ((row * 13 + col * 7) % 5) - 2

            ground_color = (
                base_color[0] + shade_offset,
                base_color[1] + shade_offset * 2,
                base_color[2] + shade_offset
            )

            pygame.draw.rect(screen, ground_color, rect)

            # Subtle organic lawn micro-texture stippling
            tx1 = rect.x + 12 + ((row * 23 + col * 17) % 36)
            ty1 = rect.y + 10 + ((row * 19 + col * 29) % 40)
            pygame.draw.line(screen, (ground_color[0] + 5, ground_color[1] + 8, ground_color[2] + 6), (tx1, ty1), (tx1, ty1 + 1))

            tx2 = rect.x + 8 + ((row * 31 + col * 13) % 44)
            ty2 = rect.y + 14 + ((row * 11 + col * 37) % 34)
            pygame.draw.line(screen, (ground_color[0] - 4, ground_color[1] - 5, ground_color[2] - 4), (tx2, ty2), (tx2 + 1, ty2))

            # Softened grid border
            pygame.draw.rect(screen, (58, 80, 70), rect, 1)

            # Natural ground details on empty tiles (6 rich deterministic variants)
            if grid[row][col] == 0:

                variant = (row * 19 + col * 31) % 6

                if variant == 0:
                    # Dual-blade grass tuft with tip highlight
                    gx = rect.x + 15
                    gy = rect.y + 42
                    pygame.draw.line(screen, (90, 125, 95), (gx, gy), (gx - 3, gy - 6), 2)
                    pygame.draw.line(screen, (100, 140, 105), (gx, gy), (gx + 3, gy - 5), 2)
                    pygame.draw.line(screen, (120, 160, 125), (gx + 3, gy - 5), (gx + 3, gy - 6), 1)

                elif variant == 1:
                    # River pebble with sunlit highlight & base shadow
                    px = rect.x + 42
                    py = rect.y + 20
                    pygame.draw.circle(screen, (36, 52, 44), (px + 1, py + 1), 3)
                    pygame.draw.circle(screen, (48, 68, 58), (px, py), 2)
                    pygame.draw.line(screen, (70, 95, 80), (px - 1, py - 1), (px, py - 1), 1)

                elif variant == 2:
                    # 3-leaf clover cluster
                    cx = rect.x + 35
                    cy = rect.y + 35
                    pygame.draw.circle(screen, (110, 155, 115), (cx - 1, cy - 1), 2)
                    pygame.draw.circle(screen, (115, 160, 120), (cx + 1, cy - 1), 2)
                    pygame.draw.circle(screen, (105, 150, 110), (cx, cy + 1), 2)
                    pygame.draw.line(screen, (80, 120, 85), (cx, cy + 2), (cx + 1, cy + 4), 1)

                elif variant == 3:
                    # Wild meadow buttercup flower
                    fx = rect.x + 22
                    fy = rect.y + 26
                    pygame.draw.line(screen, (75, 115, 80), (fx, fy + 4), (fx, fy + 1), 1)
                    pygame.draw.circle(screen, (240, 220, 110), (fx, fy), 2)
                    pygame.draw.line(screen, (255, 245, 180), (fx, fy), (fx, fy), 1)

                elif variant == 4:
                    # Triple-blade wind-swept grass tuft
                    tx = rect.x + 38
                    ty = rect.y + 45
                    pygame.draw.line(screen, (85, 120, 90), (tx, ty), (tx - 4, ty - 5), 1)
                    pygame.draw.line(screen, (95, 135, 100), (tx, ty), (tx, ty - 7), 2)
                    pygame.draw.line(screen, (105, 145, 110), (tx, ty), (tx + 4, ty - 6), 1)

                elif variant == 5:
                    # Delicate mossy ground patch
                    mx = rect.x + 28
                    my = rect.y + 18
                    pygame.draw.circle(screen, (42, 65, 55), (mx, my), 2)
                    pygame.draw.circle(screen, (40, 62, 52), (mx + 3, my + 1), 1)

    # Outer city plot architectural frame
    city_outer = pygame.Rect(GRID_OFFSET_X, GRID_OFFSET_Y, GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
    pygame.draw.rect(screen, (20, 20, 28), city_outer.inflate(4, 4), 2)
    pygame.draw.line(screen, (75, 105, 90), (GRID_OFFSET_X - 1, GRID_OFFSET_Y - 1), (GRID_OFFSET_X + GRID_SIZE * CELL_SIZE, GRID_OFFSET_Y - 1), 1)
    pygame.draw.line(screen, (75, 105, 90), (GRID_OFFSET_X - 1, GRID_OFFSET_Y - 1), (GRID_OFFSET_X - 1, GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE), 1)

    # -------------------------
    # DRAW BUILDINGS
    # -------------------------

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):

            building = grid[row][col]

            if building != 0:

                # Only draw multi-tile buildings once from their root cell
                if building_origins.get((row, col), (row, col)) != (row, col):
                    continue

                x = GRID_OFFSET_X + col * CELL_SIZE
                y = GRID_OFFSET_Y + row * CELL_SIZE

                if building == 1:

                    # Geometrically projected semi-transparent ground shadow (top-left sunlight)
                    building_shadow_surf.fill((0, 0, 0, 0))
                    # Soft outer penumbra
                    pygame.draw.polygon(
                        building_shadow_surf,
                        (12, 20, 26, 65),
                        [(10, 48), (19, 55), (51, 55), (58, 44), (54, 40), (45, 48)]
                    )
                    # Dense core shadow
                    pygame.draw.polygon(
                        building_shadow_surf,
                        (10, 16, 22, 120),
                        [(12, 48), (20, 53), (49, 53), (56, 45), (53, 41), (45, 48)]
                    )
                    screen.blit(building_shadow_surf, (x, y))

                    # Front wall
                    pygame.draw.rect(
                        screen,
                        (0, 120, 210),
                        (x + 10, y + 18, 35, 30)
                    )

                    # Side wall
                    pygame.draw.polygon(
                        screen,
                        (0, 75, 150),
                        [
                            (x + 45, y + 18),
                            (x + 53, y + 10),
                            (x + 53, y + 40),
                            (x + 45, y + 48)
                        ]
                    )

                    # Roof
                    pygame.draw.polygon(
                        screen,
                        (50, 170, 255),
                        [
                            (x + 10, y + 18),
                            (x + 18, y + 10),
                            (x + 53, y + 10),
                            (x + 45, y + 18)
                        ]
                    )

                    # Roof-eave shading (overhang shadow on front and side walls)
                    pygame.draw.rect(
                        screen,
                        (0, 85, 155),
                        (x + 10, y + 18, 35, 2)
                    )
                    pygame.draw.line(
                        screen,
                        (0, 50, 105),
                        (x + 45, y + 19),
                        (x + 53, y + 11),
                        2
                    )

                    # Foundation contact shadows (ambient occlusion)
                    pygame.draw.line(
                        screen,
                        (0, 45, 90),
                        (x + 10, y + 48),
                        (x + 45, y + 48),
                        2
                    )
                    pygame.draw.line(
                        screen,
                        (0, 35, 75),
                        (x + 45, y + 48),
                        (x + 53, y + 40),
                        2
                    )

                    # Windows with top-left recess shadows
                    pygame.draw.rect(
                        screen, (180, 230, 255),
                        (x + 16, y + 25, 7, 7)
                    )
                    pygame.draw.line(
                        screen, (0, 70, 130),
                        (x + 16, y + 25), (x + 22, y + 25), 1
                    )
                    pygame.draw.line(
                        screen, (0, 70, 130),
                        (x + 16, y + 25), (x + 16, y + 31), 1
                    )

                    pygame.draw.rect(
                        screen, (180, 230, 255),
                        (x + 30, y + 25, 7, 7)
                    )
                    pygame.draw.line(
                        screen, (0, 70, 130),
                        (x + 30, y + 25), (x + 36, y + 25), 1
                    )
                    pygame.draw.line(
                        screen, (0, 70, 130),
                        (x + 30, y + 25), (x + 30, y + 31), 1
                    )

                elif building == 2:

                    # Geometrically projected semi-transparent ground shadow (top-left sunlight)
                    building_shadow_surf.fill((0, 0, 0, 0))
                    # Soft outer penumbra
                    pygame.draw.polygon(
                        building_shadow_surf,
                        (12, 20, 26, 65),
                        [(10, 48), (19, 55), (51, 55), (58, 44), (54, 40), (45, 48)]
                    )
                    # Dense core shadow
                    pygame.draw.polygon(
                        building_shadow_surf,
                        (10, 16, 22, 120),
                        [(12, 48), (20, 53), (49, 53), (56, 45), (53, 41), (45, 48)]
                    )
                    screen.blit(building_shadow_surf, (x, y))

                    # Front wall
                    pygame.draw.rect(
                        screen,
                        (0, 160, 90),
                        (x + 10, y + 20, 35, 28)
                    )

                    # Side wall
                    pygame.draw.polygon(
                        screen,
                        (0, 100, 60),
                        [
                            (x + 45, y + 20),
                            (x + 53, y + 12),
                            (x + 53, y + 40),
                            (x + 45, y + 48)
                        ]
                    )

                    # Roof
                    pygame.draw.polygon(
                        screen,
                        (0, 220, 130),
                        [
                            (x + 10, y + 20),
                            (x + 18, y + 12),
                            (x + 53, y + 12),
                            (x + 45, y + 20)
                        ]
                    )

                    # Roof-eave shading (overhang shadow on front and side walls)
                    pygame.draw.rect(
                        screen,
                        (0, 110, 60),
                        (x + 10, y + 20, 35, 2)
                    )
                    pygame.draw.line(
                        screen,
                        (0, 70, 40),
                        (x + 45, y + 21),
                        (x + 53, y + 13),
                        2
                    )

                    # Foundation contact shadows (ambient occlusion)
                    pygame.draw.line(
                        screen,
                        (0, 65, 35),
                        (x + 10, y + 48),
                        (x + 45, y + 48),
                        2
                    )
                    pygame.draw.line(
                        screen,
                        (0, 50, 25),
                        (x + 45, y + 48),
                        (x + 53, y + 40),
                        2
                    )

                    # Advertising billboard
                    pygame.draw.rect(
                        screen,
                        (30, 70, 50),
                        (x + 17, y + 3, 25, 9)
                    )

                    pygame.draw.rect(
                        screen,
                        (255, 220, 80),
                        (x + 21, y + 6, 17, 2)
                    )

                    # Billboard support
                    pygame.draw.line(
                        screen,
                        (180, 180, 180),
                        (x + 29, y + 12),
                        (x + 29, y + 19),
                        2
                    )

                    # Billboard shadow on roof
                    pygame.draw.rect(
                        screen,
                        (0, 175, 105),
                        (x + 20, y + 12, 22, 2)
                    )

                    # Satellite dish
                    pygame.draw.circle(
                        screen,
                        (220, 230, 220),
                        (x + 49, y + 7),
                        5
                    )

                    pygame.draw.line(
                        screen,
                        (180, 180, 180),
                        (x + 49, y + 7),
                        (x + 53, y + 2),
                        2
                    )

                    # Windows with top-left recess shadows
                    pygame.draw.rect(
                        screen, (180, 255, 220),
                        (x + 16, y + 27, 7, 7)
                    )
                    pygame.draw.line(
                        screen, (0, 90, 50),
                        (x + 16, y + 27), (x + 22, y + 27), 1
                    )
                    pygame.draw.line(
                        screen, (0, 90, 50),
                        (x + 16, y + 27), (x + 16, y + 33), 1
                    )

                    pygame.draw.rect(
                        screen, (180, 255, 220),
                        (x + 30, y + 27, 7, 7)
                    )
                    pygame.draw.line(
                        screen, (0, 90, 50),
                        (x + 30, y + 27), (x + 36, y + 27), 1
                    )
                    pygame.draw.line(
                        screen, (0, 90, 50),
                        (x + 30, y + 27), (x + 30, y + 33), 1
                    )

                elif building == 3:

                    # Geometrically projected semi-transparent ground shadow (top-left sunlight)
                    building_shadow_surf.fill((0, 0, 0, 0))
                    # Soft outer penumbra
                    pygame.draw.polygon(
                        building_shadow_surf,
                        (12, 20, 26, 65),
                        [(10, 48), (19, 55), (51, 55), (58, 44), (54, 40), (45, 48)]
                    )
                    # Dense core shadow
                    pygame.draw.polygon(
                        building_shadow_surf,
                        (10, 16, 22, 120),
                        [(12, 48), (20, 53), (49, 53), (56, 45), (53, 41), (45, 48)]
                    )
                    screen.blit(building_shadow_surf, (x, y))

                    # Front wall
                    pygame.draw.rect(
                        screen,
                        (130, 50, 190),
                        (x + 10, y + 20, 35, 28)
                    )

                    # Side wall
                    pygame.draw.polygon(
                        screen,
                        (75, 25, 120),
                        [
                            (x + 45, y + 20),
                            (x + 53, y + 12),
                            (x + 53, y + 40),
                            (x + 45, y + 48)
                        ]
                    )

                    # Roof
                    pygame.draw.polygon(
                        screen,
                        (190, 100, 255),
                        [
                            (x + 10, y + 20),
                            (x + 18, y + 12),
                            (x + 53, y + 12),
                            (x + 45, y + 20)
                        ]
                    )

                    # Roof-eave shading (overhang shadow on front and side walls)
                    pygame.draw.rect(
                        screen,
                        (90, 30, 135),
                        (x + 10, y + 20, 35, 2)
                    )
                    pygame.draw.line(
                        screen,
                        (50, 15, 80),
                        (x + 45, y + 21),
                        (x + 53, y + 13),
                        2
                    )

                    # Foundation contact shadows (ambient occlusion)
                    pygame.draw.line(
                        screen,
                        (45, 15, 70),
                        (x + 10, y + 48),
                        (x + 45, y + 48),
                        2
                    )
                    pygame.draw.line(
                        screen,
                        (35, 10, 55),
                        (x + 45, y + 48),
                        (x + 53, y + 40),
                        2
                    )

                    # Solar panel
                    pygame.draw.rect(
                        screen,
                        (30, 50, 100),
                        (x + 17, y + 14, 19, 6)
                    )

                    pygame.draw.line(
                        screen,
                        (100, 200, 255),
                        (x + 23, y + 14),
                        (x + 23, y + 20),
                        1
                    )

                    pygame.draw.line(
                        screen,
                        (100, 200, 255),
                        (x + 30, y + 14),
                        (x + 30, y + 20),
                        1
                    )

                    # Solar panel shadow on roof
                    pygame.draw.rect(
                        screen,
                        (150, 75, 210),
                        (x + 19, y + 20, 17, 1)
                    )

                    # Communication antenna
                    pygame.draw.line(
                        screen,
                        (220, 220, 240),
                        (x + 46, y + 12),
                        (x + 49, y + 2),
                        2
                    )

                    pygame.draw.circle(
                        screen,
                        (100, 220, 255),
                        (x + 49, y + 2),
                        3
                    )

                    # Laboratory windows with top-left recess shadows
                    pygame.draw.rect(
                        screen,
                        (130, 240, 255),
                        (x + 16, y + 27, 8, 9)
                    )
                    pygame.draw.line(
                        screen, (70, 25, 110),
                        (x + 16, y + 27), (x + 23, y + 27), 1
                    )
                    pygame.draw.line(
                        screen, (70, 25, 110),
                        (x + 16, y + 27), (x + 16, y + 35), 1
                    )

                    pygame.draw.rect(
                        screen,
                        (130, 240, 255),
                        (x + 30, y + 27, 8, 9)
                    )
                    pygame.draw.line(
                        screen, (70, 25, 110),
                        (x + 30, y + 27), (x + 37, y + 27), 1
                    )
                    pygame.draw.line(
                        screen, (70, 25, 110),
                        (x + 30, y + 27), (x + 30, y + 35), 1
                    )

                elif building == 4:

                    # Check adjacent road connections
                    road_up = (row > 0 and grid[row - 1][col] == 4)
                    road_down = (row < GRID_SIZE - 1 and grid[row + 1][col] == 4)
                    road_left = (col > 0 and grid[row][col - 1] == 4)
                    road_right = (col < GRID_SIZE - 1 and grid[row][col + 1] == 4)

                    # Pavement / curb base
                    pygame.draw.rect(
                        screen,
                        (115, 122, 125),
                        (x, y, CELL_SIZE, CELL_SIZE)
                    )

                    # 2.5D Curb base bevels (sunlit top/left, shaded bottom/right)
                    pygame.draw.line(screen, (140, 148, 150), (x, y), (x + CELL_SIZE - 1, y), 1)
                    pygame.draw.line(screen, (140, 148, 150), (x, y), (x, y + CELL_SIZE - 1), 1)
                    pygame.draw.line(screen, (85, 90, 92), (x, y + CELL_SIZE - 1), (x + CELL_SIZE - 1, y + CELL_SIZE - 1), 1)
                    pygame.draw.line(screen, (85, 90, 92), (x + CELL_SIZE - 1, y), (x + CELL_SIZE - 1, y + CELL_SIZE - 1), 1)

                    # Dark asphalt surface - central hub
                    pygame.draw.rect(
                        screen,
                        (42, 45, 50),
                        (x + 10, y + 10, 40, 40)
                    )

                    # Extend asphalt to connected neighbors
                    if road_up:
                        pygame.draw.rect(screen, (42, 45, 50), (x + 10, y, 40, 10))
                    if road_down:
                        pygame.draw.rect(screen, (42, 45, 50), (x + 10, y + 50, 40, 10))
                    if road_left:
                        pygame.draw.rect(screen, (42, 45, 50), (x, y + 10, 10, 40))
                    if road_right:
                        pygame.draw.rect(screen, (42, 45, 50), (x + 50, y + 10, 10, 40))

                    # Asphalt recessed inner drop-shadow (top & left)
                    if not road_up:
                        pygame.draw.line(screen, (28, 30, 34), (x + 10, y + 10), (x + 50, y + 10), 1)
                    if not road_left:
                        pygame.draw.line(screen, (28, 30, 34), (x + 10, y + 10), (x + 10, y + 50), 1)

                    # Curb lines (boundary between asphalt and sidewalk)
                    curb_color = (85, 92, 98)

                    # Top curb
                    if not road_up:
                        pygame.draw.line(screen, curb_color, (x + 10, y + 10), (x + 50, y + 10), 2)
                    else:
                        pygame.draw.line(screen, curb_color, (x + 10, y), (x + 10, y + 10), 2)
                        pygame.draw.line(screen, curb_color, (x + 50, y), (x + 50, y + 10), 2)

                    # Bottom curb
                    if not road_down:
                        pygame.draw.line(screen, curb_color, (x + 10, y + 50), (x + 50, y + 50), 2)
                    else:
                        pygame.draw.line(screen, curb_color, (x + 10, y + 50), (x + 10, y + 60), 2)
                        pygame.draw.line(screen, curb_color, (x + 50, y + 50), (x + 50, y + 60), 2)

                    # Left curb
                    if not road_left:
                        pygame.draw.line(screen, curb_color, (x + 10, y + 10), (x + 10, y + 50), 2)
                    else:
                        pygame.draw.line(screen, curb_color, (x, y + 10), (x + 10, y + 10), 2)
                        pygame.draw.line(screen, curb_color, (x, y + 50), (x + 10, y + 50), 2)

                    # Right curb
                    if not road_right:
                        pygame.draw.line(screen, curb_color, (x + 50, y + 10), (x + 50, y + 50), 2)
                    else:
                        pygame.draw.line(screen, curb_color, (x + 50, y + 10), (x + 60, y + 10), 2)
                        pygame.draw.line(screen, curb_color, (x + 50, y + 50), (x + 60, y + 50), 2)

                    # Road markings (center dashes)
                    road_white = (230, 235, 235)

                    if road_up:
                        pygame.draw.rect(screen, road_white, (x + 28, y + 4, 4, 12))
                    if road_down:
                        pygame.draw.rect(screen, road_white, (x + 28, y + 44, 4, 12))
                    if road_left:
                        pygame.draw.rect(screen, road_white, (x + 4, y + 28, 12, 4))
                    if road_right:
                        pygame.draw.rect(screen, road_white, (x + 44, y + 28, 12, 4))

                    # Center dashes on straight sections, dead-ends, or isolated tiles
                    if not (road_up or road_down or road_left or road_right):
                        pygame.draw.rect(screen, road_white, (x + 28, y + 24, 4, 12))
                    elif (road_up and road_down and not (road_left or road_right)) or (road_up != road_down and not (road_left or road_right)):
                        pygame.draw.rect(screen, road_white, (x + 28, y + 24, 4, 12))
                    elif (road_left and road_right and not (road_up or road_down)) or (road_left != road_right and not (road_up or road_down)):
                        pygame.draw.rect(screen, road_white, (x + 24, y + 28, 12, 4))

                elif building == 5:

                    # Pedestrian pathway - stone / concrete flagstone paving
                    # Neighboring connections for seamless promenade paving
                    path_up = (row > 0 and grid[row - 1][col] in (4, 5))
                    path_down = (row < GRID_SIZE - 1 and grid[row + 1][col] in (4, 5))
                    path_left = (col > 0 and grid[row][col - 1] in (4, 5))
                    path_right = (col < GRID_SIZE - 1 and grid[row][col + 1] in (4, 5))

                    # Semi-transparent drop-shadow on ground (only on outer non-connected edges)
                    building_shadow_surf.fill((0, 0, 0, 0))
                    if not (path_down and path_right):
                        pygame.draw.rect(building_shadow_surf, (12, 20, 26, 60), (5, 5, 53, 53), border_radius=4)
                        pygame.draw.rect(building_shadow_surf, (10, 16, 22, 110), (6, 6, 52, 52), border_radius=4)
                    screen.blit(building_shadow_surf, (x, y))

                    # Stone mortar base
                    pygame.draw.rect(
                        screen,
                        (155, 160, 155),
                        (x + 3, y + 3, 54, 54),
                        border_radius=3
                    )

                    # Seamless seam extensions to connected pathways & roads
                    if path_up:
                        pygame.draw.rect(screen, (155, 160, 155), (x + 3, y, 54, 4))
                    if path_down:
                        pygame.draw.rect(screen, (155, 160, 155), (x + 3, y + 56, 54, 4))
                    if path_left:
                        pygame.draw.rect(screen, (155, 160, 155), (x, y + 3, 4, 54))
                    if path_right:
                        pygame.draw.rect(screen, (155, 160, 155), (x + 56, y + 3, 4, 54))

                    # Mortar perimeter bevels (only on non-connected outer borders)
                    if not path_up:
                        pygame.draw.line(screen, (190, 195, 190), (x + 4, y + 3), (x + 55, y + 3), 1)
                    if not path_left:
                        pygame.draw.line(screen, (190, 195, 190), (x + 3, y + 4), (x + 3, y + 55), 1)
                    if not path_down:
                        pygame.draw.line(screen, (125, 130, 125), (x + 4, y + 56), (x + 55, y + 56), 1)
                    if not path_right:
                        pygame.draw.line(screen, (125, 130, 125), (x + 56, y + 4), (x + 56, y + 55), 1)

                    # 2x2 beveled paving slabs
                    for pr in range(2):
                        for pc in range(2):
                            sx = x + 6 + pc * 25
                            sy = y + 6 + pr * 25

                            # Flagstone slab surface
                            pygame.draw.rect(
                                screen,
                                (198, 202, 196),
                                (sx, sy, 23, 23)
                            )

                            # Top & Left bevel highlight
                            pygame.draw.line(
                                screen,
                                (225, 228, 222),
                                (sx, sy),
                                (sx + 22, sy),
                                1
                            )
                            pygame.draw.line(
                                screen,
                                (225, 228, 222),
                                (sx, sy),
                                (sx, sy + 22),
                                1
                            )

                            # Bottom & Right bevel shadow
                            pygame.draw.line(
                                screen,
                                (168, 172, 166),
                                (sx, sy + 22),
                                (sx + 22, sy + 22),
                                1
                            )
                            pygame.draw.line(
                                screen,
                                (168, 172, 166),
                                (sx + 22, sy),
                                (sx + 22, sy + 22),
                                1
                            )

                elif building == 6:

                    # Trees & Landscaping - deterministic 3 variations
                    tree_variant = (row * 7 + col * 13) % 3

                    if tree_variant == 0:

                        # Broadleaf Oak / Shade Tree
                        # Geometrically projected semi-transparent ground shadow
                        building_shadow_surf.fill((0, 0, 0, 0))
                        pygame.draw.ellipse(building_shadow_surf, (12, 20, 26, 60), (14, 40, 36, 16))
                        pygame.draw.ellipse(building_shadow_surf, (10, 16, 22, 115), (18, 42, 28, 12))
                        screen.blit(building_shadow_surf, (x, y))

                        # Trunk & roots
                        pygame.draw.polygon(screen, (90, 60, 35), [(x + 24, y + 47), (x + 36, y + 47), (x + 30, y + 41)])
                        pygame.draw.rect(screen, (105, 70, 42), (x + 27, y + 29, 7, 17), border_radius=2)
                        pygame.draw.line(screen, (75, 48, 28), (x + 32, y + 30), (x + 32, y + 45), 2)

                        # Trunk contact shadow & foliage overhang shadow
                        pygame.draw.line(screen, (30, 18, 10), (x + 24, y + 47), (x + 36, y + 47), 1)
                        pygame.draw.rect(screen, (65, 40, 22), (x + 27, y + 29, 7, 3))

                        # Foliage - base shadow circles
                        pygame.draw.circle(screen, (34, 85, 44), (x + 30, y + 24), 18)
                        pygame.draw.circle(screen, (34, 85, 44), (x + 21, y + 27), 13)
                        pygame.draw.circle(screen, (34, 85, 44), (x + 39, y + 27), 13)

                        # Foliage - mid leafy green
                        pygame.draw.circle(screen, (48, 125, 60), (x + 29, y + 22), 16)
                        pygame.draw.circle(screen, (48, 125, 60), (x + 20, y + 25), 11)
                        pygame.draw.circle(screen, (48, 125, 60), (x + 38, y + 25), 11)

                        # Foliage - sunlit highlights (top-left)
                        pygame.draw.circle(screen, (75, 165, 80), (x + 26, y + 18), 11)
                        pygame.draw.circle(screen, (75, 165, 80), (x + 17, y + 22), 7)
                        pygame.draw.circle(screen, (100, 195, 102), (x + 24, y + 16), 5)

                    elif tree_variant == 1:

                        # Conifer / Pine Evergreen (Tiered conical boughs)
                        # Geometrically projected semi-transparent ground shadow
                        building_shadow_surf.fill((0, 0, 0, 0))
                        pygame.draw.ellipse(building_shadow_surf, (12, 20, 26, 55), (15, 44, 34, 13))
                        pygame.draw.ellipse(building_shadow_surf, (10, 16, 22, 110), (20, 45, 24, 10))
                        screen.blit(building_shadow_surf, (x, y))

                        # Trunk
                        pygame.draw.rect(screen, (85, 55, 35), (x + 27, y + 36, 6, 14), border_radius=1)
                        # Trunk contact shadow & bough overhang shadow
                        pygame.draw.line(screen, (30, 18, 10), (x + 27, y + 50), (x + 33, y + 50), 1)
                        pygame.draw.rect(screen, (55, 35, 22), (x + 27, y + 36, 6, 3))

                        # Tier 1 (bottom bough)
                        pygame.draw.polygon(screen, (25, 75, 48), [(x + 12, y + 41), (x + 48, y + 41), (x + 30, y + 26)])
                        pygame.draw.line(screen, (50, 125, 75), (x + 13, y + 41), (x + 30, y + 27), 2)

                        # Tier 2 (middle bough)
                        pygame.draw.polygon(screen, (30, 95, 58), [(x + 16, y + 31), (x + 44, y + 31), (x + 30, y + 18)])
                        pygame.draw.line(screen, (60, 145, 88), (x + 17, y + 31), (x + 30, y + 19), 2)

                        # Tier 3 (top bough / apex)
                        pygame.draw.polygon(screen, (38, 115, 70), [(x + 20, y + 22), (x + 40, y + 22), (x + 30, y + 10)])
                        pygame.draw.line(screen, (75, 170, 105), (x + 21, y + 22), (x + 30, y + 11), 2)
                        pygame.draw.circle(screen, (95, 195, 125), (x + 30, y + 11), 2)

                    elif tree_variant == 2:

                        # Companion Flowering Copse (Dual trees with blossom dots)
                        # Geometrically projected semi-transparent ground shadows
                        building_shadow_surf.fill((0, 0, 0, 0))
                        pygame.draw.ellipse(building_shadow_surf, (12, 20, 26, 60), (12, 40, 25, 12))
                        pygame.draw.ellipse(building_shadow_surf, (10, 16, 22, 115), (15, 42, 19, 9))
                        pygame.draw.ellipse(building_shadow_surf, (12, 20, 26, 60), (33, 44, 21, 10))
                        pygame.draw.ellipse(building_shadow_surf, (10, 16, 22, 115), (35, 45, 16, 8))
                        screen.blit(building_shadow_surf, (x, y))

                        # Trunks
                        pygame.draw.rect(screen, (100, 68, 40), (x + 21, y + 29, 5, 15), border_radius=1)
                        pygame.draw.rect(screen, (110, 75, 45), (x + 40, y + 33, 4, 13), border_radius=1)
                        # Trunk contact & canopy overhang shadows
                        pygame.draw.line(screen, (30, 18, 10), (x + 21, y + 44), (x + 26, y + 44), 1)
                        pygame.draw.line(screen, (30, 18, 10), (x + 40, y + 46), (x + 44, y + 46), 1)
                        pygame.draw.rect(screen, (60, 38, 20), (x + 21, y + 29, 5, 2))
                        pygame.draw.rect(screen, (65, 42, 25), (x + 40, y + 33, 4, 2))

                        # Tree 1 (Left, larger)
                        pygame.draw.circle(screen, (40, 95, 45), (x + 23, y + 22), 14)
                        pygame.draw.circle(screen, (60, 135, 62), (x + 22, y + 20), 12)
                        pygame.draw.circle(screen, (90, 175, 82), (x + 20, y + 17), 8)
                        # Blossom highlights
                        pygame.draw.circle(screen, (245, 170, 185), (x + 17, y + 18), 2)
                        pygame.draw.circle(screen, (245, 170, 185), (x + 25, y + 15), 2)
                        pygame.draw.circle(screen, (255, 210, 220), (x + 22, y + 24), 2)

                        # Tree 2 (Right, smaller)
                        pygame.draw.circle(screen, (35, 90, 50), (x + 42, y + 26), 11)
                        pygame.draw.circle(screen, (55, 130, 68), (x + 41, y + 25), 9)
                        pygame.draw.circle(screen, (85, 170, 90), (x + 39, y + 22), 6)
                        # Blossom / fruit highlights
                        pygame.draw.circle(screen, (250, 195, 120), (x + 38, y + 26), 2)
                        pygame.draw.circle(screen, (250, 195, 120), (x + 44, y + 22), 2)

                elif building == 7:

                    # Streetlight - 2.5D cast-iron lamp post with glowing lantern & light pool
                    # Semi-transparent ground shadow & warm illumination pool
                    building_shadow_surf.fill((0, 0, 0, 0))
                    # Warm ambient light pool on ground
                    pygame.draw.ellipse(building_shadow_surf, (255, 235, 140, 40), (10, 34, 40, 20))
                    # Diagonal slender post shadow (consistent top-left sunlight)
                    pygame.draw.line(building_shadow_surf, (10, 16, 22, 105), (29, 46), (46, 53), 2)
                    pygame.draw.circle(building_shadow_surf, (10, 16, 22, 105), (47, 53), 3)
                    # Plinth base shadow
                    pygame.draw.ellipse(building_shadow_surf, (12, 20, 26, 80), (24, 46, 16, 6))
                    screen.blit(building_shadow_surf, (x, y))

                    # Concrete plinth mounting base
                    pygame.draw.rect(screen, (150, 155, 155), (x + 23, y + 43, 14, 7), border_radius=1)
                    pygame.draw.line(screen, (185, 190, 190), (x + 23, y + 43), (x + 36, y + 43), 1)
                    pygame.draw.line(screen, (110, 115, 115), (x + 23, y + 49), (x + 36, y + 49), 1)
                    # Plinth contact shadow
                    pygame.draw.line(screen, (35, 40, 40), (x + 23, y + 50), (x + 36, y + 50), 1)

                    # Cast-iron lamp post
                    pygame.draw.rect(screen, (50, 55, 60), (x + 28, y + 16, 4, 28))
                    pygame.draw.line(screen, (85, 95, 105), (x + 28, y + 17), (x + 28, y + 43), 1)
                    pygame.draw.line(screen, (30, 35, 40), (x + 31, y + 17), (x + 31, y + 43), 1)

                    # Decorative collar rings on post
                    pygame.draw.rect(screen, (70, 78, 85), (x + 27, y + 38, 6, 2))
                    pygame.draw.rect(screen, (70, 78, 85), (x + 27, y + 25, 6, 2))

                    # Top arched bracket and finial spire
                    pygame.draw.rect(screen, (50, 55, 60), (x + 22, y + 14, 16, 3))
                    pygame.draw.polygon(screen, (40, 45, 50), [(x + 26, y + 14), (x + 34, y + 14), (x + 30, y + 8)])
                    pygame.draw.line(screen, (70, 78, 85), (x + 30, y + 6), (x + 30, y + 8), 2)

                    # Lantern housing & luminous warm core
                    pygame.draw.polygon(screen, (45, 50, 55), [(x + 24, y + 14), (x + 36, y + 14), (x + 30, y + 11)])
                    pygame.draw.rect(screen, (255, 225, 110), (x + 26, y + 14, 8, 8))
                    pygame.draw.rect(screen, (255, 255, 210), (x + 28, y + 16, 4, 4))
                    pygame.draw.rect(screen, (45, 50, 55), (x + 26, y + 22, 8, 2))

                elif building == 8:

                    # Park Bench - 2.5D wooden slatted park bench with cast-iron frame & shadow
                    # Semi-transparent ground shadow underneath
                    building_shadow_surf.fill((0, 0, 0, 0))
                    pygame.draw.ellipse(building_shadow_surf, (12, 20, 26, 60), (11, 38, 40, 13))
                    pygame.draw.ellipse(building_shadow_surf, (10, 16, 22, 115), (15, 40, 32, 9))
                    # Contact dots under 4 leg feet
                    for fx, fy in [(14, 43), (19, 43), (44, 43), (48, 43)]:
                        pygame.draw.circle(building_shadow_surf, (8, 12, 16, 150), (fx, fy), 2)
                    screen.blit(building_shadow_surf, (x, y))

                    # Concrete mounting pads for legs
                    pygame.draw.rect(screen, (140, 145, 142), (x + 12, y + 42, 6, 3))
                    pygame.draw.rect(screen, (140, 145, 142), (x + 42, y + 42, 6, 3))

                    # Cast-iron frame: legs and armrests
                    pygame.draw.line(screen, (35, 45, 40), (x + 15, y + 24), (x + 14, y + 43), 3)
                    pygame.draw.line(screen, (35, 45, 40), (x + 15, y + 34), (x + 20, y + 43), 2)
                    pygame.draw.line(screen, (35, 45, 40), (x + 45, y + 24), (x + 44, y + 43), 3)
                    pygame.draw.line(screen, (35, 45, 40), (x + 45, y + 34), (x + 48, y + 43), 2)

                    pygame.draw.line(screen, (55, 70, 62), (x + 13, y + 28), (x + 19, y + 28), 2)
                    pygame.draw.line(screen, (55, 70, 62), (x + 43, y + 28), (x + 49, y + 28), 2)

                    # Backrest wooden slats with top highlights
                    pygame.draw.rect(screen, (175, 110, 55), (x + 14, y + 20, 32, 4), border_radius=1)
                    pygame.draw.line(screen, (215, 150, 90), (x + 14, y + 20), (x + 45, y + 20), 1)

                    # Slat drop shadow on lower slat
                    pygame.draw.line(screen, (125, 75, 32), (x + 14, y + 25), (x + 45, y + 25), 1)
                    pygame.draw.rect(screen, (160, 100, 48), (x + 14, y + 25, 32, 4), border_radius=1)
                    pygame.draw.line(screen, (200, 135, 80), (x + 14, y + 25), (x + 45, y + 25), 1)

                    # Seat wooden slats in 2.5D perspective
                    pygame.draw.rect(screen, (185, 120, 65), (x + 13, y + 31, 34, 4), border_radius=1)
                    pygame.draw.line(screen, (225, 160, 100), (x + 13, y + 31), (x + 46, y + 31), 1)

                    pygame.draw.rect(screen, (170, 105, 52), (x + 13, y + 36, 34, 4), border_radius=1)
                    pygame.draw.line(screen, (210, 145, 88), (x + 13, y + 36), (x + 46, y + 36), 1)
                    pygame.draw.line(screen, (115, 68, 30), (x + 13, y + 39), (x + 46, y + 39), 1)

                elif building == 9:

                    # Flower Bed - raised curb border, rich soil, dense foliage, and multi-color blossoms
                    # Semi-transparent outer ground drop-shadow
                    building_shadow_surf.fill((0, 0, 0, 0))
                    pygame.draw.rect(building_shadow_surf, (12, 20, 26, 60), (8, 8, 48, 48), border_radius=5)
                    pygame.draw.rect(building_shadow_surf, (10, 16, 22, 115), (9, 9, 47, 47), border_radius=4)
                    screen.blit(building_shadow_surf, (x, y))

                    # Raised terracotta / stone retaining border
                    pygame.draw.rect(screen, (145, 90, 65), (x + 6, y + 6, 48, 48), border_radius=4)
                    pygame.draw.line(screen, (180, 120, 95), (x + 7, y + 6), (x + 52, y + 6), 2)
                    pygame.draw.line(screen, (180, 120, 95), (x + 6, y + 7), (x + 6, y + 52), 2)
                    pygame.draw.line(screen, (105, 60, 42), (x + 7, y + 53), (x + 53, y + 53), 2)
                    pygame.draw.line(screen, (105, 60, 42), (x + 53, y + 7), (x + 53, y + 53), 2)

                    # Rich dark soil bed with top/left inner wall recessed shadow
                    pygame.draw.rect(screen, (55, 38, 25), (x + 10, y + 10, 40, 40), border_radius=2)
                    pygame.draw.rect(screen, (32, 22, 14), (x + 10, y + 10, 40, 3))
                    pygame.draw.rect(screen, (32, 22, 14), (x + 10, y + 10, 3, 40))
                    pygame.draw.rect(screen, (42, 28, 18), (x + 14, y + 16, 3, 2))
                    pygame.draw.rect(screen, (42, 28, 18), (x + 36, y + 22, 2, 3))
                    pygame.draw.rect(screen, (42, 28, 18), (x + 24, y + 38, 3, 2))

                    # Dense leafy foliage clusters
                    pygame.draw.circle(screen, (35, 95, 45), (x + 20, y + 20), 8)
                    pygame.draw.circle(screen, (42, 110, 52), (x + 38, y + 20), 8)
                    pygame.draw.circle(screen, (38, 102, 48), (x + 20, y + 38), 8)
                    pygame.draw.circle(screen, (45, 118, 56), (x + 38, y + 38), 8)
                    pygame.draw.circle(screen, (48, 125, 60), (x + 29, y + 29), 10)

                    # Foliage highlights
                    pygame.draw.circle(screen, (68, 155, 75), (x + 28, y + 27), 6)
                    pygame.draw.circle(screen, (62, 145, 70), (x + 18, y + 18), 5)
                    pygame.draw.circle(screen, (62, 145, 70), (x + 37, y + 18), 5)

                    # Blossoms - Red Tulips (top-left)
                    pygame.draw.circle(screen, (225, 55, 70), (x + 18, y + 18), 4)
                    pygame.draw.circle(screen, (255, 95, 110), (x + 17, y + 17), 2)
                    pygame.draw.circle(screen, (255, 230, 110), (x + 18, y + 18), 1)

                    # Blossoms - Golden Marigolds (top-right)
                    pygame.draw.circle(screen, (255, 185, 40), (x + 38, y + 18), 4)
                    pygame.draw.circle(screen, (255, 220, 90), (x + 37, y + 17), 2)
                    pygame.draw.circle(screen, (200, 100, 20), (x + 38, y + 18), 1)

                    # Blossoms - Lavender / Petunias (bottom-left)
                    pygame.draw.circle(screen, (175, 105, 225), (x + 18, y + 38), 4)
                    pygame.draw.circle(screen, (210, 150, 255), (x + 17, y + 37), 2)
                    pygame.draw.circle(screen, (255, 240, 140), (x + 18, y + 38), 1)

                    # Blossoms - Coral Carnations (bottom-right)
                    pygame.draw.circle(screen, (245, 110, 150), (x + 38, y + 38), 4)
                    pygame.draw.circle(screen, (255, 160, 190), (x + 37, y + 37), 2)
                    pygame.draw.circle(screen, (255, 235, 130), (x + 38, y + 38), 1)

                    # Blossoms - White Lily Centerpiece
                    pygame.draw.circle(screen, (245, 245, 250), (x + 29, y + 29), 4)
                    pygame.draw.circle(screen, (255, 255, 255), (x + 28, y + 28), 2)
                    pygame.draw.circle(screen, (255, 200, 50), (x + 29, y + 29), 1)

                elif building == 10:

                    # Tech Campus (2x2 Multi-Tile Flagship Building)
                    # Semi-transparent 2.5D Ground Shadow
                    campus_shadow_surf.fill((0, 0, 0, 0))
                    # Outer soft penumbra
                    pygame.draw.polygon(
                        campus_shadow_surf,
                        (12, 20, 26, 65),
                        [(12, 98), (28, 114), (105, 114), (118, 92), (112, 80), (96, 98)]
                    )
                    # Core dense contact shadow
                    pygame.draw.polygon(
                        campus_shadow_surf,
                        (10, 16, 22, 120),
                        [(14, 98), (29, 110), (102, 110), (116, 93), (110, 82), (96, 98)]
                    )
                    screen.blit(campus_shadow_surf, (x, y))

                    # Paved plaza base / foundation terrace
                    pygame.draw.rect(screen, (95, 105, 110), (x + 6, y + 30, 108, 80), border_radius=4)
                    pygame.draw.line(screen, (130, 140, 145), (x + 7, y + 30), (x + 113, y + 30), 1)
                    pygame.draw.line(screen, (130, 140, 145), (x + 6, y + 31), (x + 6, y + 109), 1)

                    # Main Building Architecture
                    # Front Wall
                    pygame.draw.rect(screen, (45, 95, 145), (x + 16, y + 42, 76, 58))
                    # Side Wall
                    pygame.draw.polygon(
                        screen,
                        (30, 65, 105),
                        [(x + 92, y + 42), (x + 108, y + 26), (x + 108, y + 84), (x + 92, y + 100)]
                    )
                    # Roof
                    pygame.draw.polygon(
                        screen,
                        (70, 140, 205),
                        [(x + 16, y + 42), (x + 32, y + 26), (x + 108, y + 26), (x + 92, y + 42)]
                    )

                    # Roof eave shadow
                    pygame.draw.rect(screen, (25, 55, 90), (x + 16, y + 42, 76, 2))
                    pygame.draw.line(screen, (20, 45, 75), (x + 92, y + 43), (x + 108, y + 27), 2)

                    # Foundation contact lines
                    pygame.draw.line(screen, (20, 35, 50), (x + 16, y + 100), (x + 92, y + 100), 2)
                    pygame.draw.line(screen, (15, 28, 40), (x + 92, y + 100), (x + 108, y + 84), 2)

                    # Rooftop Skylight
                    pygame.draw.polygon(
                        screen,
                        (140, 230, 255),
                        [(x + 44, y + 34), (x + 54, y + 24), (x + 88, y + 24), (x + 78, y + 34)]
                    )
                    pygame.draw.polygon(
                        screen,
                        (200, 245, 255),
                        [(x + 44, y + 34), (x + 54, y + 24), (x + 88, y + 24), (x + 78, y + 34)],
                        1
                    )
                    pygame.draw.line(screen, (200, 245, 255), (x + 61, y + 34), (x + 71, y + 24), 1)

                    # Modern Entrance Canopy & Glass Doors
                    pygame.draw.rect(screen, (30, 40, 50), (x + 46, y + 84, 20, 4))
                    pygame.draw.line(screen, (90, 110, 130), (x + 46, y + 84), (x + 65, y + 84), 1)
                    pygame.draw.rect(screen, (160, 220, 245), (x + 48, y + 88, 16, 12))
                    pygame.draw.line(screen, (40, 60, 80), (x + 56, y + 88), (x + 56, y + 100), 1)

                    # Architectural Ribbon Windows (Floor 2 and Floor 1)
                    pygame.draw.rect(screen, (170, 230, 255), (x + 22, y + 50, 64, 10))
                    pygame.draw.line(screen, (25, 60, 95), (x + 22, y + 50), (x + 85, y + 50), 1)
                    for mx in range(x + 34, x + 85, 12):
                        pygame.draw.line(screen, (45, 95, 145), (mx, y + 50), (mx, y + 59), 1)

                    pygame.draw.rect(screen, (170, 230, 255), (x + 22, y + 68, 64, 10))
                    pygame.draw.line(screen, (25, 60, 95), (x + 22, y + 68), (x + 85, y + 68), 1)
                    for mx in range(x + 34, x + 85, 12):
                        pygame.draw.line(screen, (45, 95, 145), (mx, y + 68), (mx, y + 77), 1)

                    # Side Perspective Windows
                    pygame.draw.polygon(
                        screen,
                        (130, 195, 230),
                        [(x + 96, y + 52), (x + 104, y + 44), (x + 104, y + 56), (x + 96, y + 64)]
                    )
                    pygame.draw.polygon(
                        screen,
                        (130, 195, 230),
                        [(x + 96, y + 70), (x + 104, y + 62), (x + 104, y + 74), (x + 96, y + 82)]
                    )

                    # Campus Courtyard Decorative Planters
                    pygame.draw.rect(screen, (60, 45, 30), (x + 20, y + 88, 16, 12), border_radius=2)
                    pygame.draw.circle(screen, (50, 130, 65), (x + 28, y + 92), 6)
                    pygame.draw.circle(screen, (80, 175, 95), (x + 26, y + 90), 3)

                    pygame.draw.rect(screen, (60, 45, 30), (x + 80, y + 88, 16, 12), border_radius=2)
                    pygame.draw.circle(screen, (50, 130, 65), (x + 88, y + 92), 6)
                    pygame.draw.circle(screen, (80, 175, 95), (x + 86, y + 90), 3)

                elif building == 11:

                    # Cloud Data Center (2x2 Multi-Tile High-Performance Computing Facility)
                    # Semi-transparent 2.5D Ground Shadow
                    datacenter_shadow_surf.fill((0, 0, 0, 0))
                    # Outer soft penumbra
                    pygame.draw.polygon(
                        datacenter_shadow_surf,
                        (10, 18, 24, 65),
                        [(10, 98), (26, 115), (108, 115), (119, 94), (114, 78), (96, 98)]
                    )
                    # Core contact shadow
                    pygame.draw.polygon(
                        datacenter_shadow_surf,
                        (8, 14, 20, 125),
                        [(12, 98), (28, 112), (105, 112), (117, 95), (111, 80), (96, 98)]
                    )
                    screen.blit(datacenter_shadow_surf, (x, y))

                    # Paved Industrial Foundation Slab
                    pygame.draw.rect(screen, (52, 58, 68), (x + 6, y + 28, 108, 84), border_radius=3)
                    pygame.draw.line(screen, (85, 95, 110), (x + 7, y + 28), (x + 113, y + 28), 1)
                    pygame.draw.line(screen, (85, 95, 110), (x + 6, y + 29), (x + 6, y + 111), 1)
                    pygame.draw.line(screen, (32, 36, 44), (x + 7, y + 112), (x + 114, y + 112), 1)
                    pygame.draw.line(screen, (32, 36, 44), (x + 114, y + 29), (x + 114, y + 112), 1)

                    # Yellow/Black hazard safety stripes near server loading bay
                    for hx in range(x + 14, x + 36, 6):
                        pygame.draw.line(screen, (220, 180, 40), (hx, y + 106), (hx + 3, y + 109), 2)
                        pygame.draw.line(screen, (30, 30, 30), (hx + 3, y + 106), (hx + 6, y + 109), 2)

                    # Main Data Center Building Massing
                    # Front Wall (Titanium Slate)
                    pygame.draw.rect(screen, (40, 48, 60), (x + 14, y + 42, 66, 60))
                    # Side Wall (Deep Perspective Shadow)
                    pygame.draw.polygon(
                        screen,
                        (26, 32, 42),
                        [(x + 80, y + 42), (x + 106, y + 22), (x + 106, y + 82), (x + 80, y + 102)]
                    )
                    # Roof (High-tech Composite)
                    pygame.draw.polygon(
                        screen,
                        (62, 74, 92),
                        [(x + 14, y + 42), (x + 40, y + 22), (x + 106, y + 22), (x + 80, y + 42)]
                    )

                    # Roof-eave overhang shadow
                    pygame.draw.rect(screen, (20, 25, 34), (x + 14, y + 42, 66, 2))
                    pygame.draw.line(screen, (16, 20, 28), (x + 80, y + 43), (x + 106, y + 23), 2)

                    # Foundation contact lines
                    pygame.draw.line(screen, (16, 20, 26), (x + 14, y + 102), (x + 80, y + 102), 2)
                    pygame.draw.line(screen, (12, 16, 22), (x + 80, y + 102), (x + 106, y + 82), 2)

                    # Server Hall Louvers & Glowing Server Racks
                    # Server Bay 1 (Left Bay - Cyan / Ice Blue Blade Array)
                    pygame.draw.rect(screen, (22, 28, 36), (x + 18, y + 48, 16, 34), border_radius=1)
                    pygame.draw.rect(screen, (12, 16, 22), (x + 19, y + 49, 14, 32))
                    for sy in range(y + 51, y + 80, 4):
                        pygame.draw.line(screen, (0, 210, 255), (x + 21, sy), (x + 25, sy), 1)
                        pygame.draw.circle(screen, (0, 245, 255), (x + 28, sy), 1)
                        pygame.draw.line(screen, (0, 160, 210), (x + 30, sy), (x + 31, sy), 1)

                    # Server Bay 2 (Right Bay - Emerald Matrix & Amber Activity Lights)
                    pygame.draw.rect(screen, (22, 28, 36), (x + 40, y + 48, 16, 34), border_radius=1)
                    pygame.draw.rect(screen, (12, 16, 22), (x + 41, y + 49, 14, 32))
                    for sy in range(y + 51, y + 80, 4):
                        led_color = (40, 235, 120) if (sy % 8 != 0) else (255, 195, 45)
                        pygame.draw.line(screen, led_color, (x + 43, sy), (x + 47, sy), 1)
                        pygame.draw.circle(screen, (100, 255, 160) if led_color[0] < 100 else (255, 230, 120), (x + 50, sy), 1)
                        pygame.draw.line(screen, (20, 160, 80), (x + 52, sy), (x + 53, sy), 1)

                    # High-velocity Ventilation Intake Louvers (Center top)
                    pygame.draw.rect(screen, (20, 26, 34), (x + 60, y + 48, 16, 22), border_radius=1)
                    for vy in range(y + 50, y + 68, 3):
                        pygame.draw.line(screen, (55, 68, 85), (x + 61, vy), (x + 74, vy), 1)
                        pygame.draw.line(screen, (10, 14, 18), (x + 61, vy + 1), (x + 74, vy + 1), 1)

                    # Security Airlock & Biometric Portal (Bottom center)
                    pygame.draw.rect(screen, (25, 32, 42), (x + 38, y + 86, 22, 16), border_radius=2)
                    pygame.draw.rect(screen, (15, 20, 26), (x + 40, y + 88, 18, 14))
                    pygame.draw.line(screen, (70, 90, 115), (x + 40, y + 88), (x + 57, y + 88), 1)
                    pygame.draw.circle(screen, (0, 255, 180), (x + 55, y + 94), 1)
                    pygame.draw.line(screen, (40, 50, 65), (x + 49, y + 88), (x + 49, y + 101), 1)

                    # Rooftop Infrastructure: Dual Industrial HVAC Chillers
                    # Chiller Unit 1
                    pygame.draw.rect(screen, (72, 84, 102), (x + 46, y + 26, 15, 12), border_radius=2)
                    pygame.draw.line(screen, (100, 115, 135), (x + 46, y + 26), (x + 60, y + 26), 1)
                    pygame.draw.circle(screen, (32, 40, 50), (x + 53, y + 32), 4)
                    pygame.draw.circle(screen, (60, 72, 88), (x + 53, y + 32), 4, 1)
                    pygame.draw.line(screen, (120, 140, 165), (x + 50, y + 32), (x + 56, y + 32), 1)
                    pygame.draw.line(screen, (120, 140, 165), (x + 53, y + 29), (x + 53, y + 35), 1)

                    # Chiller Unit 2
                    pygame.draw.rect(screen, (72, 84, 102), (x + 65, y + 26, 15, 12), border_radius=2)
                    pygame.draw.line(screen, (100, 115, 135), (x + 65, y + 26), (x + 79, y + 26), 1)
                    pygame.draw.circle(screen, (32, 40, 50), (x + 72, y + 32), 4)
                    pygame.draw.circle(screen, (60, 72, 88), (x + 72, y + 32), 4, 1)
                    pygame.draw.line(screen, (120, 140, 165), (x + 69, y + 32), (x + 75, y + 32), 1)
                    pygame.draw.line(screen, (120, 140, 165), (x + 72, y + 29), (x + 72, y + 35), 1)

                    # Coolant piping conduits (Cyan chilled fluid lines)
                    pygame.draw.line(screen, (40, 160, 200), (x + 53, y + 38), (x + 72, y + 38), 2)
                    pygame.draw.line(screen, (30, 120, 150), (x + 62, y + 38), (x + 62, y + 42), 2)

                    # Telecom Satellite Uplink Dish (Left roof)
                    pygame.draw.line(screen, (90, 105, 125), (x + 28, y + 34), (x + 28, y + 26), 2)
                    pygame.draw.ellipse(screen, (225, 235, 245), (x + 21, y + 19, 14, 10))
                    pygame.draw.ellipse(screen, (140, 155, 175), (x + 21, y + 19, 14, 10), 1)
                    pygame.draw.line(screen, (180, 195, 215), (x + 28, y + 24), (x + 32, y + 18), 1)
                    pygame.draw.circle(screen, (255, 80, 80), (x + 32, y + 18), 1)

                    # Aviation warning mast (Top-right corner)
                    pygame.draw.line(screen, (120, 130, 145), (x + 104, y + 22), (x + 104, y + 14), 1)
                    pygame.draw.circle(screen, (255, 40, 40), (x + 104, y + 14), 2)
                    pygame.draw.circle(screen, (255, 180, 180), (x + 104, y + 14), 1)

                    # High-Voltage Power Substation & Backup Generator (Right terrace)
                    pygame.draw.rect(screen, (48, 56, 68), (x + 84, y + 84, 20, 22), border_radius=2)
                    pygame.draw.line(screen, (80, 95, 115), (x + 84, y + 84), (x + 103, y + 84), 1)
                    pygame.draw.rect(screen, (225, 190, 40), (x + 88, y + 90, 12, 4))
                    pygame.draw.circle(screen, (20, 20, 20), (x + 94, y + 92), 1)
                    for ty in range(y + 96, y + 104, 2):
                        pygame.draw.line(screen, (25, 32, 40), (x + 86, ty), (x + 101, ty), 1)

                    # Side wall industrial conduits
                    pygame.draw.line(screen, (40, 50, 65), (x + 88, y + 48), (x + 102, y + 36), 2)
                    pygame.draw.line(screen, (30, 40, 52), (x + 88, y + 54), (x + 102, y + 42), 2)

                else:

                    # Fallback graphics for other buildings (dynamic footprint aware)
                    b_w, b_h = building_sizes.get(building, (1, 1))
                    rect = pygame.Rect(
                        x + 5,
                        y + 5,
                        b_w * CELL_SIZE - 10,
                        b_h * CELL_SIZE - 10
                    )

                    color = building_colors.get(building, (150, 150, 150))
                    pygame.draw.rect(screen, color, rect)

    # -------------------------
    # SELECTED TILE
    # -------------------------

    if selected_cell:

        sel_r, sel_c = selected_cell
        # If selecting a tile belonging to a multi-tile building, highlight its full footprint from root
        root_r, root_c = building_origins.get((sel_r, sel_c), (sel_r, sel_c))
        b_at_cell = grid[root_r][root_c] if (0 <= root_r < GRID_SIZE and 0 <= root_c < GRID_SIZE) else 0

        if b_at_cell != 0:
            b_w, b_h = building_sizes.get(b_at_cell, (1, 1))
            rect = pygame.Rect(
                GRID_OFFSET_X + root_c * CELL_SIZE,
                GRID_OFFSET_Y + root_r * CELL_SIZE,
                b_w * CELL_SIZE,
                b_h * CELL_SIZE
            )
        else:
            rect = pygame.Rect(
                GRID_OFFSET_X + sel_c * CELL_SIZE,
                GRID_OFFSET_Y + sel_r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

        pygame.draw.rect(
            screen,
            (0, 255, 0),
            rect,
            3
        )

    # =====================================================
    # HUD - MAIN PANEL
    # =====================================================

    hud_panel = pygame.Rect(
        680,
        25,
        290,
        290
    )

    pygame.draw.rect(
        screen,
        HUD_BG,
        hud_panel,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        HUD_BORDER,
        hud_panel,
        2,
        border_radius=12
    )

    # -------------------------
    # MONEY
    # -------------------------

    money_title = small_font.render(
        "MONEY",
        True,
        HUD_SECONDARY
    )

    money_value = font.render(
        f"Rs.{money}",
        True,
        HUD_TEXT
    )

    screen.blit(
        money_title,
        (700, 45)
    )

    screen.blit(
        money_value,
        (700, 70)
    )

    # -------------------------
    # STARTUP STATS
    # -------------------------

    employees_text = small_font.render(
        f"Employees: {employees}",
        True,
        HUD_TEXT
    )

    users_text = small_font.render(
        f"Users: {users}",
        True,
        HUD_TEXT
    )

    innovation_text = small_font.render(
        f"Innovation: {innovation}",
        True,
        HUD_TEXT
    )

    reputation_text = small_font.render(
        f"Reputation: {reputation}",
        True,
        HUD_TEXT
    )

    screen.blit(
        employees_text,
        (700, 125)
    )

    screen.blit(
        users_text,
        (700, 155)
    )

    screen.blit(
        innovation_text,
        (700, 185)
    )

    screen.blit(
        reputation_text,
        (700, 215)
    )

    # -------------------------
    # TOTAL CITY INCOME
    # -------------------------

    total_city_income = 0

    for row in range(GRID_SIZE):

        for col in range(GRID_SIZE):

            building = grid[row][col]

            if building != 0:

                # Count income strictly once at root tile for multi-tile buildings
                if building_origins.get((row, col), (row, col)) == (row, col):
                    total_city_income += building_income.get(building, 0)

    total_income_title = small_font.render(
        "Total City Income",
        True,
        HUD_SECONDARY
    )

    total_income_value = small_font.render(
        f"+Rs.{total_city_income} / 5 sec",
        True,
        HUD_TEXT
    )

    screen.blit(
        total_income_title,
        (700, 245)
    )

    screen.blit(
        total_income_value,
        (700, 275)
    )

    # =====================================================
    # HUD - BUILDING PANEL
    # =====================================================

    building_panel = pygame.Rect(
        680,
        335,
        290,
        190
    )

    pygame.draw.rect(
        screen,
        HUD_BG,
        building_panel,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        HUD_BORDER,
        building_panel,
        2,
        border_radius=12
    )

    # -------------------------
    # SELECTED BUILDING
    # -------------------------

    selected_name = building_names[current_building]
    selected_cost = building_costs[current_building]
    selected_income = building_income[current_building]

    building_title = small_font.render(
        "CURRENT BUILDING",
        True,
        HUD_SECONDARY
    )

    building_name_text = small_font.render(
        selected_name,
        True,
        HUD_TEXT
    )

    building_cost_text = small_font.render(
        f"Cost: Rs.{selected_cost}",
        True,
        HUD_TEXT
    )

    building_income_text = small_font.render(
        f"Income: +Rs.{selected_income} / 5 sec",
        True,
        HUD_TEXT
    )

    screen.blit(
        building_title,
        (700, 355)
    )

    screen.blit(
        building_name_text,
        (700, 385)
    )

    screen.blit(
        building_cost_text,
        (700, 420)
    )

    screen.blit(
        building_income_text,
        (700, 450)
    )

    # -------------------------
    # CONTROLS
    # -------------------------

    controls_line1 = small_font.render(
        "1: Office  2: Marketing  3: R&D  4: Road  5: Path",
        True,
        (200, 200, 200)
    )

    controls_line2 = small_font.render(
        "6: Trees  7: Lamp  8: Bench  9: Flowers  0: Campus  C: Data Ctr",
        True,
        (200, 200, 200)
    )

    screen.blit(
        controls_line1,
        (50, 652)
    )

    screen.blit(
        controls_line2,
        (50, 674)
    )
    # =====================================================
    # BUILD MENU
    # =====================================================

    # Build Menu title
    build_menu_title = small_font.render(
        "BUILD MENU",
        True,
        HUD_TEXT
    )

    screen.blit(
        build_menu_title,
        (680, 530)
    )

    # Draw Office button
    pygame.draw.rect(
        screen,
        building_colors[1],
        office_button,
        border_radius=8
    )

    # Draw Marketing button
    pygame.draw.rect(
        screen,
        building_colors[2],
        marketing_button,
        border_radius=8
    )

    # Draw R&D button
    pygame.draw.rect(
        screen,
        building_colors[3],
        rd_button,
        border_radius=8
    )

    # Button text
    office_name = button_font.render("OFFICE", True, HUD_TEXT)
    office_price = button_font.render("Rs.100", True, HUD_TEXT)

    marketing_name = button_font.render("MARKETING", True, HUD_TEXT)
    marketing_price = button_font.render("Rs.150", True, HUD_TEXT)

    rd_name = button_font.render("R&D", True, HUD_TEXT)
    rd_price = button_font.render("Rs.250", True, HUD_TEXT)

    # Office button
    screen.blit(office_name, office_name.get_rect(center=(office_button.centerx, office_button.centery - 10)))
    screen.blit(office_price, office_price.get_rect(center=(office_button.centerx, office_button.centery + 12)))

    # Marketing button
    screen.blit(marketing_name, marketing_name.get_rect(center=(marketing_button.centerx, marketing_button.centery - 10)))
    screen.blit(marketing_price, marketing_price.get_rect(center=(marketing_button.centerx, marketing_button.centery + 12)))

    # R&D button
    screen.blit(rd_name, rd_name.get_rect(center=(rd_button.centerx, rd_button.centery - 10)))
    screen.blit(rd_price, rd_price.get_rect(center=(rd_button.centerx, rd_button.centery + 12)))

    # -------------------------
    # UPDATE SCREEN
    # -------------------------

    pygame.display.flip()

    clock.tick(FPS)

# -----------------------------
# EXIT
# -----------------------------

pygame.quit()
sys.exit()