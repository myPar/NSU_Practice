import numpy as np
from plot_statistic import input_attributes_keys
from plot_statistic import output_attributes_keys

# covariation matrices names
cov_matrices_names = ["all_with_all", "all_with_in", "all_with_out"]


# get covaration matrices (data - dict of pairs: key - attribute name, value - attribute data)
def get_attributes_typical_cart(input_data_dict: dict, name_idx_dict: dict) -> dict:
    # order data: 1. input attr data 2. output attr data 3. other attr data
    data_dict = dict()
    # for input attr
    for key in input_attributes_keys:
        data_dict[key] = input_data_dict[key]
    # for output attr
    for key in output_attributes_keys:
        data_dict[key] = input_data_dict[key]
    # TODO: get other attributes data
    # get key-list in insertion order
    keys = list(data_dict)

    # construct data: 2d array
    data = np.array([[]])
    for key in keys:
        data = np.concatenate((data, data_dict[key]), axis=0)

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
