import pygame
import pygame_gui
import random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)  
TILE_COLOR = (100, 100, 250)  
EMPTY_COLOR = BACKGROUND_COLOR 

window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Sliding Tile Puzzle')
manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
header_rect = pygame.Rect(0, 0, WINDOW_WIDTH, 50)
header_surface = pygame.Surface(header_rect.size)
header_surface.fill((240, 240, 240))  

puzzle_box_size = 400
puzzle_box_rect = pygame.Rect((WINDOW_WIDTH - puzzle_box_size) // 2,
                              (WINDOW_HEIGHT - puzzle_box_size) // 2 + 50,
                              puzzle_box_size,
                              puzzle_box_size)

difficulty = 3
tile_size = puzzle_box_size // difficulty
tiles = []
empty_tile_pos = (difficulty - 1, difficulty - 1)


button_size = (200, 50)
button_padding = 20
buttons_start_x = (WINDOW_WIDTH - 3 * button_size[0] - 2 * button_padding) // 2
button_y = header_rect.height + button_padding

choose_image_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(buttons_start_x, button_y, *button_size),
    text='Choose Image',
    manager=manager
)

difficulty_options = ['3x3', '4x4', '5x5', '6x6', '7x7', '8x8']
difficulty_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=difficulty_options,
    starting_option='3x3',
    relative_rect=pygame.Rect(buttons_start_x + button_size[0] + button_padding, button_y, *button_size),
    manager=manager
)

animations_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(buttons_start_x + 2 * (button_size[0] + button_padding), button_y, *button_size),
    text='Animations',
    manager=manager
)

clock = pygame.time.Clock()

def create_grid():
    global tiles, empty_tile_pos
    tiles = [(i * difficulty + j + 1) for i in range(difficulty) for j in range(difficulty)]
    tiles[-1] = 0 
    empty_tile_pos = (difficulty - 1, difficulty - 1)
    random.shuffle(tiles)

def draw_grid():
    for i in range(difficulty):
        for j in range(difficulty):
            tile_value = tiles[i * difficulty + j]
            tile_rect = pygame.Rect(puzzle_box_rect.left + j * tile_size,
                                    puzzle_box_rect.top + i * tile_size,
                                    tile_size, tile_size)
            if tile_value:
                pygame.draw.rect(window_surface, TILE_COLOR, tile_rect)
                font = pygame.font.Font(None, 50)
                text_surf = font.render(str(tile_value), True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=tile_rect.center)
                window_surface.blit(text_surf, text_rect)
            else:
                pygame.draw.rect(window_surface, EMPTY_COLOR, tile_rect)

def is_solvable(tile_list):
    inversions = 0
    for i in range(len(tile_list)):
        for j in range(i + 1, len(tile_list)):
            if tile_list[i] and tile_list[j] and tile_list[i] > tile_list[j]:
                inversions += 1
    return inversions % 2 == 0


def get_tile_position(mouse_pos):
    x, y = mouse_pos
    if puzzle_box_rect.collidepoint(mouse_pos):
        grid_x = (x - puzzle_box_rect.left) // tile_size
        grid_y = (y - puzzle_box_rect.top) // tile_size
        return grid_y, grid_x
    return None

def move_tile(tile_pos):
    global empty_tile_pos
    x, y = tile_pos
    ex, ey = empty_tile_pos
    if (x == ex and abs(y - ey) == 1) or (y == ey and abs(x - ex) == 1):
        tiles[ex * difficulty + ey], tiles[x * difficulty + y] = tiles[x * difficulty + y], tiles[ex * difficulty + ey]
        empty_tile_pos = (x, y)

create_grid()

is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == difficulty_dropdown:
                difficulty = int(event.text[0])
                tile_size = puzzle_box_size // difficulty
                create_grid()

        manager.process_events(event)
    manager.update(time_delta)
    window_surface.fill(BACKGROUND_COLOR)
    window_surface.blit(header_surface, header_rect.topleft)
    draw_grid()
    manager.draw_ui(window_surface)
    pygame.display.update()
pygame.quit()
