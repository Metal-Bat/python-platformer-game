import pygame
from tiles import Tile
from player import Player
from particles import ParticleEffect
from settings import title_size, screen_width
from support import import_folder


class Level:
    def __init__(self, level_data: list[str], screen: object) -> None:
        """level setup

        Args:
            level_data (list[str]): array of string contains X for set the blocks
            screen (object): screen object to draw item in it
        """
        self.display_screen: object = screen
        self.setup_level(level_data)
        self.world_shift: int = 0
        self.current_x = 0

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    def create_jump_particles(self, position: tuple):
        if self.player.sprite.facing_right:
            position -= pygame.math.Vector2(10, 5)
        else:
            position += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(position, "jump")
        self.dust_sprite.add(jump_particle_sprite)

    def setup_level(self, layout: list[str]) -> None:
        self.tiles: object = pygame.sprite.Group()
        self.player: object = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row):
                x: int = column_index * title_size
                y: int = row_index * title_size

                if cell == "X":
                    tile: object = Tile((x, y), title_size)
                    self.tiles.add(tile)
                if cell == "P":
                    player_sprite: object = Player((x, y), self.display_screen, self.create_jump_particles)
                    self.player.add(player_sprite)

    def scroll_x(self) -> None:
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 7
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -7
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 7

    def get_player_on_ground(self) -> None:
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self) -> None:
        if not self.player_on_ground and self.player.sprite.on_ground and self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land")
            self.dust_sprite.add(fall_dust_particle)

    def horizontal_movement(self) -> None:
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement(self) -> None:
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    player.in_jump_mod = False
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 0:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def run(self) -> None:
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_screen)

        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_screen)
        self.scroll_x()

        self.player.update()
        self.horizontal_movement()
        self.get_player_on_ground()
        self.vertical_movement()
        self.create_landing_dust()
        self.player.draw(self.display_screen)
