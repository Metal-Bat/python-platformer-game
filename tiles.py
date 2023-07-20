import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, position: list[int], size: int) -> None:
        """Tile making class

        Args:
            position (List[int]): position of tile on screen
            size (int): size of tile on screen
        """
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("grey")
        self.rect = self.image.get_rect(topleft=position)

    def update(self, x_shift: int) -> None:
        """update position of tiles on screen

        Args:
            x_shift (int): speed and direction of move
        """
        self.rect.x += x_shift
