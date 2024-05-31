#version 330
uniform sampler2D surface;

out vec4 fragColor;
in vec2 uv;

void main() {
    fragColor = texture(surface, uv);
}