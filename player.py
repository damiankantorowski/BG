import glm
import pygame
from camera import Camera


PLAYER_POS = glm.vec3(0, 10, 0)
MOUSE_SENSITIVITY = 0.001
PLAYER_SPEED = 0.01
JUMP_SPEED = 0.002


class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=90, pitch=-20):
        self.app = app
        self.velocity = glm.vec3()
        self.is_jumping = False
        self.standing_on = None
        super().__init__(position, yaw, pitch)

    def update(self):
        self.mouse_control()
        self.keyboard_control()
        self.gravity()
        if self.position.y < -30:
            self.respawn()
        super().update()
    
    def respawn(self):
        self.position = glm.vec3(0, 10, 0)
        self.velocity = glm.vec3(0, 0, 0)
        self.yaw = glm.radians(90)
        self.pitch = glm.radians(-20)

    def mouse_control(self):
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        key_state = pygame.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time
        next_step = glm.vec3()
        if key_state[pygame.K_w]:
            next_step += self.move_forward(vel)
        if key_state[pygame.K_s]:
            next_step += self.move_back(vel)
        if key_state[pygame.K_a]:
            next_step += self.move_left(vel)
        if key_state[pygame.K_d]:
            next_step += self.move_right(vel)
        if key_state[pygame.K_SPACE] and self.standing_on:
            self.is_jumping = True
            self.velocity.y = JUMP_SPEED * self.app.delta_time
        if key_state[pygame.K_r]:
            self.app.scene.level = 1
            self.app.scene.load()
            self.app.scene.time = None
            self.app.scene.start_time = pygame.time.get_ticks()
            self.respawn()
        next_step = self.move_with_blocks(next_step)
        self.move(next_step)

    def move(self, next_step):
        if not self.collides(dx=next_step[0]):
            self.position.x += next_step[0]
        if not self.collides(dy=next_step[1]):
            self.position.y += next_step[1]
        if not self.collides(dz=next_step[2]):
            self.position.z += next_step[2]
            
    def move_with_blocks(self, next_step):
        if self.standing_on and self.standing_on.move_to:
            next_step += self.standing_on.delta_move
        return next_step

    def collides(self, dx=0, dy=0, dz=0):
        if dy == 0:
            dy = self.velocity.y * self.app.delta_time
        return any(obj.collides(self.position + glm.vec3(dx, dy, dz)) for obj in self.app.scene.objects)

    def gravity(self):
        self.position += self.velocity * self.app.delta_time
        ground = set(obj for obj in self.app.scene.objects if obj.below(self.position))
        self.standing_on = ground.pop() if ground else None
        if self.standing_on:
            self.velocity.y = 0
            self.is_jumping = False
        if self.is_jumping or not self.standing_on:
            self.velocity.y -= 0.0001 * self.app.delta_time
