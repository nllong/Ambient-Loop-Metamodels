# Ambient Loop Metamodels

[![Build Status](https://travis-ci.org/nllong/ambient-loop-metamodels.svg?branch=develop)](https://travis-ci.org/nllong/ambient-loop-metamodels) [![Documentation Status](https://readthedocs.org/projects/ambient-loop-metamodels/badge/?version=latest)](https://ambient-loop-metamodels.readthedocs.io/en/latest/?badge=latest)
  
The ambient loop metamodels use the Metamodeling Framework to generate black box models that can be loaded offline to evaluate various response variables (e.g. outlet water temperature, total heating electricity, total district heating energy, etc.). Prior to this repository existing, the metamodels were developed and stored along side the Framework; however, the Framework is now designed to be included as a dependency and run in context of other Python scripts. 

## Using the Models

### Creating and Processing Simulations Files

The first thing to do is to create a parametric analysis of the desired building energy model. This is typically done using OpenStudio's PAT Application.

If using PAT, then the download_bem_results.py can be used to save the results and post process the results in preparation for the metamodeling.

* Update the ID and PAT server information in the `download_bem_results.py` file
* Run the script to download the data from OpenStudio Server

```bash
python download_bem_results.py
```

* Downselect the variables of interest from the `all_json_variables.json` and save as a new file `selected_json_variables.json`.
* Update the simulation directory name in the `process_data.py` file
* Run the postprocessing script

```bash
python process_data.py
``` 

### Creating New Metamodels

The first requirement is to update the model_definitions for the new metamodel. The model definitions contain the data required to generate the data model including the parameters of each of the requested metamodel. The model_definitions folder contains some entries that can be copied, pasted, then updated as needed.

```bash
metamodel.py inspect -f model_definitions/all_metamodels.json -a smoff_test -m RandomForest
metamodel.py build -f model_definitions/all_metamodels.json -a smoff_test -m RandomForest
metamodel.py evaluate -f model_definitions/all_metamodels.json -a smoff_test -m RandomForest

# or for a specific model 
metamodel.py inspect -f model_definitions/all_metamodels.json -a smoff_sweep_v2 -m RandomForest -d 0.005
metamodel.py build -f model_definitions/all_metamodels.json -a smoff_sweep_v2 -m RandomForest -d 0.005
metamodel.py evaluate -f model_definitions/all_metamodels.json -a smoff_sweep_v2 -m RandomForest -d 0.005
metamodel.py validate -f model_definitions/all_metamodels.json -a smoff_sweep_v2 -m RandomForest -d 0.005
```

### Using Existing Metamodels

The metamodels are too large to share using Github, therefore, the user must download the models and place them into the right director(y|ies) to leverage this library.

There is a set of example metamodes that can be used to run the Generate CSVs script (defined below), you must download and install these models into the correct. To do this run the following in the root of this repository:

```bash
# mac / linux
./download_test_metamodels.sh .

# windows -- run the command in gitbash or cygwin (easiest)
./download_test_metamodels.sh .
```

#### Generate Metamodel Result CSVs

Make sure to run the script above to download and extract the existing metamodels. The example `generate_csvs.py` script loads the office and retail metamodels to generate a 3 dimensions sweep (inlet temperature, hour of day, response variable) and saves CSV files to be loaded into Modelica.

### Saving New Metamodels

To be documented

### Citation

Please reference this project using the following:

Long, N., Almajed, F., von Rhein, J., & Henze, G. (2021). Development of a metamodelling framework for building energy models with application to fifth-generation district heating and cooling networks. Journal of Building Performance Simulation, 14(2), 203–225. https://doi.org/10.1080/19401493.2021.1884291


## To Do

* Provide method to share metamodels by uploading and downloading to a shared S3 account (assuming permissions)
* Locate the metamodel.json files and the models together
