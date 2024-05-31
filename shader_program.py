import os.path


class ShaderProgram:
    def __init__(self, ctx, path):
        self.ctx = ctx
        self.path = os.path.join(path, 'shaders')
        self.programs = {}
        self.programs['default'] = self.get_program('default')
        self.programs['skybox'] = self.get_program('skybox')
        self.programs['text'] = self.get_program('text')

    def get_program(self, shader_program_name):
        with open(os.path.join(self.path, f'{shader_program_name}.vert')) as file:
            vertex_shader = file.read()
        with open(os.path.join(self.path, f'{shader_program_name}.frag')) as file:
            fragment_shader = file.read()
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def destroy(self):
        [program.release() for program in self.programs.values()]
