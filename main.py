from OpenGL.GL import *
from glfw.GLFW import *
import glm
import numpy as np

from cameras import OrbitCamera
from projections import PerspectiveProjection
from experience import Uniform, Shader, Window
from objects import Cube, Diamond, Frame, Grid

global_vertex_shader_src = '''
#version 330 core

layout (location = 0) in vec3 vin_pos; 
layout (location = 1) in vec3 vin_color; 

out vec4 vout_color;

uniform mat4 MVP;

void main()
{
    // 3D points in homogeneous coordinates
    vec4 p3D_in_hcoord = vec4(vin_pos.xyz, 1.0);

    gl_Position = MVP * p3D_in_hcoord;

    vout_color = vec4(vin_color, 1.);
}
'''

global_fragment_shader_src = '''
#version 330 core

in vec4 vout_color;

out vec4 FragColor;

void main()
{
    FragColor = vout_color;
}
'''

def main():
    # initialize environments
    camera = OrbitCamera(45, 60, 10)
    perspective = PerspectiveProjection(1080, 1080, 45, .1, 50)
    window = Window(1080, 1080, "Project 1", perspective, camera)
    shader = Shader(global_vertex_shader_src, global_fragment_shader_src)

    # initialize objects
    I = glm.mat4()              # identity matrix
    M_cube = glm.mat4()         # initial M matrix of cube
    M_diamond = glm.mat4()      # initial M matrix of diamond
    M_camera_center_diamond = glm.translate(camera.current_center)  # initial M matrix of camera center diamond
    
    frame_world = Frame(I, camera, perspective, shader)
    grid = Grid(I, camera, perspective, shader, 5, 5)
    
    frame_cube = Frame(M_cube, camera, perspective, shader)
    cube = Cube(M_cube, camera, perspective, shader, .3, glm.vec3(0.8, 0.35, 0.35))
    
    frame_diamond = Frame(M_diamond, camera, perspective, shader)
    diamond = Diamond(M_cube, camera, perspective, shader, .3, glm.vec3(0.35, 0.55, 0.8))
    
    camera_center_diamond = Diamond(M_camera_center_diamond, camera, perspective, shader, .1, glm.vec3(0.45, 0.70, 0.45))
    
    prev_t = glfwGetTime()

    # loop until the user closes the window
    while not window.should_close:
        # enable depth test
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        # update polygon mode (GL_FILL or GL_LINE)
        glPolygonMode(GL_FRONT_AND_BACK, window.current_polygon_mode)

        shader.use_program()    # enable shader and uniforms
        
        # update M matrices
        
        # animating
        t = glfwGetTime()
        delta = t - prev_t
        prev_t = t
        th1 = np.radians(t*90)
        th2 = np.radians(t*120)
        
        # rotation
        R_x = glm.rotate(th1, glm.vec3(1,0,0))
        R_y = glm.rotate(th2, glm.vec3(0,1,0))
        
        # circular translation
        T_xz = glm.translate(glm.vec3(2 * np.cos(th1), 0, 2 * np.sin(th1)))
        T_xy = glm.translate(glm.vec3(0, 2 * np.cos(th1), 2 * np.sin(th1)))
        
        # floating
        T_float = glm.translate(glm.vec3(0, .1 * np.sin(t), 0))
        
        # final transformations
        M_cube = T_xz * R_x
        M_diamond = T_xy * T_xz * R_y
        M_camera_center_diamond = glm.translate(camera.current_center) * T_float
        
        camera.update(delta)         # update V matrix

        # apply to objects
        frame_world.update_MVP(I)
        frame_world.draw()
        grid.update_MVP(I)
        if window.grid_enabled: grid.draw()
        
        frame_cube.update_MVP(M_cube)
        frame_cube.draw()
        cube.update_MVP(M_cube)
        cube.draw()
        
        frame_diamond.update_MVP(M_diamond)
        frame_diamond.draw()
        diamond.update_MVP(M_diamond)
        diamond.draw()
        
        camera_center_diamond.update_MVP(M_camera_center_diamond)
        if camera.center_enabled: camera_center_diamond.draw()
        
        window.update()         # update window

    # terminate glfw
    window.terminate()

if __name__ == "__main__":
    main()
