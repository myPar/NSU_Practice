import pandas as pd
import numpy as np
import sys
# import global keys
from data.global_keys import*


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
            exit(1)
    # remove output attributes keys
    for out_key in output_attributes_keys:
        try:
            key_set.remove(out_key)
        except KeyError:
            print("Fatal: no such out key in data header: " + out_key, file=sys.stderr)
            exit(1)
    # remove string data keys
    for str_data_key in string_data_keys:
        try:
            key_set.remove(str_data_key)
        except KeyError:
            print("Fatal: no such string data key in data header: " + str_data_key, file=sys.stderr)
            exit(1)

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


# gets attributes data, specified in keys list
def get_attributes_data(input_file_name: str, keys):
    result = dict()

    # add data in dict for each key
    for key in keys:
        result[key] = get_plot_data(input_file_name, "column", key)
    # return the result as the dictionary of pairs: key - attr name; value - attr data
    return result
