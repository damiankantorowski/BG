import os.path
import pygame
import moderngl


class Textures:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.path = os.path.join(app.path, 'textures')
        self.textures = {}
        self.textures[0] = self.get_texture(os.path.join(self.path, '0.png'))
        self.textures[1] = self.get_texture(os.path.join(self.path, '1.png'))
        self.textures[2] = self.get_texture(os.path.join(self.path, '2.png'))
        self.textures[3] = self.get_texture(os.path.join(self.path, '3.png'))
        self.textures[4] = self.get_texture(os.path.join(self.path, '4.png'))
        self.textures[5] = self.get_texture(os.path.join(self.path, '5.png'))
        self.textures['skybox'] = self.get_texture_cube(os.path.join(self.path, 'skybox'))

    def get_texture_cube(self, path):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        textures = []
        for face in faces:
            texture = pygame.image.load(os.path.join(path, f'{face}.jpg')).convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pygame.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)
        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)
        for i in range(6):
            texture_data = pygame.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)
        return texture_cube

    def get_texture(self, path):
        texture = pygame.image.load(path).convert()
        texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pygame.image.tostring(texture, 'RGB'))
        texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
        texture.build_mipmaps()
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
