import sys
import pygame

from asteroidfield import AsteroidField
from asteroid import Asteroid
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, SCORE_PER_ASTEROID
from player import Player
from shot import Shot


def handle_collisions(
    player: Player, asteroids: pygame.sprite.Group, shots: pygame.sprite.Group
) -> int:
    points = 0
    for asteroid in asteroids.sprites():
        if asteroid.is_colliding_with(player):
            print("Game over!")
            sys.exit()
        for shot in shots.sprites():
            if asteroid.is_colliding_with(shot):
                asteroid.split()
                shot.kill()
                points += SCORE_PER_ASTEROID
                break
    return points


def draw_hud(screen: pygame.Surface, font: pygame.font.Font, score: int) -> None:
    score_text = font.render(f"Score: {score}", True, "white")
    screen.blit(score_text, (16, 16))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0
    font = pygame.font.Font(None, 28)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        score += handle_collisions(player, asteroids, shots)
        for sprite in drawable.sprites():
            sprite.draw(screen)
        draw_hud(screen, font, score)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
