import glm
import math

ASPECT_RATIO = 16/9 
V_FOV = glm.radians(60)
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)
NEAR = 0.01
FAR = 2000.0
PITCH_MAX = glm.radians(89)

class Camera:
    def __init__(self, position, yaw, pitch):
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, 1)
        self.rotation = glm.vec3(0, 0, 0)
        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4()

    def update(self):
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        self.m_view = glm.lookAt(self.position, self.position + self.rotation, self.up)

    def update_vectors(self):
        self.forward.x = glm.cos(self.yaw)
        self.forward.z = glm.sin(self.yaw)
        self.rotation.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.rotation.y = glm.sin(self.pitch)
        self.rotation.z = glm.sin(self.yaw) * glm.cos(self.pitch)
        self.rotation = glm.normalize(self.rotation)
        self.rotation = glm.clamp(self.rotation, -1, 1)
        self.right = glm.normalize(glm.cross(self.rotation, glm.vec3(0, 1, 0)))

    def rotate_pitch(self, delta_y):
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
        self.yaw += delta_x

    def move_left(self, velocity):
        return -self.right * velocity

    def move_right(self, velocity):
        return self.right * velocity

    def move_forward(self, velocity):
        return self.forward * velocity

    def move_back(self, velocity):
        return -self.forward * velocity
