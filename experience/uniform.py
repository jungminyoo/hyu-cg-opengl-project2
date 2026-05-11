from typing import Generic, TypeVar

from .shader import Shader

UniformType = TypeVar('UniformType')

class Uniform(Generic[UniformType]):
    '''class for single uniform in single shader program'''
    
    def __init__(self, name: str, init_data: UniformType, shader: Shader):
        self._name = name
        self._data = init_data
        self._location = shader.get_uniform_location(name)

    @property
    def name(self): return self._name

    @property
    def data(self): return self._data
    @data.setter
    def data(self, new_data: UniformType): self._data = new_data

    @property
    def location(self): return self._location