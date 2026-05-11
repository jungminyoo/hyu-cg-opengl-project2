from OpenGL.GL import *
import glm

from .object import Object
from experience import Shader
from projections import Projection
from cameras import Camera

class Diamond(Object):
    '''class for single diamond object'''
    
    def __init__(self, init_V: glm.mat4x4, camera: Camera, projection: Projection, shader: Shader, half_extent: float, color: glm.vec3):
        super().__init__(init_V, camera, projection, shader)
        
        self._half_extent = half_extent
        self._color = color
        self._VAO = self._prepare_vao()
    
    def _prepare_vao(self) -> int | list[int]: 
        # prepare vertex data (in main memory)
        # 36 vertices for 12 triangles
        vertices = glm.array(glm.float32,
            # position                                                          color
            -self._half_extent, 0,                      self._half_extent,      self._color.x, self._color.y, self._color.z,
            self._half_extent,  0,                      self._half_extent,      self._color.x, self._color.y, self._color.z,
            0,                  self._half_extent * 2,  0,                      self._color.x, self._color.y, self._color.z,
                        
            self._half_extent,  0,                      self._half_extent,      self._color.x, self._color.y, self._color.z,
            self._half_extent,  0,                      -self._half_extent,     self._color.x, self._color.y, self._color.z,
            0,                  self._half_extent * 2,  0,                      self._color.x, self._color.y, self._color.z,
                        
            self._half_extent,  0,                      -self._half_extent,     self._color.x, self._color.y, self._color.z,
            -self._half_extent, 0,                      -self._half_extent,     self._color.x, self._color.y, self._color.z,
            0,                  self._half_extent * 2,  0,                      self._color.x, self._color.y, self._color.z,
                        
            -self._half_extent, 0,                      -self._half_extent,     self._color.x, self._color.y, self._color.z,
            -self._half_extent, 0,                      self._half_extent,      self._color.x, self._color.y, self._color.z,
            0,                  self._half_extent * 2,  0,                      self._color.x, self._color.y, self._color.z,
                        
            -self._half_extent, 0,                      self._half_extent,      self._color.x, self._color.y, self._color.z,
            self._half_extent,  0,                      self._half_extent,      self._color.x, self._color.y, self._color.z,
            0,                  -self._half_extent * 2, 0,                      self._color.x, self._color.y, self._color.z,
                        
            self._half_extent,  0,                      self._half_extent,      self._color.x, self._color.y, self._color.z,
            self._half_extent,  0,                      -self._half_extent,     self._color.x, self._color.y, self._color.z,
            0,                  -self._half_extent * 2, 0,                      self._color.x, self._color.y, self._color.z,
                        
            self._half_extent,  0,                      -self._half_extent,     self._color.x, self._color.y, self._color.z,
            -self._half_extent, 0,                      -self._half_extent,     self._color.x, self._color.y, self._color.z,
            0,                  -self._half_extent * 2, 0,                      self._color.x, self._color.y, self._color.z,
                        
            -self._half_extent, 0,                      -self._half_extent,     self._color.x, self._color.y, self._color.z,
            -self._half_extent, 0,                      self._half_extent,      self._color.x, self._color.y, self._color.z,
            0,                  -self._half_extent * 2, 0,                      self._color.x, self._color.y, self._color.z,
                        
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
        glUniformMatrix4fv(self._MVP.location, 1, GL_FALSE, glm.value_ptr(self._MVP.data))
        glDrawArrays(GL_TRIANGLES, 0, 24)
    
    @property
    def VAO(self): return self._VAO