import pygame
import moderngl
from model import *


NUM_LEVELS = 5

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.level = 1
        self.load()
        self.skybox = SkyBox(app)
        self.time = None
        self.start_time = pygame.time.get_ticks()

    def load(self):
        self.objects = []
        if self.level == 1:
            self.objects.append(Cube(self.app, tex_id=0, pos=(0, 0, 0)))
            self.objects.append(Cube(self.app, tex_id=0, pos=(0, 3, 6)))
            self.objects.append(Cube(self.app, tex_id=0, pos=(6, 6, 6)))
            self.objects.append(Cube(self.app, tex_id=0, pos=(6, 9, 0)))
            self.objects.append(Cube(self.app, tex_id=0, pos=(0, 12, 0)))
            self.objects.append(Cube(self.app, tex_id=0, pos=(0, 15, 6)))
            self.objects.append(Cube(self.app, tex_id=0, pos=(6, 18, 6)))
            self.objects.append(Cube(self.app, tex_id=0, pos=(6, 21, 0)))
            self.objects.append(Cube(self.app, tex_id=1, pos=(0, 24, 0)))
        elif self.level == 2:
            self.objects.append(Cube(self.app, tex_id=1, pos=(0, 0, 0)))
            self.objects.append(Cube(self.app, tex_id=1, pos=(0, 6, 6), move_to=(0, -2, 6)))
            self.objects.append(Cube(self.app, tex_id=1, pos=(0, -2, 12), move_to=(0, 6, 12)))
            self.objects.append(Cube(self.app, tex_id=1, pos=(0, 6, 18), move_to=(0, -2, 18)))
            self.objects.append(Cube(self.app, tex_id=1, pos=(0, -2, 24), move_to=(0, 6, 24)))
            self.objects.append(Cube(self.app, tex_id=2, pos=(0, 0, 30)))
        elif self.level == 3:
            self.objects.append(Cube(self.app, tex_id=2, pos=(0, 0, 0)))
            self.objects.append(Cube(self.app, tex_id=2, pos=(6, 0, 6), move_to=(-6, 0, 6)))
            self.objects.append(Cube(self.app, tex_id=2, pos=(0, 0, 12)))
            self.objects.append(Cube(self.app, tex_id=2, pos=(-6, 0, 18), move_to=(6, 0, 18)))
            self.objects.append(Cube(self.app, tex_id=2, pos=(0, 0, 24)))
            self.objects.append(Cube(self.app, tex_id=2, pos=(6, 0, 30), move_to=(-6, 0, 30)))
            self.objects.append(Cube(self.app, tex_id=2, pos=(0, 0, 36)))
            self.objects.append(Cube(self.app, tex_id=2, pos=(-6, 0, 42), move_to=(6, 0, 42)))
            self.objects.append(Cube(self.app, tex_id=2, pos=(0, 0, 48)))
            self.objects.append(Cube(self.app, tex_id=2, pos=(6, 0, 54), move_to=(-6, 0, 54)))
            self.objects.append(Cube(self.app, tex_id=3, pos=(0, 0, 60)))
        elif self.level == 4:
            self.objects.append(Cube(self.app, tex_id=3, pos=(0, 0, 0)))
            self.objects.append(Cube(self.app, tex_id=3, pos=(0, 0, 2), move_to=(0, 6, 12)))
            self.objects.append(Cube(self.app, tex_id=3, pos=(0, 12, 24), move_to=(0, 6, 14)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 12, 26)))
        elif self.level == 5:
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 0, 0)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 0, 2)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 0, 4)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 2, 4)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 4, 4)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 6, 4)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 8, 4)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 0, 6)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 0, 8)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 0, 10)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 0, 12)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 2, 12)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 4, 12)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 6, 12)))
            self.objects.append(Cube(self.app, tex_id=4, pos=(0, 8, 12)))
            self.objects.append(Cube(self.app, tex_id=5, pos=(0, 0, 14))) 
        elif self.level == 6:
            self.objects.append(Cube(self.app, tex_id=5, pos=(0, 0, 0)))
            self.objects.append(Cube(self.app, tex_id=5, pos=(0, 0, 2)))
            self.objects.append(Cube(self.app, tex_id=5, pos=(0, 0, -2)))
            self.objects.append(Cube(self.app, tex_id=5, pos=(2, 0, 0)))
            self.objects.append(Cube(self.app, tex_id=5, pos=(-2, 0, 0)))
            
    def render_timer(self): 
        self.app.timer_surf.fill((0,0,0,0))
        time = self.time if self.time else pygame.time.get_ticks() - self.start_time
        minutes = str(time // 60000).zfill(2)
        seconds = str((time // 1000) % 60).zfill(2)
        millisecond = str((time // 10) % 100).zfill(2)
        time_string = f'{minutes}:{seconds}:{millisecond}'
        if self.level == NUM_LEVELS + 1:
            text = self.app.font2.render(str(time_string), 1, (255, 255, 255) )
            rect = text.get_rect(center=(self.app.win_size[0]/2, self.app.win_size[1]/2))
        else:
            text = self.app.font1.render(str(time_string), 1, (255, 255, 255) )
            rect = text.get_rect(topleft=(self.app.win_size[0] - 150, 10))
        self.app.timer_surf.blit(text, rect)
        self.app.timer_surf = pygame.transform.flip(self.app.timer_surf, False, True)
        texture_data = self.app.timer_surf.get_view('1')
        self.app.timer_texture.write(texture_data)
        self.app.ctx.enable(moderngl.BLEND)
        self.app.timer_texture.use(location=0)
        self.app.vao.vaos['text'].render(mode=moderngl.TRIANGLE_STRIP)
        self.app.ctx.disable(moderngl.BLEND)

    def update(self):
        if self.objects[-1].below(self.app.player.position):
            if self.level < NUM_LEVELS:
                self.level += 1
                self.load()
                self.app.player.respawn()
            elif self.level == NUM_LEVELS:
                self.time = pygame.time.get_ticks() - self.start_time
                self.level = NUM_LEVELS + 1
                self.load()
                self.app.player.respawn()
            
    def render(self):
        for obj in self.objects:
            obj.render()
        self.skybox.render()
        self.render_timer()
