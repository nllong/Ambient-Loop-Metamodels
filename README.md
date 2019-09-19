# Ambient Loop Metamodels

|build| |docs|

The ambient loop metamodels use the Metamodeling Framework (soon to be renamed Metamodeling Framework) to generate black box models that can be loaded offline to evaluate various response variables (e.g. outlet water temperature, total heating electricity, total district heating energy, etc.).Prior to this repository existing, the metamodels were developed and stored along side the Framework; however, the Framework is now designed to be included as a dependency and run in context of other Python scripts. 

## Using the Models

### Creating New Metamodels


### Using Existing Metamodels

The metamodels are too large to share using Github, therefore, the user must download the models and place them into the right director(y|ies) to leverage this library.

There is a set of example metamodes that can be used to run the Generate CSVs script (defined below), you must download and install these models into the correct. To do this run the following in the root of this repository:

```bash
# mac / linux
./download_test_metamodels.sh .

# windows -- run the command in gitbash or cygwin (easiest)
./download_test_metamodels.sh .
```

#### Generate CSVs

Make sure to run the script above to download and extract the existing metamodels. The example `generate_csvs.py` script loads the office and retail metamodels to generate a 3 dimensions sweep (inlet temperature, hour of day, response variable) and saves CSV files to be loaded into Modelica.

### Saving New Metamodels

To be documented

## To Do

* Provide method to share metamodels by uploading and downloading to a shared S3 account (assuming permissions)
* Locate the metamodel.json files and the models together


.. |build| image:: https://travis-ci.org/nllong/metamodeling-framework.svg?branch=develop
    :target: https://travis-ci.org/nllong/metamodeling-framework

.. |docs| image:: https://readthedocs.org/projects/metamodeling-framework/badge/?version=latest
	:target: https://metamodeling-framework.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status