from OpenGL.GL import *
import glm
import numpy as np

from .object import Object
from experience import Shader
from projections import Projection
from cameras import Camera

class Grid(Object):
    '''class for grid on xz plane'''
    
    def __init__(self, init_V: glm.mat4x4, camera: Camera, projection: Projection, shader: Shader, grid_half_width: int, grid_half_depth: int):
        super().__init__(init_V, camera, projection, shader)
        
        self._VAO = self._prepare_vao()
        self._grid_half_width = grid_half_width
        self._grid_half_depth = grid_half_depth

    def _prepare_vao(self) -> int | list[int]:
        # prepare vertex data (in main memory)
        vertices = glm.array(glm.float32,
            # position        # color
            0.0, 0.0, -0.5,  0.5, 0.5, 0.5, # line start
            0.0, 0.0, 0.5,   0.5, 0.5, 0.5, # line end
        )

        # create and activate VAO (vertex array object)
        VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
        glBindVertexArray(VAO)      # activate VAO

        # create and activate VBO (vertex buffer object)
        VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
        glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

        # copy vertex data to VBO
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy vertex data to the currently bound vertex buffer

        # configure vertex positions
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
        glEnableVertexAttribArray(0)

        # configure vertex colors
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
        glEnableVertexAttribArray(1)

        return VAO

    def draw(self):
        glBindVertexArray(self.VAO)
        
        for i in range(-self._grid_half_width, self._grid_half_width + 1):
            MVP_line = self._MVP.data \
                        * glm.translate(glm.vec3(i, 0, 0)) \
                        * glm.scale(glm.vec3(self._grid_half_depth * 2))
            glUniformMatrix4fv(self._MVP.location, 1, GL_FALSE, glm.value_ptr(MVP_line))
            glDrawArrays(GL_LINES, 0, 2)
        
        for i in range(-self._grid_half_depth, self._grid_half_depth + 1):
            MVP_line = self._MVP.data \
                        * glm.translate(glm.vec3(0, 0, i)) \
                        * glm.scale(glm.vec3(self._grid_half_width * 2)) \
                        * glm.rotate(np.pi * 0.5, glm.vec3(0, 1, 0))
            glUniformMatrix4fv(self._MVP.location, 1, GL_FALSE, glm.value_ptr(MVP_line))
            glDrawArrays(GL_LINES, 0, 2)

    @property
    def VAO(self): return self._VAO