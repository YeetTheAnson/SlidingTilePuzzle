import pygame
import pygame_gui

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255) 

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
puzzle_box_surface = pygame.Surface(puzzle_box_rect.size)
puzzle_box_surface.fill((230, 230, 230))  

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

is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0
    # limit to 60fps to prevent performance issue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.fill(BACKGROUND_COLOR)
    window_surface.blit(header_surface, header_rect.topleft)
    window_surface.blit(puzzle_box_surface, puzzle_box_rect.topleft)
    manager.draw_ui(window_surface)
    pygame.display.update()

pygame.quit()
