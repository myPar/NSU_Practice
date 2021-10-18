import numpy as np
# import global keys
from data.global_keys import *

# covariation matrices names
cov_matrices_names = ["all_with_all", "all_with_in", "all_with_out"]


# get covaration matrices (input_data_dict - dict of pairs: key - attribute name, value - attribute data)
def get_attributes_typical_cart(input_data_dict: dict, other_attributes_keys) -> dict:
    # order data: 1. input attr data 2. output attr data 3. other attr data
    data_dict = dict()
    # for input attr
    for in_key in input_attributes_keys:
        data_dict[in_key] = input_data_dict[in_key]
    # for output attr
    for out_key in output_attributes_keys:
        data_dict[out_key] = input_data_dict[out_key]
    # for other attributes
    for key in other_attributes_keys:
        data_dict[key] = input_data_dict[key]
    # get key-list in insertion order
    keys = list(data_dict)

    # construct data: 2d array
    data = [data_dict[keys[0]]]
    for i in range(len(keys) - 1):
        # concatenate data arrays by x axis
        data = np.concatenate((data, [data_dict[keys[i + 1]]]), axis=0)

    # calc covariation matrix (all with all)
    cov_matrix_all = np.corrcoef(data)

    count_in = len(input_attributes_keys)       # input attr count
    count_out = len(output_attributes_keys)     # output attr count
    count_all = len(input_data_dict)            # all attributes count

    # get from "all" cov-matrix "all with in" cov matrix:
    delete_indices_row = np.arrange(count_in)                   # row indices to delete
    delete_indices_column = np.arrange(count_in, count_all)     # column indices to delete

    # delete input attr rows
    cov_matrix_all_in = np.delete(cov_matrix_all, delete_indices_row, 0)
    # delete not input attributes column
    cov_matrix_all_in = np.delete(cov_matrix_all_in, delete_indices_column, 1)

    # get from "all" cov-matrix "all with out" cov matrix:
    delete_indices_row = np.arange(count_in, count_in + count_out)
    delete_indices_column = np.concatenate((np.arange(count_in), np.arrange(count_out, count_all)), 0)
    # delete output attr rows
    cov_matrix_all_out = np.delete(cov_matrix_all, delete_indices_row, 0)
    # delete not output columns
    cov_matrix_all_out = np.delete(cov_matrix_all_out, delete_indices_column, 1)

    # return result as a dict of cov matrices:
    result = dict()
    result[cov_matrices_names[0]] = cov_matrix_all
    result[cov_matrices_names[1]] = cov_matrix_all_in
    result[cov_matrices_names[2]] = cov_matrix_all_out

    return result
