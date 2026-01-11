import pygame
from typing import List, Tuple, Callable
from constants import WIDTH, HEIGHT, COLORS, FPS

class Menu:
    def __init__(self, win: pygame.Surface):
        self.win = win
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont('comicsans', 70)
        self.font_item = pygame.font.SysFont('comicsans', 50)
        self.selected_idx = 0
        
        # Menu Options
        self.items: List[Tuple[str, Callable]] = []
        self.running = True
        
        # Settings (defaults)
        self.grid_size = 20  # Example default
        self.mode = "PvP"    # PvP, Single, PvAI

    def add_item(self, text: str, action: Callable):
        self.items.append((text, action))

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(FPS)
            self._handle_input()
            self._draw()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_idx = (self.selected_idx - 1) % len(self.items)
                elif event.key == pygame.K_DOWN:
                    self.selected_idx = (self.selected_idx + 1) % len(self.items)
                elif event.key == pygame.K_RETURN:
                    # Execute the callback
                    _, action = self.items[self.selected_idx]
                    if action:
                        action()

    def _draw(self):
        self.win.fill(COLORS['BLACK'])
        
        # Draw Title
        title_text = self.font_title.render("Snake Battle", 1, COLORS['WHITE'])
        self.win.blit(title_text, (WIDTH/2 - title_text.get_width()/2, 100))

        # Draw Items
        for idx, (text, _) in enumerate(self.items):
            color = COLORS['RED'] if idx == self.selected_idx else COLORS['WHITE']
            item_text = self.font_item.render(text, 1, color)
            self.win.blit(item_text, (WIDTH/2 - item_text.get_width()/2, 250 + idx * 70))
            
        pygame.display.update()
