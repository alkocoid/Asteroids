import pygame

def init_fonts():
    large_font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    return large_font, small_font

def draw_text(surface, text, font, pos):
    rendered = font.render(text, True, "white")
    rect = rendered.get_rect(center=pos)
    surface.blit(rendered, rect)