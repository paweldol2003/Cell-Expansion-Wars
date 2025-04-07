# menu_scene.py
import pygame
import pygame_gui
import re
import sys


class MenuScene:
    def __init__(self, images, screen, manager):
        self.images = images
        self.screen = screen
        self.manager = manager
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.multi = False
        self.online = False
        self.font = pygame.font.SysFont(None, 36)

        self.create_buttons()
        self.create_ip_port_inputs()

    def create_buttons(self):
        center_x = self.screen_width // 2
        y_mode = int(self.screen_height * 0.15)
        button_width, button_height = 200, 50
        offset = 150

        self.buttons = [
            {"text": "Singleplayer", "multi": False, "rect": pygame.Rect(center_x - offset - button_width // 2, y_mode, button_width, button_height), "type": "mode"},
            {"text": "Multiplayer", "multi": True, "rect": pygame.Rect(center_x + offset - button_width // 2, y_mode, button_width, button_height), "type": "mode"},
            {"text": "Local", "rect": pygame.Rect(center_x - offset - button_width // 2, y_mode + 60, button_width, 40), "type": "net_mode", "online": False},
            {"text": "Online", "rect": pygame.Rect(center_x + offset - button_width // 2, y_mode + 60, button_width, 40), "type": "net_mode", "online": True},
        ]

        y_levels = y_mode + 120
        level_gap = 70

        for i in range(3):
            self.buttons.append({
                "text": f"Poziom {i+1}",
                "stage": f"stage_{i+1}",
                "rect": pygame.Rect(center_x - button_width // 2, y_levels + i * level_gap, button_width, button_height),
                "type": "single"
            })

        self.buttons.append({
            "text": "Poziom 3",
            "stage": "stage_3_multi",
            "rect": pygame.Rect(center_x - button_width // 2, y_levels, button_width, button_height),
            "type": "multi"
        })

        y_load = y_levels + 3 * level_gap + 30
        self.buttons.append({
            "text": "Wczytaj zapis (JSON)",
            "stage": "load_json",
            "rect": pygame.Rect(center_x - offset - button_width // 2, y_load, button_width, 40),
            "type": "load"
        })

        self.buttons.append({
            "text": "Wczytaj zapis (XML)",
            "stage": "load_xml",
            "rect": pygame.Rect(center_x + offset - button_width // 2, y_load, button_width, 40),
            "type": "load"
        })

        self.buttons.append({
            "text": "Wczytaj zapis (MongoDB)",
            "stage": "load_mongo",
            "rect": pygame.Rect(center_x - button_width // 2, y_load + 50, button_width, 40),
            "type": "load"
        })

    def create_ip_port_inputs(self):
        self.ip_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.screen_width - 200) // 2, 420, 200, 30),
            manager=self.manager
        )
        self.ip_input.set_text("192.168.0.1")
        self.ip_input.hide()

        self.port_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.screen_width - 200) // 2, 460, 200, 30),
            manager=self.manager
        )
        self.port_input.set_text("12345")
        self.port_input.hide()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.manager.process_events(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.buttons:
                    if btn["rect"].collidepoint(event.pos):
                        if btn["type"] == "mode":
                            self.multi = btn["multi"]
                        elif btn["type"] == "net_mode" and self.multi:
                            self.online = btn["online"]
                        elif btn["type"] == "load":
                            return btn["stage"]
                        elif (self.multi and btn["type"] == "multi") or (not self.multi and btn["type"] == "single"):
                            if self.multi and self.online:
                                if not self.validate_ip_port():
                                    print(" Błędny IP lub port!")
                                    return None
                            return btn["stage"]
        return None

    def validate_ip_port(self):
        ip = self.ip_input.get_text()
        port = self.port_input.get_text()
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if not ip_pattern.match(ip):
            return False
        parts = ip.split('.')
        if not all(0 <= int(p) <= 255 for p in parts):
            return False
        try:
            p = int(port)
            return 0 < p < 65536
        except ValueError:
            return False

    def update(self, time_delta):
        self.manager.update(time_delta)
        if self.multi and self.online:
            self.ip_input.show()
            self.port_input.show()
        else:
            self.ip_input.hide()
            self.port_input.hide()

    def draw(self, screen: pygame.Surface):
        screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()

        for btn in self.buttons:
            show = (
                btn["type"] == "mode" or
                (btn["type"] == "net_mode" and self.multi) or
                (btn["type"] == "single" and not self.multi) or
                (btn["type"] == "multi" and self.multi) or
                btn["type"] == "load"
            )

            if show:
                hovered = btn["rect"].collidepoint(mouse_pos)

                if btn["type"] == "mode":
                    color = (100, 200, 100) if btn["multi"] == self.multi else (70, 70, 200)
                elif btn["type"] == "net_mode":
                    color = (100, 150, 250) if btn["online"] == self.online else (70, 70, 200)
                else:
                    color = (70, 70, 200)

                if hovered:
                    color = tuple(min(255, c + 40) for c in color)

                pygame.draw.rect(screen, color, btn["rect"], border_radius=8)
                text = self.font.render(btn["text"], True, (255, 255, 255))
                text_rect = text.get_rect(center=btn["rect"].center)
                screen.blit(text, text_rect)

        self.manager.draw_ui(screen)
