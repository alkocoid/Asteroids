import pygame

def init_fonts():
    large_font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    return large_font, small_font

def draw_text(surface, text, font, pos):
    rendered = font.render(text, True, "white")
    rect = rendered.get_rect(center=pos)
    surface.blit(rendered, rect)

def draw_leaderboard(surface, score_manager, large_font, small_font, screen_width):
    surface.fill("black")
    draw_text(surface, "LEADERBOARD", large_font, (screen_width // 2, 80))
    for i, (name, score) in enumerate(score_manager.leaderboard):
        line = f"{i + 1}. {name}  -  {score}"
        y = 160 + i * 40
        draw_text(surface, line, small_font, (screen_width // 2, y))
    draw_text(surface, "Press Enter to play again", small_font, (screen_width // 2, 580))