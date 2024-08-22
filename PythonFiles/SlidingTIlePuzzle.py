import pygame
import pygame_gui
import random

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

animations_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((550, 60), (200, 40)),
    text="Animations",
    manager=manager
)

grid_size = 3
tile_size = 100
grid_margin = 5
grid_origin = ((WINDOW_SIZE[0] - (grid_size * (tile_size + grid_margin))) // 2,
               ((WINDOW_SIZE[1] - 100) - (grid_size * (tile_size + grid_margin))) // 2 + 100)

tiles = []
for i in range(grid_size * grid_size):
    tiles.append(i)

def draw_grid():
    for i in range(grid_size):
        for j in range(grid_size):
            if tiles[i * grid_size + j] != grid_size * grid_size - 1:
                pygame.draw.rect(screen, TILE_COLOR, (
                    grid_origin[0] + j * (tile_size + grid_margin),
                    grid_origin[1] + i * (tile_size + grid_margin),
                    tile_size, tile_size
                ))
                font = pygame.font.Font(None, 36)
                text = font.render(str(tiles[i * grid_size + j] + 1), True, (0, 0, 0))
                text_rect = text.get_rect(center=(
                    grid_origin[0] + j * (tile_size + grid_margin) + tile_size // 2,
                    grid_origin[1] + i * (tile_size + grid_margin) + tile_size // 2
                ))
                screen.blit(text, text_rect)

def handle_tile_click(pos):
    x, y = pos
    grid_x = (x - grid_origin[0]) // (tile_size + grid_margin)
    grid_y = (y - grid_origin[1]) // (tile_size + grid_margin)
    
    if 0 <= grid_x < grid_size and 0 <= grid_y < grid_size:
        index = grid_y * grid_size + grid_x
        empty_index = tiles.index(grid_size * grid_size - 1)
        
        if index - 1 == empty_index and index % grid_size != 0:  
            tiles[index], tiles[empty_index] = tiles[empty_index], tiles[index]
        elif index + 1 == empty_index and (index + 1) % grid_size != 0:  
            tiles[index], tiles[empty_index] = tiles[empty_index], tiles[index]
        elif index - grid_size == empty_index:  
            tiles[index], tiles[empty_index] = tiles[empty_index], tiles[index]
        elif index + grid_size == empty_index:  
            tiles[index], tiles[empty_index] = tiles[empty_index], tiles[index]

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                handle_tile_click(event.pos)
        
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == difficulty_dropdown:
                grid_size = int(event.text.split('x')[0])
                tile_size = 500 // grid_size
                grid_origin = ((WINDOW_SIZE[0] - (grid_size * (tile_size + grid_margin))) // 2,
                               ((WINDOW_SIZE[1] - 100) - (grid_size * (tile_size + grid_margin))) // 2 + 100)
                tiles = list(range(grid_size * grid_size))
                random.shuffle(tiles)
        
        manager.process_events(event)
    
    manager.update(time_delta)
    
    screen.fill(BACKGROUND_COLOR)
    manager.draw_ui(screen)
    draw_grid()
    
    pygame.display.update()

pygame.quit()