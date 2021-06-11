import pygame
from math import ceil
from typing import List, Dict, Tuple, Union, Optional
from buildings import Defence, Building


class MainWindow:
    WINDOW_SIZE: List[int] = [1250, 1015]
    WIDTH: int = 12
    HEIGHT: int = 12
    MARGIN: int = 1
    BUTTON_WIDTH: int = 85
    BUTTON_HEIGHT: int = 85
    BUTTON_MARGIN: int = 5

    BUILDINGS_COLORS: Dict[str, Tuple[int, int, int]] = {
        "Star Base": (81, 86, 181),
        "Compact House": (255, 234, 0),
        "Mine": (0, 255, 4),
        "Bank": (255, 196, 0),
        "Silo": (22, 166, 0),
        "Training Camp": (157, 10, 255),
        "Factory": (206, 10, 255),
        "Starport": (255, 0, 230),
        "Warp Gate": (99, 99, 99),
        "Laboratory": (41, 229, 242),
        "Observatory": (0, 191, 255),
        "Cannon Blast": (255, 68, 5),
        "Sniper Tower": (255, 0, 0),
        "Missile Launcher": (181, 36, 36),
        "Laser Tower": (227, 52, 70),
        "Mortar": (201, 10, 0),
        "Freeze Turret": (184, 245, 242),
        "Friends Bunker": (189, 67, 26),
        "Defence Bunker": (130, 48, 21),
        "Walls": (0, 0, 0),
        "Traps": (247, 111, 7)
    }
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    GREEN: Tuple[int, int, int] = (0, 255, 0)
    RED: Tuple[int, int, int] = (255, 0, 0)
    BACKGROUND: Tuple[int, int, int] = (255, 255, 255)
    
    def __init__(self, buildings_data: Dict[str, Union[Building, Defence]]):
        self.buildings_data: Dict[str, Union[Building, Defence]] = buildings_data
        self.screen: Optional[pygame.Surface] = None
        self.icon: pygame.surface.Surface = pygame.image.load("res/images/icon.png")
        self.create_window()
        self.name_font: pygame.font.Font = pygame.font.Font("res/fonts/FreeSansBold.ttf", 10)
        self.amount_font: pygame.font.Font = pygame.font.Font("res/fonts/impact.ttf", 16)
        self.buttons: Optional[Dict[str, pygame.rect.Rect]] = {}
        self.create_buttons()
        self.main_grid: pygame.rect.Rect = pygame.Rect(0, 0, 936, 1015)
        self.placed_objects: Optional[Dict[str, Union[pygame.rect.Rect, List[pygame.rect.Rect]]]] = {}
        self.place_starbase()
        self.main_loop()

    def create_window(self):
        pygame.init()
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("GLRBaseDesigner")
        self.screen: pygame.surface.Surface = pygame.display.set_mode(self.WINDOW_SIZE)

    def create_buttons(self):
        buildings: Optional[List[List[str, int]]] = []
        for building in self.buildings_data:
            buildings.append([building, self.buildings_data[building].amount])
        column: int = 0
        row: int = 1
        for building in buildings:
            if row == int(ceil(len(buildings)/2)) and len(buildings) % 2 != 0:
                obj: pygame.rect.Rect = pygame.Rect(self.BUTTON_MARGIN + 1000,
                                                    (self.BUTTON_MARGIN + self.BUTTON_HEIGHT) * row + (
                                                        self.BUTTON_MARGIN - self.BUTTON_HEIGHT),
                                                    self.BUTTON_WIDTH,
                                                    self.BUTTON_HEIGHT)
                self.buttons[building[0]]: pygame.rect.Rect = obj
            else:
                obj: pygame.rect.Rect = pygame.Rect((self.BUTTON_MARGIN + self.BUTTON_WIDTH) * column + (
                                                        self.BUTTON_MARGIN + 1000),
                                                    (self.BUTTON_MARGIN + self.BUTTON_HEIGHT) * row + (
                                                        self.BUTTON_MARGIN - self.BUTTON_HEIGHT),
                                                    self.BUTTON_WIDTH,
                                                    self.BUTTON_HEIGHT)
                self.buttons[building[0]]: pygame.rect.Rect = obj
            if column < 1:
                column += 1
            else:
                column = 0
                row += 1

    def text_to_buttons(self):
        for button in self.buttons:
            building: Union[Building, Defence] = self.buildings_data[button]
            building_name: pygame.surface.Surface = self.name_font.render(f"{' '.join(button.split('_')).title()}",
                                                                          True,
                                                                          self.BLACK)
            center_name: pygame.rect.Rect = building_name.get_rect(center=self.buttons[button].center)
            amount: pygame.surface.Surface = self.amount_font.render(f"{building.amount}",
                                                                     True,
                                                                     self.BLACK)
            x, y, _, _ = amount.get_rect(center=self.buttons[button].center)
            amount_posiotion: Dict[int, Tuple[int, int]] = {
                1: (x+36, y+34),
                2: (x+33, y+34),
                3: (x+29, y+34)
            }
            length = len(str(self.buildings_data[button].amount))
            self.screen.blit(amount, amount_posiotion[length])
            self.screen.blit(building_name, center_name)

    def text_to_object(self, obj_type: str, rect: pygame.rect.Rect):
        split_name: List[str] = obj_type.split()
        if len(split_name) == 2:
            text: pygame.surface.Surface = self.name_font.render(split_name[0], True, self.BLACK)
            x, y, _, _ = text.get_rect(center=rect.center)
            self.screen.blit(text, (x, y-5))
            text = self.name_font.render(split_name[1], True, self.BLACK)
            x, y, _, _ = text.get_rect(center=rect.center)
            self.screen.blit(text, (x, y+5))
        else:
            text = self.name_font.render(f"{obj_type}", True, self.BLACK)
            center_rect: pygame.rect.Rect = text.get_rect(center=rect.center)
            if obj_type.title() != "Walls" and obj_type.title() != "Traps":
                self.screen.blit(text, center_rect)

    def place_starbase(self):
        starbase: pygame.rect.Rect = pygame.Rect(31 * self.WIDTH + 31 * self.MARGIN,
                                                 34 * self.WIDTH + 34 * self.MARGIN,
                                                 10 * self.WIDTH + 10 * self.MARGIN,
                                                 10 * self.WIDTH + 10 * self.MARGIN)
        self.placed_objects["Star Base"]: pygame.rect.Rect = [starbase]
        pygame.draw.rect(self.screen,
                         self.BUILDINGS_COLORS["Star Base"],
                         starbase)

    def place_buttons(self):
        buildings: Optional[List[List[str, int]]] = []
        for building in self.buildings_data:
            buildings.append([building, self.buildings_data[building].amount])
        column: int = 0
        row: int = 1
        for building in buildings:
            if row == int(ceil(len(buildings) / 2)) and len(buildings) % 2 != 0:
                pygame.draw.rect(self.screen,
                                 self.WHITE,
                                 [self.BUTTON_MARGIN + 1000,
                                  (self.BUTTON_MARGIN + self.BUTTON_HEIGHT) * row + (
                                      self.BUTTON_MARGIN - self.BUTTON_HEIGHT),
                                  self.BUTTON_WIDTH,
                                  self.BUTTON_HEIGHT])
            else:
                pygame.draw.rect(self.screen,
                                 self.WHITE,
                                 [(self.BUTTON_MARGIN + self.BUTTON_WIDTH) * column + self.BUTTON_MARGIN + 1000,
                                  (self.BUTTON_MARGIN + self.BUTTON_HEIGHT) * row + (
                                      self.BUTTON_MARGIN - self.BUTTON_HEIGHT),
                                  self.BUTTON_WIDTH,
                                  self.BUTTON_HEIGHT])
            if column < 1:
                column += 1
            else:
                column = 0
                row += 1
        self.text_to_buttons()

    def draw_objects(self):
        for obj_type in self.placed_objects:
            for obj in self.placed_objects[obj_type]:
                color: Tuple[int, int, int] = self.BUILDINGS_COLORS[obj_type.title()]
                pygame.draw.rect(self.screen,
                                 color,
                                 obj)
                self.text_to_object(obj_type, obj)

    def remove_obj(self, pos: Tuple[int, int], dragging: bool = False) -> Tuple[str, float]:
        for obj_type in self.placed_objects:
            for obj in self.placed_objects[obj_type]:
                if obj.collidepoint(pos):
                    if obj_type == "Star Base" and dragging:
                        self.placed_objects[obj_type].remove(obj)
                    elif obj_type != "Star Base":
                        self.placed_objects[obj_type].remove(obj)
                        self.buildings_data[obj_type].amount += 1
                    if dragging:
                        if obj_type == "Star Base":
                            dragging_data = (obj_type, (10 * self.WIDTH) + (self.MARGIN * 10))
                        else:
                            dragging_data = (obj_type,
                                             (self.buildings_data[obj_type].get_size()[0] * self.WIDTH)+(
                                              self.MARGIN * self.buildings_data[obj_type].get_size()[0]))
                        return dragging_data

    def draw_radius(self, obj_type: str, rect: pygame.rect.Rect):
        if obj_type != "Star Base" and hasattr(self.buildings_data[obj_type], "radius"):
            center: Tuple[int, int] = rect.center
            pygame.draw.circle(self.screen,
                               (255, 0, 0),
                               center,
                               (self.buildings_data[obj_type].radius * self.WIDTH) + (
                                self.MARGIN * self.buildings_data[obj_type].radius), 4)

    def get_grid_coords(self) -> Tuple[int, int]:
        x, y = pygame.mouse.get_pos()
        ix: int = x // (self.WIDTH + 1)
        iy: int = y // (self.WIDTH + 1)
        cx, cy = ix * (self.WIDTH + 1), iy * (self.WIDTH + 1)
        return cx, cy

    def snap_to_grid(self, size) -> bool:
        cx, cy = self.get_grid_coords()
        highlight_surface: pygame.rect.Rect = pygame.Rect(cx, cy, size, size)
        color: Tuple[int, int, int] = (20, 199, 0)
        colliding: bool = False
        for obj_type in self.placed_objects:
            if highlight_surface.collidelistall(self.placed_objects[obj_type]):
                color = (255, 0, 0)
                colliding = True
        if not self.main_grid.contains(highlight_surface):
            colliding = True
        pygame.draw.rect(self.screen, color, highlight_surface)
        return colliding

    def update_screen(self):
        self.screen.fill(self.BLACK)
        for row in range(78):
            for column in range(72):
                color: Tuple[int, int, int] = self.BACKGROUND
                pygame.draw.rect(self.screen,
                                 color,
                                 [(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                                  (self.MARGIN + self.HEIGHT) * row + self.MARGIN,
                                  self.WIDTH,
                                  self.HEIGHT])
        self.place_buttons()
        self.draw_objects()
        pos: Tuple[int, int] = pygame.mouse.get_pos()
        for obj_type in self.placed_objects:
            for obj in self.placed_objects[obj_type]:
                if obj.collidepoint(pos):
                    self.draw_radius(obj_type, obj)

    def main_loop(self):
        running: bool = True
        dragging: Union[bool, Tuple[str, float]] = False
        colliding: bool = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    cx, cy = self.get_grid_coords()
                    if self.main_grid.collidepoint(pos) and dragging and not colliding and pygame.mouse.get_pressed(3)[0]:
                        building_type: str = dragging[0]
                        building_size: float = dragging[1]
                        if building_type not in self.placed_objects:
                            self.placed_objects[building_type]: pygame.rect.Rect = [pygame.Rect(cx,
                                                                                    cy,
                                                                                    building_size,
                                                                                    building_size)]
                        else:
                            self.placed_objects[building_type].append(pygame.Rect(cx,
                                                                                  cy,
                                                                                  building_size,
                                                                                  building_size))
                        if building_type != "Star Base":
                            if self.buildings_data[building_type].amount > 1:
                                self.buildings_data[building_type].amount -= 1
                            else:
                                self.buildings_data[building_type].amount -= 1
                                dragging = False
                        else:
                            dragging = False

                    elif self.main_grid.collidepoint(pos) and pygame.mouse.get_pressed(3)[2] and not dragging:
                        self.remove_obj(pos)

                    elif self.main_grid.collidepoint(pos) and not dragging and pygame.mouse.get_pressed(3)[0]:
                        dragging = self.remove_obj(pos, dragging=True)

                    elif not self.main_grid.collidepoint(pos) and dragging and dragging[0] != "Star Base":
                        dragging = False

                    else:
                        for button in self.buttons:
                            if self.buttons[button].collidepoint(pos) and not dragging and pygame.mouse.get_pressed(3)[0]:
                                if self.buildings_data[button].amount > 0:
                                    dragging = (button, (self.buildings_data[button].get_size()[0] * self.WIDTH) + (
                                                self.MARGIN * self.buildings_data[button].get_size()[0]))

            self.update_screen()
            if dragging:
                colliding = self.snap_to_grid(dragging[1])
            pygame.display.flip()
        pygame.quit()
