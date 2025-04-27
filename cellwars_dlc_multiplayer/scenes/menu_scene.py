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

        # fonty
        self.title_font = pygame.font.SysFont(None, 72)
        self.font       = pygame.font.SysFont(None, 36)
        self.load_font  = pygame.font.SysFont(None, 24)

        # przygotuj przyciski i oblicz położenie inputów
        self.create_buttons()
        self.create_ip_port_inputs()

    def create_buttons(self):
        center_x = self.screen_width // 2
        y_mode   = int(self.screen_height * 0.15)

        # ─── wielkości przycisków poziomów ──────────────────────
        LEVELS = 6
        max_label = max((f"Poziom {i}" for i in range(1, LEVELS + 1)),
                        key=lambda t: self.font.size(t)[0])
        label_w, _    = self.font.size(max_label)
        button_w      = max(200, label_w + 20)
        button_h      = 50
        offset        = 150

        # ─── wielkości przycisków "Wczytaj…" ───────────────────
        load_texts = ["Wczytaj zapis (JSON)", "Wczytaj zapis (XML)", "Wczytaj zapis (MongoDB)"]
        max_load = max(load_texts, key=lambda t: self.load_font.size(t)[0])
        load_w, _   = self.load_font.size(max_load)
        load_w     = max(160, load_w + 20)
        load_h      = 30
        # ────────────────────────────────────────────────────────

        # tryb Single/Multi
        self.buttons = [
            {"text": "Singleplayer", "multi": False,
             "rect": pygame.Rect(center_x-offset-button_w//2, y_mode,         button_w, button_h),
             "type": "mode"},
            {"text": "Multiplayer",  "multi": True,
             "rect": pygame.Rect(center_x+offset-button_w//2, y_mode,         button_w, button_h),
             "type": "mode"},
            {"text": "Local",
             "rect": pygame.Rect(center_x-offset-button_w//2, y_mode+60,      button_w, 40),
             "type": "net_mode", "online": False},
            {"text": "Online",
             "rect": pygame.Rect(center_x+offset-button_w//2, y_mode+60,      button_w, 40),
             "type": "net_mode", "online": True},
        ]

        # przyciski poziomów w dwóch rzędach (3x2)
        y_levels = y_mode + 120
        cols     = 3
        gap_x    = 20
        gap_y    = 20
        total_w  = cols*button_w + (cols-1)*gap_x
        start_x  = center_x - total_w//2

        for i in range(LEVELS):
            row = i // cols
            col = i % cols
            x   = start_x + col*(button_w + gap_x)
            y   = y_levels + row*(button_h + gap_y)
            self.buttons.append({
                "text":  f"Poziom {i+1}",
                "stage": f"stage_{i+1}",
                "rect":  pygame.Rect(x, y, button_w, button_h),
                "type": "single",
            })

        # przycisk multi na miejscu Poziom 3
        self.buttons.append({
            "text":  "Poziom 3",
            "stage": "stage_3_multi",
            "rect":  pygame.Rect(start_x+2*(button_w+gap_x), y_levels, button_w, button_h),
            "type": "multi",
        })

        # przyciski wczytywania
        y_load = y_levels + 2*(button_h+gap_y) + 30
        self.buttons.extend([
            {"text": "Wczytaj zapis (JSON)",
             "stage": "load_json",
             "rect": pygame.Rect(center_x-offset-load_w//2, y_load,                load_w, load_h),
             "type": "load"},
            {"text": "Wczytaj zapis (XML)",
             "stage": "load_xml",
             "rect": pygame.Rect(center_x+offset-load_w//2, y_load,                load_w, load_h),
             "type": "load"},
            {"text": "Wczytaj zapis (MongoDB)",
             "stage": "load_mongo",
             "rect": pygame.Rect(center_x-load_w//2, y_load+load_h+10,              load_w, load_h),
             "type": "load"},
        ])

        # zapisz pozycję inputów poniżej tych wszystkich przycisków
        self.input_x      = (self.screen_width - 200)//2
        self.input_y      = y_load + load_h + 60
        self.port_input_y = self.input_y + 40

    def create_ip_port_inputs(self):
        # używamy wcześniej obliczonych współrzędnych, żeby nic nie zasłaniać
        self.ip_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(self.input_x, self.input_y, 200, 30),
            manager=self.manager
        )
        self.ip_input.set_text("192.168.0.1")
        self.ip_input.hide()

        self.port_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(self.input_x, self.port_input_y, 200, 30),
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
                        elif ((self.multi and btn["type"] == "multi") or
                              (not self.multi and btn["type"] == "single")):
                            if self.multi and self.online and not self.validate_ip_port():
                                print("Błędny IP lub port!")
                                return None
                            return btn["stage"]
        return None

    def validate_ip_port(self):
        ip   = self.ip_input.get_text()
        port = self.port_input.get_text()
        ip_pat = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if not ip_pat.match(ip):
            return False
        if not all(0 <= int(p) <= 255 for p in ip.split('.')):
            return False
        try:
            p = int(port)
            return 0 < p < 65536
        except:
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

        # rysuj tytuł
        title_surf = self.title_font.render("Cell Expansion Wars", True, (255,255,255))
        title_rect = title_surf.get_rect(center=(self.screen_width//2, 50))
        screen.blit(title_surf, title_rect)

        for btn in self.buttons:
            show = (
                btn["type"] == "mode" or
                (btn["type"] == "net_mode" and self.multi) or
                (btn["type"] == "single" and not self.multi) or
                (btn["type"] == "multi" and self.multi) or
                btn["type"] == "load"
            )
            if not show:
                continue

            # wybierz font
            font = self.load_font if btn["type"] == "load" else self.font

            # kolor
            if btn["type"] == "mode":
                color = (100,200,100) if btn["multi"]==self.multi else (70,70,200)
            elif btn["type"] == "net_mode":
                color = (100,150,250) if btn["online"]==self.online else (70,70,200)
            else:
                color = (70,70,200)

            if btn["rect"].collidepoint(mouse_pos):
                color = tuple(min(255,c+40) for c in color)

            pygame.draw.rect(screen, color, btn["rect"], border_radius=8)
            txt_s = font.render(btn["text"], True, (255,255,255))
            txt_r = txt_s.get_rect(center=btn["rect"].center)
            screen.blit(txt_s, txt_r)

        self.manager.draw_ui(screen)
