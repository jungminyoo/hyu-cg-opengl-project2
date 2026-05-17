from OpenGL.GL import *
from glfw.GLFW import *
import glm
import numpy as np

from cameras import OrbitCamera
from projections import PerspectiveProjection
from experience import Window, Light, Node
from objects import Cube, Diamond, Frame, Grid

def main():
    # initialize environments
    camera = OrbitCamera(45, 60, 10)
    perspective = PerspectiveProjection(1080, 1080, 45, .1, 50)
    window = Window(1080, 1080, "Project 2", perspective, camera)
    light = Light(glm.vec3(5, 5, 5), glm.vec3(1, 1, 1))

    # initialize nodes
    I = glm.mat4()              # identity matrix
    base = Node(None, I)
    node_cube = Node(base, I)
    node_diamond = Node(node_cube, I)
    
    node_camera_center_diamond = Node(None, I)
    node_camera_center_diamond.set_transform(glm.translate(camera.current_center))
    
    base.update_tree_global_transform()
    node_camera_center_diamond.update_tree_global_transform()
    
    # initialize objects
    
    grid = Grid(camera, perspective, base, 5, 5)
    frame_world = Frame(camera, perspective, base)
    cube = Cube(glm.vec3(0.8, 0.35, 0.35), camera, perspective, light, node_cube, .3)
    diamond = Diamond(glm.vec3(0.35, 0.55, 0.8), camera, perspective, light, node_diamond, .3)
    
    camera_center_diamond = Diamond(glm.vec3(0.45, 0.70, 0.45), camera, perspective, light, node_camera_center_diamond, .1)
    
    prev_t = glfwGetTime()

    # loop until the user closes the window
    while not window.should_close:
        # enable depth test
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        # update polygon mode (GL_FILL or GL_LINE)
        glPolygonMode(GL_FRONT_AND_BACK, window.current_polygon_mode)

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
        M_diamond = T_xy * R_y
        M_camera_center_diamond = glm.translate(camera.current_center) * T_float
        
        camera.update(delta)         # update V matrix

        # apply to objects
        # frame_world.update_MVP(I)
        # frame_world.draw()
        # grid.update_MVP(I)
        # if window.grid_enabled: grid.draw()
        
        # frame_cube.update_MVP(M_cube)
        # frame_cube.draw()
        node_cube.set_transform(M_cube)
        node_diamond.set_transform(M_diamond)
        node_camera_center_diamond.set_transform(M_camera_center_diamond)
        
        base.update_tree_global_transform()
        node_camera_center_diamond.update_tree_global_transform()

        frame_world.draw()
        grid.draw()
        cube.draw()
        diamond.draw()
        camera_center_diamond.draw()
        
        # frame_diamond.update_MVP(M_diamond)
        # frame_diamond.draw()
        # diamond.update_MVP(M_diamond)
        # diamond.draw()
        
        # camera_center_diamond.update_MVP(M_camera_center_diamond)
        # if camera.center_enabled: camera_center_diamond.draw()
        
        window.update()         # update window

    # terminate glfw
    window.terminate()

if __name__ == "__main__":
    main()
