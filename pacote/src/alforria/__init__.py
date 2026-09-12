"""Pacote Alforria"""

__version__ = "0.3.4"


from .dominio.grupo import Grupo
from .dominio.professor import Professor
from .dominio.turma import Turma

__all__ = ["Grupo", "Professor", "Turma", "__version__"]
