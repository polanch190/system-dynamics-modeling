"""
Python model "MEM_pysd_Timestep_at1_run1.py"
Translated using PySD version 0.10.0
"""
from __future__ import division
import numpy as np
from pysd import utils
import xarray as xr

from pysd.py_backend.functions import cache
from pysd.py_backend import functions

_subscript_dict = {}

_namespace = {
    'TIME': 'time',
    'Time': 'time',
    'Base Growth Rate': 'base_growth_rate',
    'Base Plant Sed Rate': 'base_plant_sed_rate',
    'Marsh Elevation': 'marsh_elevation',
    'Plant Death': 'plant_death',
    'Plant Death Rate': 'plant_death_rate',
    'Plant Growth': 'plant_growth',
    'Plant Growth Rate': 'plant_growth_rate',
    'Sed Decrease': 'sed_decrease',
    'Sed Increase': 'sed_increase',
    'Spartina': 'spartina',
    'SLR Rate': 'slr_rate',
    'FINAL TIME': 'final_time',
    'INITIAL TIME': 'initial_time',
    'SAVEPER': 'saveper',
    'TIME STEP': 'time_step'
}

__pysd_version__ = "0.10.0"

__data = {'scope': None, 'time': lambda: 0}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


def time():
    return __data['time']()


@cache('run')
def base_growth_rate():
    """
    Real Name: b'Base Growth Rate'
    Original Eqn: b'0.025'
    Units: b'1/Year'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.025


@cache('run')
def base_plant_sed_rate():
    """
    Real Name: b'Base Plant Sed Rate'
    Original Eqn: b'0.025'
    Units: b'1/Year'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.025


@cache('step')
def marsh_elevation():
    """
    Real Name: b'Marsh Elevation'
    Original Eqn: b'INTEG ( Sed Increase-Sed Decrease, 1)'
    Units: b'meters'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_marsh_elevation()


@cache('step')
def plant_death():
    """
    Real Name: b'Plant Death'
    Original Eqn: b'Spartina*Plant Death Rate'
    Units: b'meters/Year'
    Limits: (None, None)
    Type: component

    b''
    """
    return spartina() * plant_death_rate()


@cache('step')
def plant_death_rate():
    """
    Real Name: b'Plant Death Rate'
    Original Eqn: b'IF THEN ELSE(Marsh Elevation < 0.5 :OR: Marsh Elevation > 1.5, Base Growth Rate , 0 \\\\ )'
    Units: b'1/Year'
    Limits: (None, None)
    Type: component

    b'Imagine the plants live for two years and then die.\\t\\t\\t\\t(I am trying to mimic the rabbit population model in the tutorial where \\n    \\t\\tthey call  death rate the Avreage lifespan of rabbit. They said they live \\n    \\t\\tfor 8 years and then die.'
    """
    return functions.if_then_else(marsh_elevation() < 0.5 or marsh_elevation() > 1.5,
                                  base_growth_rate(), 0)


@cache('step')
def plant_growth():
    """
    Real Name: b'Plant Growth'
    Original Eqn: b'Spartina * Plant Growth Rate'
    Units: b'meters/Year'
    Limits: (None, None)
    Type: component

    b''
    """
    return spartina() * plant_growth_rate()


@cache('step')
def plant_growth_rate():
    """
    Real Name: b'Plant Growth Rate'
    Original Eqn: b'IF THEN ELSE(Marsh Elevation > 0.5 :AND: Marsh Elevation < 1.5 , Base Growth Rate , \\\\ 0 )'
    Units: b'1/Year'
    Limits: (None, None)
    Type: component

    b''
    """
    return functions.if_then_else(marsh_elevation() > 0.5 and marsh_elevation() < 1.5,
                                  base_growth_rate(), 0)


@cache('step')
def sed_decrease():
    """
    Real Name: b'Sed Decrease'
    Original Eqn: b'Spartina * Base Plant Sed Rate'
    Units: b'meters/Year'
    Limits: (None, None)
    Type: component

    b''
    """
    return spartina() * base_plant_sed_rate()


@cache('step')
def sed_increase():
    """
    Real Name: b'Sed Increase'
    Original Eqn: b'Spartina * Base Plant Sed Rate - SLR Rate'
    Units: b'meters/Year'
    Limits: (None, None)
    Type: component

    b''
    """
    return spartina() * base_plant_sed_rate() - slr_rate()


@cache('step')
def spartina():
    """
    Real Name: b'Spartina'
    Original Eqn: b'INTEG ( Plant Growth-Plant Death, 2)'
    Units: b'meters'
    Limits: (None, None)
    Type: component

    b''
    """
    return _integ_spartina()


@cache('run')
def slr_rate():
    """
    Real Name: b'SLR Rate'
    Original Eqn: b'0.0032'
    Units: b'meters/Year'
    Limits: (None, None)
    Type: constant

    b''
    """
    return 0.0032


@cache('run')
def final_time():
    """
    Real Name: b'FINAL TIME'
    Original Eqn: b'100'
    Units: b'Year'
    Limits: (None, None)
    Type: constant

    b'The final time for the simulation.'
    """
    return 100


@cache('run')
def initial_time():
    """
    Real Name: b'INITIAL TIME'
    Original Eqn: b'0'
    Units: b'Year'
    Limits: (None, None)
    Type: constant

    b'The initial time for the simulation.'
    """
    return 0


@cache('step')
def saveper():
    """
    Real Name: b'SAVEPER'
    Original Eqn: b'TIME STEP'
    Units: b'Year'
    Limits: (0.0, None)
    Type: component

    b'The frequency with which output is stored.'
    """
    return time_step()


@cache('run')
def time_step():
    """
    Real Name: b'TIME STEP'
    Original Eqn: b'1'
    Units: b'Year'
    Limits: (0.0, None)
    Type: constant

    b'The time step for the simulation.'
    """
    return 1


_integ_marsh_elevation = functions.Integ(lambda: sed_increase() - sed_decrease(), lambda: 1)

_integ_spartina = functions.Integ(lambda: plant_growth() - plant_death(), lambda: 2)
