# game.py — Game orchestrator: loop, states, collisions, HUD

import pygame
import random
from settings import *
from entities import Player, Bullet, Asteroid


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock  = pygame.time.Clock()
        self.font_hud    = pygame.font.SysFont("monospace", 22, bold=True)
        self.font_large  = pygame.font.SysFont("monospace", 48, bold=True)
        self.font_medium = pygame.font.SysFont("monospace", 26, bold=True)
        self._init_state()

    # ── State ──────────────────────────────────────────────────────

    def _init_state(self):
        """Reset all game state (used on start and restart)."""
        self.all_sprites = pygame.sprite.Group()
        self.bullets     = pygame.sprite.Group()
        self.asteroids   = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.score       = 0
        self.frame_count = 0
        self.running     = True
        self.game_over   = False

    # ── Main entry ─────────────────────────────────────────────────

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            if self.game_over:
                self._handle_events_over()
                self._draw_game_over()
            else:
                self._handle_events()
                self._update()
                self._draw()

    # ── Events ─────────────────────────────────────────────────────

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self._try_shoot()

    def _handle_events_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._init_state()   # restart
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    # ── Shooting ───────────────────────────────────────────────────

    def _try_shoot(self):
        if self.player.can_shoot():
            bullet = self.player.shoot()
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)

    # ── Update ─────────────────────────────────────────────────────

    def _update(self):
        keys = pygame.key.get_pressed()

        # Hold space for continuous fire
        if keys[pygame.K_SPACE]:
            self._try_shoot()

        self.all_sprites.update(keys)
        self.frame_count += 1

        # Spawn asteroids
        if self.frame_count % SPAWN_RATE == 0:
            ast = Asteroid()
            self.asteroids.add(ast)
            self.all_sprites.add(ast)

        self._check_collisions()

    def _check_collisions(self):
        # Bullet × Asteroid — pixel-accurate via masks
        hits = pygame.sprite.groupcollide(
            self.bullets, self.asteroids,
            True, True,
            pygame.sprite.collide_mask
        )
        self.score += len(hits)

        # Asteroid × Player
        if pygame.sprite.spritecollideany(self.player, self.asteroids, pygame.sprite.collide_mask):
            self.game_over = True
            return

        # Asteroid reaches bottom of screen
        for ast in list(self.asteroids):
            if ast.rect.top > HEIGHT:
                self.game_over = True
                return

    # ── Draw ───────────────────────────────────────────────────────

    def _draw(self):
        self.screen.fill(DARK_GRAY)
        self._draw_stars()
        self.all_sprites.draw(self.screen)
        self._draw_hud()
        pygame.display.flip()

    def _draw_stars(self):
        """Static star field seeded by frame for subtle twinkle."""
        rng = random.Random(42)
        for _ in range(80):
            x = rng.randint(0, WIDTH - 1)
            y = rng.randint(0, HEIGHT - 1)
            b = rng.randint(60, 160)
            # Subtle twinkle every 40 frames
            if (self.frame_count // 40) % 2 == 0:
                b = min(255, b + 40)
            self.screen.set_at((x, y), (b, b, b))

    def _draw_hud(self):
        # Score
        score_surf = self.font_hud.render(f"SCORE  {self.score:05d}", True, CYAN)
        self.screen.blit(score_surf, (14, 12))
        # FPS (debug, dim)
        fps_surf = self.font_hud.render(f"FPS {int(self.clock.get_fps())}", True, (60, 80, 90))
        self.screen.blit(fps_surf, (WIDTH - 100, 12))

    def _draw_game_over(self):
        self.screen.fill(DARK_GRAY)
        self._draw_stars()

        # Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        # GAME OVER title
        title = self.font_large.render("GAME OVER", True, RED)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70)))

        # Score
        score_txt = self.font_medium.render(f"Pontuação: {self.score}", True, YELLOW)
        self.screen.blit(score_txt, score_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        # Instructions
        inst = self.font_medium.render("[R] Reiniciar   [ESC] Sair", True, WHITE)
        self.screen.blit(inst, inst.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60)))

        pygame.display.flip()
