import glm


BLOCKS_SPEED = 0.005


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.pos = glm.vec3(pos)
        self.vao_name = vao_name
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = glm.vec3(scale)
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = app.player

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.pos)
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def render(self):
        self.update()
        self.vao.render()


class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.texture = self.app.textures.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use(location=0)
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def update(self):
        self.m_model = self.get_model_matrix()
        self.texture.use(location=0)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)


class Cube(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), move_to=None):
        self.move_to = glm.vec3(move_to) if move_to else None
        self.start_pos = glm.vec3(pos)
        self.end_pos = glm.vec3(move_to) if move_to else None
        self.delta_move = glm.vec3()
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
     
    def below(self, player_position):
        p = player_position
        c = self.pos
        s = self.scale
        return (p.x >= c.x - s.x and p.x <= c.x + s.x and
                p.y - 2.5 >= c.y + s.y and p.y - 3.5 <= c.y + s.y and
                p.z >= c.z - s.z and p.z <= c.z + s.z)
    
    def collides(self, player_position):
        p = player_position
        c = self.pos
        s = self.scale
        return (p.x >= c.x - s.x and p.x <= c.x + s.x and
                p.y + 1 >= c.y - s.y and p.y - 2 <= c.y + s.y and
                p.z >= c.z - s.z and p.z <= c.z + s.z)
    
    def update(self):
        if self.move_to:
            self.pos += self.delta_move
            if glm.all(glm.epsilonEqual(self.pos, self.move_to, 0.1)):
                self.move_to = self.start_pos
            if glm.all(glm.epsilonEqual(self.pos, self.start_pos, 0.1)):
                self.move_to = self.end_pos
            self.delta_move = glm.normalize(self.move_to - self.pos) * BLOCKS_SPEED * self.app.delta_time
        super().update()


class SkyBox(BaseModel):
    def __init__(self, app, vao_name='skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.texture = self.app.textures.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)

    def update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))
