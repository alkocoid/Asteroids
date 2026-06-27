from circleshape import CircleShape
import pygame
import random
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event

class Asteroid(CircleShape):

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        super().update(dt)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        random_angle = random.uniform(20.0, 50.0)
        velo_a = self.velocity.rotate(random_angle)
        velo_b = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        a_asteroid = self._spawn_child(new_radius)
        b_asteroid = self._spawn_child(new_radius)
        a_asteroid.velocity = velo_a * 1.2
        b_asteroid.velocity = velo_b * 1.2

    def _spawn_child(self, radius):
        if random.random() < 0.1:
            cls = random.choices(POWER_UP_TYPES, weights=POWER_UP_WEIGHTS, k=1)[0]
        else:
            cls = Asteroid
        return cls(self.position.x, self.position.y, radius)

class PowerUp(Asteroid):

    color = (255, 255, 255)

    def draw(self, screen):
        # common drawing logic
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def apply(self, player):
        raise NotImplementedError("Subclasses must implement apply()")

class ShieldPowerUp(PowerUp):
    color = (0, 100, 255)

    def apply(self, player):
        player.invincible_timer = min(player.invincible_timer + 5, 30)

class SpeedPowerUp(PowerUp):
    color = (255, 200, 0)

    def apply(self, player):
        player.speed_multiplier = min(player.speed_multiplier * 1.5, 10)

class LiveUp(PowerUp):
    color = (255, 0, 0)

    def apply(self, player):
        player.lives += 1

class ShootSpeedPowerUp(PowerUp):
    color = (255, 100, 0)

    def apply(self, player):
        player.shoot_speed_multiplier = min(player.shoot_speed_multiplier * 1.5, 10.0)

class ShootRatePowerUp(PowerUp):
    color = (0, 255, 100)

    def apply(self, player):
        player.cooldown_multiplier = max(player.cooldown_multiplier * 0.75, 0.1)

POWER_UP_TYPES = [ShieldPowerUp, SpeedPowerUp, ShootSpeedPowerUp, ShootRatePowerUp, LiveUp]
POWER_UP_WEIGHTS = [5, 5, 5, 5, 2]