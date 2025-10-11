import pygame


class CircleShape(pygame.sprite.Sprite):
    """Common sprite base that keeps position, velocity, and radius state."""

    def __init__(self, x: float, y: float, radius: float) -> None:
        containers = getattr(self, "containers", ())
        if not isinstance(containers, tuple):
            containers = (containers,)
        super().__init__(*containers)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2()
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        raise NotImplementedError

    def update(self, dt: float) -> None:
        raise NotImplementedError

    def is_colliding_with(self, other: "CircleShape") -> bool:
        return pygame.Vector2.distance_to(self.position, other.position) < (
            self.radius + other.radius
        )
