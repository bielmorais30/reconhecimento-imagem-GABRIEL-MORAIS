# entities.py — Player, Bullet, Asteroid sprites

import pygame
import random
import math
from settings import *


class Player(pygame.sprite.Sprite):
    """Player-controlled spaceship (triangle shape, Atari style)."""

    def __init__(self):
        super().__init__()
        self.width  = 36
        self.height = 42
        self.image  = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._draw_ship()

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom   = HEIGHT - 20

        self.shoot_cooldown = 0

    def _draw_ship(self):
        """Render the ship as a cyan triangle with engine glow."""
        self.image.fill((0, 0, 0, 0))  # transparent
        # Main hull
        pts = [
            (self.width // 2, 0),                  # nose
            (0,               self.height),          # bottom-left
            (self.width,      self.height),          # bottom-right
        ]
        pygame.draw.polygon(self.image, CYAN, pts)
        # Inner detail line
        inner = [
            (self.width // 2, 6),
            (4,               self.height - 4),
            (self.width - 4,  self.height - 4),
        ]
        pygame.draw.polygon(self.image, DIM_CYAN, inner, 2)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Clamp inside screen
        self.rect.left  = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def can_shoot(self):
        return self.shoot_cooldown <= 0

    def shoot(self):
        """Return a new Bullet and reset cooldown."""
        self.shoot_cooldown = SHOOT_COOLDOWN
        return Bullet(self.rect.centerx, self.rect.top)


class Bullet(pygame.sprite.Sprite):
    """Projectile fired by the player."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BULLET_W, BULLET_H), pygame.SRCALPHA)
        # Gradient look: bright center, dim edges
        pygame.draw.rect(self.image, YELLOW,      (0, 0, BULLET_W, BULLET_H), border_radius=2)
        pygame.draw.rect(self.image, WHITE,        (1, 0, 1,        BULLET_H // 3))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom   = y

    def update(self, *args):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    """Randomly shaped falling rock."""

    def __init__(self):
        super().__init__()
        self.size  = random.randint(ASTEROID_SIZE_MIN, ASTEROID_SIZE_MAX)
        self.speed = random.uniform(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)
        self.angle = 0                          # rotation angle
        self.spin  = random.uniform(-1.5, 1.5)  # degrees per frame

        # Generate an irregular polygon (8 vertices with noise)
        self._raw_pts = self._make_polygon(self.size)
        self.image     = self._render(self.angle)
        self.rect      = self.image.get_rect()
        self.rect.x    = random.randint(0, WIDTH - self.size * 2)
        self.rect.y    = -self.size * 2

        # Mask for pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)

    @staticmethod
    def _make_polygon(size):
        """Create jagged polygon points around a center."""
        pts = []
        num_verts = random.randint(7, 10)
        for i in range(num_verts):
            angle  = (2 * math.pi / num_verts) * i
            radius = size * random.uniform(0.65, 1.0)
            pts.append((
                math.cos(angle) * radius + size,
                math.sin(angle) * radius + size,
            ))
        return pts

    def _render(self, angle_deg):
        """Draw rotated asteroid onto a transparent surface."""
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        # Rotate points
        cx, cy = self.size, self.size
        rad = math.radians(angle_deg)
        rotated = [
            (
                cx + (p[0] - cx) * math.cos(rad) - (p[1] - cy) * math.sin(rad),
                cy + (p[0] - cx) * math.sin(rad) + (p[1] - cy) * math.cos(rad),
            )
            for p in self._raw_pts
        ]
        pygame.draw.polygon(surf, ORANGE,      rotated)
        pygame.draw.polygon(surf, RED,         rotated, 2)
        return surf

    def update(self, *args):
        self.rect.y += self.speed
        # Spin
        self.angle = (self.angle + self.spin) % 360
        center = self.rect.center
        self.image = self._render(self.angle)
        self.rect  = self.image.get_rect(center=center)
        self.mask  = pygame.mask.from_surface(self.image)
