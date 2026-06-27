import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from ui import init_fonts, draw_text
import sys



def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0
    large_font, small_font = init_fonts()
    center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    below_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
    

    # setting up groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # add class to Group
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, drawable, updatable)

    asteroidfield = AsteroidField()
    player = Player(x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2)

    def reset_game():
        updatable.empty()
        drawable.empty()
        asteroids.empty()
        shots.empty()

        AsteroidField()
        return Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)

    state = "start"

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_RETURN:
                    if state in ("start", "game_over"):
                        player = reset_game()
                        state = "playing"

        screen.fill("black")

        if state == "start":
            draw_text(screen, "ASTEROIDS", large_font, center)
            draw_text(screen, "Press Enter to Start", small_font, below_center)

        elif state == "playing":
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    log_event("player_hit")
                    state = "game_over"

            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        asteroid.split()
                        shot.kill()

            for object in drawable:
                object.draw(screen)

        elif state == "game_over":
            draw_text(screen, "GAME OVER", large_font, center)
            draw_text(screen, "Press Enter to Restart", small_font, below_center)

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
    main()
