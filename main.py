import copy
from functools import reduce

import game
import pygame
from pygame.math import Vector2
from entity import Entity
from player import Player
from Tilemap import Tilemap
from animations import AnimatedSprite
import os
from enemy import Enemy


class PauseMenu:
    def __init__(self, options: dict):
        self.options = options
        self.selected = 0
        self.height = len(options) * game.font.get_height()
        self.padding_y = 5

    def render(self):
        for i, item in enumerate(self.options.keys()):
            surface = game.font.render(item, game.antialias, (0, 0, 0) if i == self.selected else (255, 255, 255))
            if i == self.selected:
                pygame.draw.rect(game.display, (255, 255, 255), ((game.DISPLAY_WIDTH - surface.get_width()) // 2,
                                                                 (
                                                                         game.DISPLAY_HEIGHT - self.height) // 2 + i * game.font.get_height() + i * self.padding_y,
                                                                 surface.get_width(), surface.get_height()))
            game.display.blit(surface, ((game.DISPLAY_WIDTH - surface.get_width()) // 2,
                                        (
                                                game.DISPLAY_HEIGHT - self.height) // 2 + i * game.font.get_height() + i * self.padding_y))

    def on_keypress(self, key):
        if key == pygame.K_DOWN:
            if self.selected < len(self.options) - 1:
                self.selected += 1
        if key == pygame.K_UP:
            if self.selected > 0:
                self.selected -= 1
        if key == pygame.K_RETURN:
            list(self.options.values())[self.selected]()


class SettingsMenu(PauseMenu):
    def __init__(self, options: list):
        super().__init__(options)

    def on_keypress(self, key):
        selected = self.options[self.selected]
        if key == pygame.K_RETURN:
            selected.on_select()
            # return otherwise the Pausemenu will try to call the widget which won't work!
            return
        selected.on_keypress(key)
        super().on_keypress(key)

    def render(self):
        for i, widget in enumerate(self.options):
            widget_surface: pygame.Surface = widget.render()
            offset_x = 100
            surface = game.font.render(widget.text, game.antialias, (0, 0, 0) if i == self.selected else (255, 255, 255))
            if i == self.selected:
                pygame.draw.rect(game.display, (255, 255, 255),
                                 ((game.DISPLAY_WIDTH - surface.get_width()) // 2 - offset_x,
                                  (
                                          game.DISPLAY_HEIGHT - self.height) // 2 + i * game.font.get_height() + i * self.padding_y,
                                  surface.get_width(), surface.get_height()))
            game.display.blit(surface, ((game.DISPLAY_WIDTH - surface.get_width()) // 2 - offset_x,
                                        (
                                                game.DISPLAY_HEIGHT - self.height) // 2 + i * game.font.get_height() + i * self.padding_y))
            if widget_surface:
                game.display.blit(widget_surface, (
                    game.DISPLAY_WIDTH // 2 + offset_x,
                    (game.DISPLAY_HEIGHT - self.height) // 2 + i * game.font.get_height() + i * self.padding_y))

    class MenuItem:
        def __init__(self, text=None, callback=None):
            self.height = game.font.get_height()
            self.text = text
            self.callback = callback
            self.value = None

        def get(self):
            return self.value

        def on_keypress(self, key):
            pass

        def render(self):
            pass

        def on_select(self):
            if self.callback:
                self.callback()

    class Checkbox(MenuItem):
        def __init__(self, value: bool, **kwargs):
            super().__init__(**kwargs)
            self.value = value
            self.size = self.height
            self.padding = 2

        def on_select(self):
            self.value = not self.value

        def render(self):
            surface = pygame.Surface((self.size, self.size))
            pygame.draw.rect(surface, (255, 255, 255), (0, 0, self.size, self.size), self.padding)
            inner_size = self.size - self.padding * 4
            if self.value:
                pygame.draw.rect(surface, (255, 255, 255), (self.padding * 2, self.padding * 2, inner_size, inner_size))
            return surface

    class ValueList(MenuItem):
        def __init__(self, values: list, **kwargs):
            super().__init__(**kwargs)
            self.values = values
            self.selected = 0

        def get(self):
            return self.values[self.selected]

        def render(self):
            return game.font.render(f"< {self.values[self.selected]} >", game.antialias, (255, 255, 255))

        def on_keypress(self, key):
            if key == pygame.K_LEFT:
                if self.selected > 0:
                    self.selected -= 1
                else:
                    self.selected = len(self.values) - 1
            if key == pygame.K_RIGHT:
                if self.selected < len(self.values) - 1:
                    self.selected += 1
                else:
                    self.selected = 0

    class Slider(MenuItem):
        def __init__(self, min, max, step, value, **kwargs):
            super().__init__(**kwargs)
            self.min = min
            self.max = max
            self.step = step
            self.value = value
            self.rect_width = 100

        def on_keypress(self, key):
            if key == pygame.K_LEFT:
                if self.value > self.min:
                    self.value -= self.step
            if key == pygame.K_RIGHT:
                if self.value < self.max:
                    self.value += self.step

        def render(self):
            text = game.font.render(str(self.value), game.antialias, (255, 255, 255))
            text_width = max(50, text.get_width())
            surface = pygame.Surface((self.rect_width + text_width, self.height))
            padding = 2
            pygame.draw.rect(surface, (255, 255, 255), (0, 0, self.rect_width, self.height), padding)
            inner_width = (self.value / self.max) * self.rect_width - padding * 4
            pygame.draw.rect(surface, (255, 255, 255),
                             (padding * 2, padding * 2, inner_width, self.height - padding * 4), 0)
            surface.blit(text, (self.rect_width + text_width - text.get_width(), 0))
            return surface


class Shuriken(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__("shuriken.png", *args, **kwargs)
        self.rotation = 0
        self.rotated_iamge = None
        self.new_rect = None

    def update(self):
        super().update()
        self.rotation += 1080 * game.dt

        self.rotated_image = pygame.transform.rotate(self.ent, self.rotation)
        self.new_rect = self.rotated_image.get_rect(center=self.ent.get_rect(topleft=self.position.xy).center)

    def render(self):
        game.display.blit(self.rotated_image, (self.new_rect.x - game.camera_x, self.new_rect.y))


class Game:
    def __init__(self):

        self.bg = (200, 200, 200)
        self.running = True
        self.level = Tilemap("map.tmj")
        self.keys_y = 0
        self.keys_x = 0
        self.man = Entity("Theguy.png", (100, 100))
        self.in_menu = False
        self.show_debug = True
        self.pause_menu = PauseMenu({
            "Resume": self.toggle_menu,
            "Settings": self.open_settings_menu,
            "Exit": self.exit,
        })
        self.settings_menu = SettingsMenu([
            SettingsMenu.Checkbox(self.show_debug, text="Show debug"),
            SettingsMenu.Checkbox(False, text="Fullscreen"),
            SettingsMenu.ValueList(game.resolutions, text="Resolution"),
            SettingsMenu.MenuItem(text="Save & Go Back", callback=self.save_settings)
        ])

        self.settings = {}
        for widget in self.settings_menu.options:
            self.settings[widget.text] = widget.get()

        self.active_menu = self.pause_menu
        game.vampire = Player("player", 500, "ninja.png", (1, 1))

    def save_settings(self):
        settings = {}
        for widget in self.settings_menu.options:
            settings[widget.text] = widget.get()
        if settings["Fullscreen"] != self.settings["Fullscreen"]:
            pygame.display.toggle_fullscreen()
        if settings["Resolution"] != self.settings["Resolution"]:
            game.DISPLAY_WIDTH, game.DISPLAY_HEIGHT = settings["Resolution"].split("x")
            game.DISPLAY_WIDTH = int(game.DISPLAY_WIDTH)
            game.DISPLAY_HEIGHT = int(game.DISPLAY_HEIGHT)
            game.display = pygame.Surface((game.DISPLAY_WIDTH, game.DISPLAY_HEIGHT))
        self.show_debug = settings["Show debug"]
        self.settings = settings
        self.toggle_menu()

    def open_settings_menu(self):
        self.in_menu = False  # force toggle_menu to flip back to True
        self.toggle_menu()
        self.active_menu = self.settings_menu

    def exit(self):
        self.running = False

    def toggle_menu(self):
        self.in_menu = not self.in_menu
        if self.in_menu:
            self.bg = (0, 0, 0)
        else:
            self.active_menu = self.pause_menu
            self.bg = (200, 200, 200)

    def charinput(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                shuriken = Shuriken(game.vampire.position)
                shuriken.velocity = pygame.mouse.get_pos() - (game.vampire.position - (game.camera_x, 0))
                shuriken.velocity.scale_to_length(1000)
                game.entities.append(shuriken)
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.keys_y -= 1

            if event.key == pygame.K_RIGHT:
                self.keys_x += 1
            if event.key == pygame.K_LEFT:
                self.keys_x -= 1

            if event.key == pygame.K_ESCAPE:
                self.toggle_menu()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.keys_x += 1
            if event.key == pygame.K_RIGHT:
                self.keys_x -= 1
            if event.key == pygame.K_UP:
                self.keys_y += 1

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.VIDEORESIZE:
                game.WINDOW_WIDTH, game.WINDOW_HEIGHT = event.size
            if self.in_menu:
                if event.type == pygame.KEYDOWN:
                    self.active_menu.on_keypress(event.key)
            self.charinput(event)

    def charactermovement(self):
        # acceleration by input

        if self.keys_y < 0 and game.vampire.grounded:
            game.vampire.velocity.y -= game.vampire.jump

        if abs(game.vampire.velocity.x) < game.vampire.max_vel.x:
            game.vampire.velocity.x += game.vampire.acceleration.x * self.keys_x * game.dt
        if game.vampire.velocity.y < -game.vampire.max_vel.y:
            game.vampire.velocity.y = -game.vampire.max_vel.y
        elif game.vampire.velocity.y > game.vampire.max_vel.y:
            game.vampire.velocity.y = game.vampire.max_vel.y

        # flipping
        if game.vampire.velocity.x < 0 and game.vampire.lookleft == False:
            game.vampire.ent.flipped = True
            count = 0
            for i in range(len(game.vampire.walkingimages)):
                game.vampire.walkingimages[count] = pygame.transform.flip(game.vampire.walkingimages[count], True,
                                                                          False)
                count += 1
            game.vampire.lookleft = True

        if game.vampire.velocity.x > 0 and game.vampire.lookleft == True:
            game.vampire.ent.flipped = False
            count = 0
            for i in range(len(game.vampire.walkingimages)):
                game.vampire.walkingimages[count] = pygame.transform.flip(game.vampire.walkingimages[count], True,
                                                                          False)
                count += 1
            game.vampire.lookleft = False

        if self.keys_x == 0:
            if abs(game.vampire.velocity.x) > game.vampire.min_speed:
                game.vampire.velocity.x -= game.vampire.velocity.x * game.vampire.deceleration * game.dt
            else:
                game.vampire.velocity.x = 0
        if self.keys_x < 0 and game.vampire.velocity.x > 0 or self.keys_x > 0 and game.vampire.velocity.x < 0:
            game.vampire.velocity.x -= game.vampire.velocity.x * game.vampire.deceleration * game.dt

        if not game.vampire.grounded:
            game.vampire.velocity.y += game.vampire.gravity * game.dt

        collisions = self.tile_collision(game.vampire.position, game.vampire.size, self.level.detectors)
        collided_w = 0
        if collisions["tl"] > 0:
            collided_w = collisions["tl"]
        if collisions["tr"] > 0:
            collided_w = collisions["tr"]
        if collisions["bl"] > 0:
            collided_w = collisions["bl"]
        if collisions["br"] > 0:
            collided_w = collisions["br"]
        if collided_w == 32:
            game.text("CHEST ! ! ! ", (game.DISPLAY_WIDTH / 2, game.font.get_height()), center=True)
            self.level.passthrough[159] = 44
            self.level.passthrough[160] = 44
            self.level.passthrough[161] = 44
            self.level.solids[159] = 0
            self.level.solids[160] = 0
            self.level.solids[161] = 0

        self.resolve_tile_collision(game.vampire)

        if not game.vampire.grounded and game.vampire.velocity.y > 0:
            game.vampire.ent.row = 2
        else:
            if game.vampire.velocity.x != 0:
                game.vampire.ent.row = 1
                game.vampire.ent.fps = 15
            else:
                game.vampire.ent.row = 0
                game.vampire.ent.fps = 2

        if game.vampire.position.x > game.camera_padding:
            if game.vampire.position.x - game.camera_x < game.camera_padding:
                game.camera_x = int(game.vampire.position.x - game.camera_padding)
        else:
            game.camera_x = 0
        if game.vampire.position.x - game.camera_x > game.DISPLAY_WIDTH - game.camera_padding:
            game.camera_x = int(game.vampire.position.x - game.DISPLAY_WIDTH + game.camera_padding)

    def resolve_tile_collision(self, entity):
        next_x = entity.position.x + entity.velocity.x * game.dt
        collisions = self.tile_collision(Vector2(next_x, entity.position.y), entity.size, self.level.solids)
        if entity.velocity.x <= 0:
            if collisions["tl"] > 0 or collisions["bl"] > 0 and not entity.grounded:
                next_x = self.get_tile_xy_at(*entity.position.xy).x
                entity.velocity.x = 0
        else:
            if collisions["tr"] > 0 or collisions["br"] > 0 and not entity.grounded:
                next_x = self.get_tile_xy_at(entity.position.x + self.level.tw // 2,
                                             entity.position.y).x - 1 + (self.level.tw - entity.size)
                entity.velocity.x = 0
        entity.position.x = next_x

        next_y = entity.position.y + entity.velocity.y * game.dt
        collisions = self.tile_collision(Vector2(entity.position.x, next_y), entity.size, self.level.solids)
        if collisions["tl"] > 0 or collisions["tr"] > 0:
            next_y = self.get_tile_xy_at(*entity.position.xy).y
            entity.velocity.y = 0
        if collisions["bl"] > 0 or collisions["br"] > 0:
            next_y = self.get_tile_xy_at(entity.position.x,
                                         entity.position.y + self.level.th // 2).y + (self.level.th - entity.size)
            entity.grounded = True
            entity.velocity.y = 0
        else:
            entity.grounded = False
        entity.position.y = next_y

    def get_tile_xy_at(self, x, y):
        tile_x = int(x // self.level.tw) * self.level.tw
        tile_y = int(y // self.level.th) * self.level.th
        return Vector2(tile_x, tile_y)

    def windowcolission(self):
        for i in [game.vampire]:
            # right side
            if i.position.x + i.size > game.camera_x + game.DISPLAY_WIDTH:
                i.position.x -= i.bounce
                i.velocity.x = abs(i.velocity.x) * -0.1
            # left side
            if i.position.x < 0:
                i.velocity.x = -abs(i.velocity.x) * -0.1
                i.position.x += i.bounce
            # top side
            if i.position.y < 0:
                i.velocity.y = -abs(i.velocity.y) * -0.1
                i.position.y += i.bounce

            if i.position.y + i.size > game.DISPLAY_HEIGHT:
                i.position.xy = (0, 0)

    def tile_collision(self, position: Vector2, size: int, layer):
        return {
            "tl": self.get_tile_at(*position.xy, layer),
            "tr": self.get_tile_at(position.x + size,
                                   position.y, layer),
            "bl": self.get_tile_at(position.x,
                                   position.y + size, layer),
            "br": self.get_tile_at(position.x + size,
                                   position.y + size, layer)
        }

    def get_tile_at(self, x, y, layer):
        tile_x = int(x // self.level.tw)
        tile_y = int(y // self.level.th)
        if 0 <= tile_x < self.level.width and 0 <= tile_y < self.level.height:
            tile_index = tile_x + tile_y * self.level.width
            return layer[tile_index]
        return -1

    def loop(self):
        clock = pygame.time.Clock()

        while self.running:
            game.dt = clock.tick(game.FPS) / 1000
            self.input()

            game.display.fill(self.bg)
            if self.in_menu:
                self.active_menu.render()
            else:
                self.level.render()

                self.charactermovement()
                self.windowcolission()

                # displaying every entity
                for entity in game.entities:
                    entity.update()
                    entity.render()
                game.vampire.render()
                self.man.render()

                if self.show_debug:
                    game.text(
                        f"grounded={game.vampire.grounded} x={game.vampire.position.x:06.1f} y={game.vampire.position.y:06.1f} camera={game.camera_x} entities={len(game.entities)} fps={1/game.dt:.0f}",
                        (0, game.DISPLAY_HEIGHT - game.font.get_height()))
            game.window.blit(pygame.transform.scale(game.display, (game.WINDOW_WIDTH, game.WINDOW_HEIGHT)), (0, 0))
            pygame.display.flip()


Game().loop()
