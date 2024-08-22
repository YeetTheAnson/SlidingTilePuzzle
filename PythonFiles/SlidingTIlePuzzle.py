import pygame
import pygame_gui
import random
import time

pygame.init()
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Sliding Tile Puzzle")

manager = pygame_gui.UIManager(WINDOW_SIZE, 'theme.json')

BACKGROUND_COLOR = (240, 240, 240)
ACCENT_COLOR = (0, 120, 212)
TILE_COLOR = (255, 255, 255)

header = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, 0), (800, 50)),
    text="Score: 0",
    manager=manager
)

choose_image_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 60), (200, 40)),
    text="Choose Image",
    manager=manager
)

difficulty_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=['3x3', '4x4', '5x5', '6x6', '7x7', '8x8'],
    starting_option='3x3',
    relative_rect=pygame.Rect((300, 60), (200, 40)),
    manager=manager
)

animations_toggle = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((550, 60), (200, 40)),
    text="Animations: Off",
    manager=manager
)

shuffle_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 550), (200, 40)),
    text="Shuffle",
    manager=manager
)

grid_size = 3
grid_area = 400
tile_size = grid_area // grid_size
grid_margin = 2
grid_origin = ((WINDOW_SIZE[0] - grid_area) // 2, (WINDOW_SIZE[1] - grid_area) // 2)

tiles = list(range(grid_size * grid_size))

animation_speed = 10
animating_tiles = []
use_animations = False

def is_solved():
    return tiles == list(range(grid_size * grid_size))

def draw_grid():
    for i in range(grid_size):
        for j in range(grid_size):
            if tiles[i * grid_size + j] != grid_size * grid_size - 1:
                tile_rect = pygame.Rect(
                    grid_origin[0] + j * (tile_size + grid_margin),
                    grid_origin[1] + i * (tile_size + grid_margin),
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, TILE_COLOR, tile_rect)
                font = pygame.font.Font(None, tile_size // 2)
                text = font.render(str(tiles[i * grid_size + j] + 1), True, (0, 0, 0))
                text_rect = text.get_rect(center=tile_rect.center)
                screen.blit(text, text_rect)

def handle_tile_click(pos):
    global tiles
    x, y = pos
    grid_x = (x - grid_origin[0]) // (tile_size + grid_margin)
    grid_y = (y - grid_origin[1]) // (tile_size + grid_margin)
    
    if 0 <= grid_x < grid_size and 0 <= grid_y < grid_size:
        index = grid_y * grid_size + grid_x
        empty_index = tiles.index(grid_size * grid_size - 1)
        
        if index - 1 == empty_index and index % grid_size != 0:  # Left
            swap_tiles(index, empty_index)
        elif index + 1 == empty_index and (index + 1) % grid_size != 0:  # Right
            swap_tiles(index, empty_index)
        elif index - grid_size == empty_index:  # Above
            swap_tiles(index, empty_index)
        elif index + grid_size == empty_index:  # Below
            swap_tiles(index, empty_index)

def swap_tiles(index1, index2):
    global tiles, animating_tiles
    if use_animations:
        animating_tiles = [(index1, index2, 0)]
    else:
        tiles[index1], tiles[index2] = tiles[index2], tiles[index1]

def update_animations():
    global tiles, animating_tiles
    if animating_tiles:
        index1, index2, progress = animating_tiles[0]
        progress += animation_speed
        if progress >= tile_size + grid_margin:
            tiles[index1], tiles[index2] = tiles[index2], tiles[index1]
            animating_tiles = []
        else:
            animating_tiles[0] = (index1, index2, progress)

def draw_animations():
    if animating_tiles:
        index1, index2, progress = animating_tiles[0]
        y1, x1 = divmod(index1, grid_size)
        y2, x2 = divmod(index2, grid_size)
        
        direction = (x2 - x1, y2 - y1)
        
        if progress > tile_size:
            overshoot = progress - tile_size
            progress = tile_size - overshoot * 0.3
        
        tile_rect = pygame.Rect(
            grid_origin[0] + x1 * (tile_size + grid_margin) + direction[0] * progress,
            grid_origin[1] + y1 * (tile_size + grid_margin) + direction[1] * progress,
            tile_size, tile_size
        )
        pygame.draw.rect(screen, TILE_COLOR, tile_rect)
        font = pygame.font.Font(None, tile_size // 2)
        text = font.render(str(tiles[index1] + 1), True, (0, 0, 0))
        text_rect = text.get_rect(center=tile_rect.center)
        screen.blit(text, text_rect)

def shuffle_tiles():
    global tiles
    empty_index = tiles.index(grid_size * grid_size - 1)
    for _ in range(1000):
        possible_moves = []
        if empty_index % grid_size != 0:
            possible_moves.append(empty_index - 1)
        if (empty_index + 1) % grid_size != 0:
            possible_moves.append(empty_index + 1)
        if empty_index >= grid_size:
            possible_moves.append(empty_index - grid_size)
        if empty_index < grid_size * (grid_size - 1):
            possible_moves.append(empty_index + grid_size)
        
        move = random.choice(possible_moves)
        tiles[empty_index], tiles[move] = tiles[move], tiles[empty_index]
        empty_index = move

clock = pygame.time.Clock()
is_running = True

shuffle_tiles()

while is_running:
    time_delta = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not animating_tiles:
                handle_tile_click(event.pos)
        
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == difficulty_dropdown:
                grid_size = int(event.text.split('x')[0])
                tile_size = grid_area // grid_size
                tiles = list(range(grid_size * grid_size))
                shuffle_tiles()
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == animations_toggle:
                use_animations = not use_animations
                animations_toggle.set_text(f"Animations: {'On' if use_animations else 'Off'}")
            elif event.ui_element == shuffle_button:
                shuffle_tiles()
        
        manager.process_events(event)
    
    manager.update(time_delta)
    
    screen.fill(BACKGROUND_COLOR)
    
    if not animating_tiles:
        draw_grid()
    else:
        draw_grid()
        draw_animations()
        update_animations()
    
    manager.draw_ui(screen)
    
    if is_solved():
        font = pygame.font.Font(None, 72)
        text = font.render("You Win!", True, ACCENT_COLOR)
        text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
        screen.blit(text, text_rect)
    
    pygame.display.update()

pygame.quit()