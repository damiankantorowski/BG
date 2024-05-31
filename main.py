import os.path
import sys
import pygame
import moderngl
from player import Player
from scene import Scene
from vao import VAO
from textures import Textures


class Game:
    def __init__(self):
        pygame.init()
        self.win_size = (1280, 720)
        self.path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        pygame.display.set_caption('Game')
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.set_mode(self.win_size, flags=pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        self.ctx = moderngl.create_context()
        self.ctx.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.delta_time = 0
        self.player = Player(self)
        self.vao = VAO(self)
        self.textures = Textures(self)
        self.scene = Scene(self)
        self.font1 = pygame.font.SysFont(None, 48)
        self.font2 = pygame.font.SysFont(None, 150)
        self.timer_surf = pygame.Surface(self.win_size, flags=pygame.SRCALPHA)
        self.timer_texture = self.ctx.texture(self.win_size, 4)
        self.timer_texture.swizzle = 'BGRA'
        self.is_running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.is_running = False

    def update(self):
        self.delta_time = self.clock.tick(60)
        self.time = pygame.time.get_ticks() * 0.001
        self.scene.update()
        self.player.update()

    def render(self):
        self.ctx.clear()
        self.scene.render()
        pygame.display.flip()
        

if __name__ == '__main__':
    game = Game()
    while game.is_running:
        game.handle_events()
        game.update()
        game.render()
    game.textures.destroy()
    game.vao.destroy()
    pygame.quit()
    sys.exit()
