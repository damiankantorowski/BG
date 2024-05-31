#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

uniform sampler2D u_texture_0;

void main() {
    float gamma = 2.2;
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = pow(color, vec3(gamma));
    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1.0);
}
