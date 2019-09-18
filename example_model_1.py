# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example analysis script demonstrating how to programatically load and run already persisted
reduced order models. This example loads two response variables (models) from the small office
random forest reduced order models. The loaded models are then passed through the
sweep-temp-test.json analysis definition file. The analysis definition has a few fixed
covariates and a few covariates with multiple values to run.

.. code-block:: bash

    python analysis_ex1.py

.. moduleauthor:: Nicholas Long (nicholas.l.long@colorado.edu, nicholas.lee.long@gmail.com)
"""

# Add the parent directory to the path so the metamodel and analysis definitiona libraries
# can be found.
import sys

sys.path.append("..")  # Adds higher directory to python modules path.

from metamodeling.metamodels import Metamodels
from metamodeling.analysis_definition.analysis_definition import AnalysisDefinition

# Load in the models for analysis
metamodel = Metamodels('./smoff/metamodels.json')
metamodel.set_analysis('smoff_sweep_v2')

# Load the exising models
if metamodel.models_exist(
        'RandomForest',
        models_to_load=['HeatingElectricity', 'DistrictHeatingHotWaterEnergy'],
        root_path='smoff'):
    metamodel.load_models(
        'RandomForest',
        models_to_load=['HeatingElectricity', 'DistrictHeatingHotWaterEnergy'],
        root_path='smoff')
else:
    raise Exception('ROMs do not exist')

# Load in the analysis definition
analysis = AnalysisDefinition('sweep-temp-test.json')

# convert the analysis definition to a dataframe for use in the metamodel
data = analysis.as_dataframe()
data = metamodel.yhats(data, 'RF', ['HeatingElectricity', 'DistrictHeatingHotWaterEnergy'])

# view all the data
print(data)

# describe the data
print(data.describe())

# view a couple single rows
print(data.iloc[0])
print(data.iloc[7])
