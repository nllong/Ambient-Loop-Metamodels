import glob
import json
import os
import time

import pandas as pd

# Set the download name to the file that you want to process
#DOWNLOAD_NAME = "smoff_sweep_v2"
DOWNLOAD_NAME = "smoff_test"
base_dir = os.path.join(os.path.dirname(__file__), "simulations", DOWNLOAD_NAME)
json_variable_file = os.path.join(base_dir, 'selected_json_variables.json')

if not os.path.exists(base_dir):
    raise Exception(f"Path does not exist to process {base_dir}")

if not os.path.exists(json_variable_file):
    raise Exception(f"Path does not exist for selected_json_variables.json in {base_dir}")


def return_value(metadatum, json_results):
    """Return the value of a multilevel dictionary. Should use jsonpath-ng"""
    if metadatum["level_2"]:
        return json_results[metadatum["level_1"]][metadatum["level_2"]]
    elif metadatum["level_1"]:
        return json_results[metadatum["level_1"]]
    else:
        return ""


def process_directory(dir, json_variable_file, index_length):
    """ Process the JSON files that exist in the directory"""
    with open(json_variable_file) as f:
        vars_metadata = json.load(f)

        new_data = {}

        for var in vars_metadata:
            if os.path.exists(os.path.join(dir, var["file"])):
                # Put empty rename to at end
                metadata = sorted(
                    var["data"], key=lambda k: (k['order'], k['rename_to'] or "z", k['level_1'], k['level_2'])
                )

                # Now load the result json file (var["file"])
                with open(os.path.join(dir, var["file"])) as f2:
                    json_results = json.load(f2)

                    # save the updated data
                    for metadatum in metadata:
                        if metadatum["rename_to"]:
                            new_data[metadatum["rename_to"]] = [return_value(metadatum, json_results)]
                        elif metadatum["level_2"]:
                            new_data[f"{metadatum['level_1']}.{metadatum['level_2']}"] = [
                                return_value(metadatum, json_results)]
                        else:
                            new_data[metadatum['level_1']] = [return_value(metadatum, json_results)]

        # expand each of the records to the index_length. Do that here and not in dataframes
        # because it is much much much faster
        for k, _v in new_data.items():
            new_data[k] = new_data[k] * index_length

        return new_data


files = glob.glob(f"{base_dir}/*/*.csv")
for index, csv_file in enumerate(files):
    dir = os.path.dirname(csv_file)
    start = time.time()

    print(f"Processing directory: {dir}")
    if os.path.exists(os.path.join(dir, 'processed.csv')):
        print(f"  directory has already been processed, skipping")
        continue

    # add the JSON data to the time series data. Each row gets the same data as it qualifies the simulation
    df = pd.read_csv(csv_file)
    print(f"  finished reading results csv in {time.time() - start} seconds")

    start = time.time()
    # Determine the ETS inlet temperature
    # By default use the district heating hot water as the default. When there is no heating and cooling, the
    # district cooling temp is the same as the district heating temp.
    df['total_district_energy'] = df['District Cooling Chilled Water Energy'] + df['District Heating Hot Water Energy']
    df['ETSInletTemperature'] = df['District Heating Outlet Temperature']
    filter_1 = df['District Cooling Chilled Water Energy'] > 0
    filter_1_zero = df['District Cooling Chilled Water Energy'] == 0
    filter_2 = df['District Heating Hot Water Energy'] > 0
    filter_2_zero = df['District Heating Hot Water Energy'] == 0
    df.loc[filter_1 & filter_2_zero, 'ETSInletTemperature'] = df['District Cooling Outlet Temperature']
    df.loc[filter_1_zero & filter_2, 'ETSInletTemperature'] = df['District Heating Outlet Temperature']
    # The most complicated is when heating and cooling occurs during the same hour. Weight the ETS inlet temp as
    # a function of the energy used for heating/cooling
    tmp = df[filter_1 & filter_2]
    df.loc[filter_1 & filter_2, 'ETSInletTemperature'] = \
        tmp['District Cooling Chilled Water Energy'] / tmp['total_district_energy'] * tmp['District Cooling Outlet Temperature'] + \
        tmp['District Heating Hot Water Energy'] / tmp['total_district_energy'] * tmp['District Heating Outlet Temperature']

    json_results = process_directory(dir, json_variable_file, len(df.index))
    print(f"  finished processing JSON in {time.time() - start} seconds")

    # load new data and fill down the data to the same number of rows in the CSV file
    start = time.time()
    df2 = pd.DataFrame(json_results)
    print(f"  finished creating JSON-based dataframe in {time.time() - start} seconds")
    # df2 = pd.concat([df2] * len(df.index), ignore_index=True)
    # print(f"  finished extending JSON-based dataframe in {time.time() - start} seconds")

    # append the columns
    start = time.time()
    df = pd.concat([df, df2], axis=1)
    print(f"  finished concatenating JSON-based dataframe in {time.time() - start} seconds")

    # write out the result data to the directory. This may be slower (slightly) but allows
    # for restarting the postprocessing as needed.
    df.columns = df.columns.str.replace(' ', '')

    # rename a couple of columns to be more usefully named
    df.rename(
        columns={
            'DistrictHeatingInletTemperature': 'ETSHeatingOutletTemperature',
            'DistrictCoolingInletTemperature': 'ETSCoolingOutletTemperature',
        },
        inplace=True)
    # make sure to drop a column as well
    df.to_csv(os.path.join(dir, 'processed.csv'), index=False)

# aggregate as text files which will be must faster than dataframes
# process all of the directories and store one large CSV file
lines = None
header = None
files = glob.glob(f"{base_dir}/*/processed.csv")
for index, csv_file in enumerate(files):
    start = time.time()

    print(f"Aggregating file: {csv_file}")
    if index == 0:
        with open(csv_file, 'r') as file:
            lines = file.readlines()
            header = lines.pop(0)
    # elif index > 3:
    #     break
    else:
        with open(csv_file, 'r') as file:
            new_lines = file.readlines()
            new_header = new_lines.pop(0)
            if new_header != header:
                print(f"Uh oh, columns don't match, skipping dataframe. {header} <> {new_header}")
            else:
                lines += new_lines

    print(f"  finished combining results in {time.time() - start} seconds")
    # df.to_csv(os.path.join(dir, 'data.out'), index=False)
    # if index >= 2:
    #     break

# go through all the column names are remove any spaces - this reads the last dataframe, df, processed in the loop.
print(f"Saving simulation_results file")
start = time.time()
simulation_results_file = os.path.join(base_dir, 'simulation_results.csv')
with open(simulation_results_file, 'w') as file:
    file.write(header)
    for line in lines:
        file.write(line)
print(f"  finished aggregating results in {time.time() - start} seconds")
# main_df.to_csv(simulation_results_file, index=False)

# if there is a desire to see runtime performance of measures, then look at this gist:
#    https://gist.github.com/nllong/d17836137bc5d90b7783e1403a38e867
