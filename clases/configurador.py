import os
from enum import Enum
from typing import Annotated
from modulos.func_auxiliares import error
from pydantic import BaseModel, FilePath, Field, ValidationError, model_validator

class supportedAlg(str, Enum):
    GEN = 'evolutivo_generacional'
    EST = 'evolutivo_estacionario'

class supportedCruce(str, Enum):
    MOC = 'MOC'
    OX2 = 'OX2'

class ConfigModel(BaseModel):
    # Definimos todos los campos del fichero de configuración aquí
    data: list[FilePath] = Field(alias='DATA')
    alg: list[supportedAlg] = Field(alias='ALG')
    seed: list[Annotated[int, Field(ge=10000000, le=99999999)]] = Field(alias='SEED')
    k: list[Annotated[int, Field(gt=0)]] = Field(alias='K')
    prcAleatorio: list[Annotated[int, Field(ge=0, le=100)]] = Field(alias='PRC_ALEATORIO')
    tampoblacion: list[Annotated[int, Field(gt=0)]] = Field(alias='TAMPOBLACION')
    numElites: list[Annotated[int, Field(ge=0)]] = Field(default=[None], alias='NUM_ELITES')
    numPadres: list[Annotated[int, Field(gt=0)]] = Field(default=[None], alias='NUM_PADRES')
    kBest: list[Annotated[int, Field(gt=0)]] = Field(alias='KBEST')
    prcCruce: list[Annotated[int, Field(ge=0, le=100)]] = Field(default=[None], alias='PRC_CRUCE')
    cruce: list[supportedCruce] = Field(alias='CRUCE')
    prcMutacion: list[Annotated[int, Field(ge=0, le=100)]] = Field(alias='PRC_MUTACION')
    kWorst: list[Annotated[int, Field(gt=0)]] = Field(alias='KWORST')
    maxEvaluaciones: list[Annotated[int, Field(gt=0)]] = Field(alias='MAX_EVALUACIONES')
    maxSegundos: list[Annotated[int, Field(gt=0)]] = Field(alias='MAX_SEGUNDOS')

    @model_validator(mode='after')
    def comprobaciones_post(self):
        """
        Comprueba que numElites 
        """
        if supportedAlg.GEN in self.alg and (None in self.numElites or None in self.prcCruce):
                raise ValueError("El parámetro NUM_ELITES y PRC_CRUCE es obligatorio para el algoritmo evolutivo_generacional.")
        if supportedAlg.EST in self.alg and None in self.numPadres:
            raise ValueError("El parámetro NUM_PADRES es obligatorio para el algoritmo evolutivo_estacionario.")

        return self

class Configurador(ConfigModel):
    def __init__(self, ruta: str):
        """
        Crea una instancia de Configurador a partir de un fichero de configuración.
        """
        try:
            config_dict = {}
            with open(ruta, 'r') as archivo:
                for linea in archivo:
                    partes = linea.strip().split()
                    if len(partes) < 3 or partes[1] != '=':
                        continue

                    campo, valores = partes[0], partes[2:]
                    config_dict[campo] = valores

            super().__init__(**config_dict) # Le pasamos los datos para que los valide e inicie

        except ValidationError as e:
            # Si Pydantic encuentra un error (campo faltante, tipo incorrecto, valor fuera de rango),
            # lo notificamos y salimos.
            error(f"Error en el fichero de configuración:\n{e}")
            exit(1)
        except FileNotFoundError:
            error(f"El archivo de configuración '{ruta}' no fue encontrado.")
            exit(1)

    def mostrarInfo(self):
        print(' CONFIGURACIÓN APLICADA: '.center(100, 'X'))
        
        for field_name, field_info in ConfigModel.model_fields.items():
            value = getattr(self, field_name) # Devuelve el valor del atributo dado por el field_name

            display_value = [item.value if isinstance(item, Enum) else item for item in value] # Guardamos los valores y si es un Enum, tenemos que hacer .value
            print(f'  {field_info.alias or field_name}: {display_value}')
