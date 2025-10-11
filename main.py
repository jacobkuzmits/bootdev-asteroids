import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import (
    PLAYER_START_LIVES,
    SCORE_PER_ASTEROID,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from player import Player
from shot import Shot


def clear_groups(*groups: pygame.sprite.Group) -> None:
    for group in groups:
        for sprite in group.sprites():
            sprite.kill()


def handle_collisions(
    player: Player | None, asteroids: pygame.sprite.Group, shots: pygame.sprite.Group
) -> tuple[int, bool]:
    points = 0
    player_hit = False
    if player is None:
        return points, player_hit

    for asteroid in asteroids.sprites():
        if asteroid.is_colliding_with(player):
            player_hit = True
            break
        for shot in shots.sprites():
            if asteroid.is_colliding_with(shot):
                asteroid.split()
                shot.kill()
                points += SCORE_PER_ASTEROID
                break
    return points, player_hit


def draw_hud(
    screen: pygame.Surface, font: pygame.font.Font, score: int, lives: int
) -> None:
    score_text = font.render(f"Score: {score}", True, "white")
    screen.blit(score_text, (16, 16))
    lives_text = font.render(f"Lives: {lives}", True, "white")
    screen.blit(lives_text, (16, 16 + score_text.get_height() + 8))


def draw_menu(
    screen: pygame.Surface,
    title_font: pygame.font.Font,
    font: pygame.font.Font,
    last_score: int,
) -> None:
    screen_rect = screen.get_rect()
    title = title_font.render("Asteroids", True, "white")
    prompt = font.render("Press SPACE to start", True, "white")
    screen.blit(title, title.get_rect(center=(screen_rect.centerx, screen_rect.centery - 40)))
    screen.blit(
        prompt, prompt.get_rect(center=(screen_rect.centerx, screen_rect.centery + 10))
    )
    if last_score > 0:
        score_text = font.render(f"Last score: {last_score}", True, "white")
        screen.blit(
            score_text,
            score_text.get_rect(center=(screen_rect.centerx, screen_rect.centery + 50)),
        )


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0
    hud_font = pygame.font.Font(None, 28)
    title_font = pygame.font.Font(None, 72)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    player: Player | None = None
    score = 0
    last_score = 0
    lives = PLAYER_START_LIVES
    state = "menu"

    def begin_game() -> None:
        nonlocal player, score, lives, state
        clear_groups(asteroids, shots, updatable, drawable)
        score = 0
        lives = PLAYER_START_LIVES
        AsteroidField()
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        state = "playing"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if (
                state == "menu"
                and event.type == pygame.KEYDOWN
                and event.key in (pygame.K_SPACE, pygame.K_RETURN)
            ):
                begin_game()

        screen.fill("black")

        if state == "menu":
            draw_menu(screen, title_font, hud_font, last_score)
        elif state == "playing":
            updatable.update(dt)
            gained, player_hit = handle_collisions(player, asteroids, shots)
            score += gained
            if player_hit:
                if player is not None:
                    player.kill()
                player = None
                lives -= 1
                if lives > 0:
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                else:
                    last_score = score
                    state = "menu"
                    clear_groups(asteroids, shots, updatable, drawable)

            for sprite in drawable.sprites():
                sprite.draw(screen)
            draw_hud(screen, hud_font, score, lives)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
