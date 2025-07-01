from .boton import *
from .input import *
from .palabra import *
from .recuadro import *
from .texto import *
"""
Módulo UI

Cada uno de los componentes, más o menos (de acuerdo a las necesidades), tienen el mismo patrón:

- crear_*: Es una función que instancia y configura un elemento que se va a renderizar
- wrap_*: Es una función que define cómo se debe renderizar un elemento en particular y devuelve un objeto
    estandarizado con el método "render" y las propiedades "ancho" y "alto" del elemento. Esta función es útil
    para cuando se necesitan pasar varios elementos de diferentes tipos a una función que los renderice en grupo
    y pueda manejar los anchos, altos y separaciones entre elementos.

En el módulo de boton.py se explica mejor cada función y el resto de componentes repiten el comportamiento.
"""
__all__ = ["boton", "input", "palabra", "recuadro", "texto"]