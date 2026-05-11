from abc import ABC, abstractmethod
import glm

from experience import Uniform, Shader
from projections import Projection
from cameras import Camera

class Object(ABC):
    """
    abstract class for various objects\n
    to use objects, shader must at least contain following codes\n
    .. code:: glsl
        #version 330 core

        layout (location = 0) in vec3 vin_pos;
        uniform mat4 MVP;

        void main() {
            vec4 p3D_in_hcoord = vec4(vin_pos.xyz, 1.0);
            gl_Position = MVP * p3D_in_hcoord;
        }
    """ 
    
    def __init__(self, init_V: glm.mat4x4, camera: Camera, projection: Projection, shader: Shader):
        super().__init__()
        
        self._camera = camera
        self._projection = projection
        self._MVP = Uniform[glm.mat4x4]("MVP", self._projection.P.matrix * self._camera.V.matrix * init_V, shader)
    
    @abstractmethod
    def _prepare_vao(self) -> int | list[int]: pass
    
    @abstractmethod
    def draw(self): pass
    
    def update_MVP(self, new_M: glm.mat4x4):
        self._MVP.data = self._projection.P.matrix * self._camera.V.matrix * new_M
    
    @property
    @abstractmethod
    def VAO(self): pass