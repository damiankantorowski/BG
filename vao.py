from vbo import VBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, app):
        self.ctx = app.ctx
        self.vbo = VBO(app.ctx)
        self.program = ShaderProgram(app.ctx, app.path)
        self.vaos = {}
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cube'])
        self.vaos['skybox'] = self.get_vao(
            program=self.program.programs['skybox'],
            vbo=self.vbo.vbos['skybox'])
        self.vaos['text'] = self.get_vao(
            program=self.program.programs['text'],
            vbo=self.vbo.vbos['text'])

    def get_vao(self, program, vbo):
        return self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()