import pandas as pd
import numpy as np
import Statistic
import sys

# init input attributes keys
input_attributes_keys = ["rgmp[Sm3/Sm3]", "N32[cps]",
                         "SampleTime[s]", "DPV[mbar]",
                         "PL[bara]"]
# init output attributes keys
output_attributes_keys = ["GasPointLE[1/m]", "GasPointHE[1/m]",
                          "WaterPointLE[1/m]", "WaterPointHE[1/m]",
                          "OilPointLE[1/m]", "OilPointHE[1/m]"]
# other attributes keys (init in runtime)
other_attributes_keys = []


def get_other_attr_keys(file_name: str):
    df = pd.read_csv(filepath_or_buffer=file_name, sep=' ', header=0)
    # getting file header (column names)
    header = df.columns.to_numpy()
    # make set from header keys to get O(1) asymptotic of searching keys
    key_set = set(header)

    # remove input attributes keys
    for in_key in input_attributes_keys:
        try:
            key_set.remove(in_key)
        except KeyError:
            print("Fatal: no such in key in data header: " + in_key, file=sys.stderr)
    # remove output  attributes keys
    for out_key in output_attributes_keys:
        try:
            key_set.remove(out_key)
        except KeyError:
            print("Fatal: no such out key in data header: " + out_key, file=sys.stderr)
    return np.array(list(key_set))


# returns np_array of column/row data by idx
def get_plot_data(file_name: str, d_type: str, key: str):
    try:
        key = int(key)
    except ValueError:
        pass

    df = pd.read_csv(filepath_or_buffer=file_name, sep=' ', header=0)
    # getting file header (column names)
    header = df.columns.to_numpy()

    if d_type == "row":
        return df.loc[key].to_numpy()
    elif d_type == "column":
        if type(key) == int:
            return df[header[key]].to_numpy()
        else:
            return df[key].to_numpy()


# getting input attributes data: columns: AO, AP, AU, AV, AW (names in csv)
# AO - rgmp[Sm3/Sm3] AP - N32[cps] AU - SampleTime[s] AV - DPV[mbar] AW - PL[bara]
def get_input_attr_data(input_file_name: str):
    result = dict()
    # add data in dict for each key
    for key in input_attributes_keys:
        result[key] = get_plot_data(input_file_name, "column", key)

    return result


# getting output parameters data: columns: WaterPoint, GasPoint, OilPoint
def get_output_attr_data(input_file_name: str):
    result = dict()

    # add data in dict for each key
    for key in output_attributes_keys:
        result[key] = get_plot_data(input_file_name, "column", key)

    return result


# getting other attributes data (not input and not output attributes)
def get_other_attr_data(input_file_name: str):
    result = dict()

    # add data in dict for each key
    for key in other_attributes_keys:
        result[key] = get_plot_data(input_file_name, "column", key)

    return result


def main():
    input_file_name = "data.txt"

    # get input attributes data
    input_attr_data = get_input_attr_data(input_file_name)
    # get output attributes data
    output_attr_data = get_output_attr_data(input_file_name)

    # get other attributes keys
    global other_attributes_keys
    other_attributes_keys = get_other_attr_keys(input_file_name)
    # get other attributes data
    other_attr_data = get_other_attr_data(input_file_name)

    gas_le_statistic = Statistic.DataStatistic(output_attr_data["GasPointLE[1/m]"], "GasPointLE[1/m]")
    gas_le_statistic.print_statistic()


if __name__ == "__main__":
    main()
