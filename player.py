import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, position: list[int], screen: object, create_jump_particles: object) -> None:
        """initial player character

        Args:
            position (list[int]): default position of character
            screen (object): display screen
        """
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image: object = self.animations["idle"][self.frame_index]
        self.rect: object = self.image.get_rect(topleft=position)

        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_screen = screen
        self.create_jump_particles = create_jump_particles

        # player movement
        self.direction: object = pygame.math.Vector2(0, 0)
        self.speed = 7
        self.gravity = 0.8
        self.jump_speed = -16

        # player status
        self.status = "idle"
        self.facing_right = True

        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self) -> None:
        character_path = "graphics/character/"
        self.animations = {
            "idle": [],
            "run": [],
            "jump": [],
            "fall": [],
        }
        for animation in self.animations.keys():
            fullpath = character_path + animation
            self.animations[animation] = import_folder(fullpath)

    def import_dust_run_particles(self) -> None:
        self.dust_run_particle = import_folder("graphics/character/dust_particles/run")

    def animate(self) -> None:
        animations = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animations):
            self.frame_index = 0

        image = animations[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # set rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        if self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def run_dust_animation(self) -> None:
        if self.status == "run" and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particle):
                self.dust_frame_index = 0
            dust_particle = self.dust_run_particle[int(self.dust_frame_index)]
            if self.facing_right:
                position = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_screen.blit(dust_particle, position)
            else:
                position = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_screen.blit(flipped_dust_particle, position)

    def get_input(self) -> None:
        """get user input for character movement"""
        keys: object = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

        self.rect.x += self.direction.x * self.speed

    def get_status(self) -> None:
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 1:
            self.status = "fall"
        else:
            if self.direction.x != 0:
                self.status = "run"
            else:
                self.status = "idle"

    def apply_gravity(self) -> None:
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self) -> None:
        self.direction.y = self.jump_speed

    def update(self) -> None:
        """update character position"""
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
