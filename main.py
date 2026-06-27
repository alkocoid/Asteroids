import sys
import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, BASE_POINTS, ASTEROID_MAX_RADIUS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from scoring import ScoreManager
from ui import init_fonts, draw_text, draw_leaderboard




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
    score_manager = ScoreManager()
    player_name = ""

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_RETURN:
                    if state == "game_over":
                        if score_manager.is_high_score():
                            state = "name_entry"
                        else:
                            player = reset_game()
                            score_manager.reset()
                            state = "playing"
                    elif state in ("start", "leaderboard"):
                        player = reset_game()
                        score_manager.reset()
                        state = "playing"
                if state == "name_entry" and event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN and player_name:
                                score_manager.submit_score(player_name)
                                player_name = ""
                                state = "leaderboard"
                            elif event.key == pygame.K_BACKSPACE:
                                player_name = player_name[:-1]
                            elif len(player_name) < 12:
                                if event.unicode.isprintable():
                                    player_name += event.unicode

        screen.fill("black")

        if state == "start":
            draw_text(screen, "ASTEROIDS", large_font, center)
            draw_text(screen, "Press Enter to Start", small_font, below_center)

        elif state == "playing":
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    state = "game_over"

            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        points = int((ASTEROID_MAX_RADIUS / asteroid.radius) * BASE_POINTS)
                        score_manager.add_points(points)
                        asteroid.split()
                        shot.kill()
            
            draw_text(screen, f"Score: {score_manager.score}", small_font, (70, 20))
            
            for object in drawable:
                object.draw(screen)

        elif state == "game_over":
            draw_text(screen, "GAME OVER", large_font, center)
            draw_text(screen, f"Score: {score_manager.score}", small_font, below_center)
            if score_manager.is_high_score():
                draw_text(screen, "New High Score! Press Enter", small_font, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            else:
                draw_text(screen, "Press Enter to Restart", small_font, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))

        elif state == "name_entry":
            draw_text(screen, "Enter your name:", small_font, center)
            draw_text(screen, player_name, large_font, below_center)

        elif state == "leaderboard":
            draw_leaderboard(screen, score_manager, large_font, small_font, SCREEN_WIDTH)

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
    main()
