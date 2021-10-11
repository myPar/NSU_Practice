import numpy as np
from plot_statistic import input_attributes_keys
from plot_statistic import output_attributes_keys


# get covaration matrices (data - dict of pairs: key-attribute name value-attribute data)
# name_idx_dict - dict of pairs: attribute name - idx in data array
def get_attributes_typical_cart(input_data_dict: dict, name_idx_dict: dict):
    # order data: 1. input attr data 2. output attr data
    data_dict = dict()
    # for input attr
    for key in input_attributes_keys:
        data_dict[key] = input_attributes_keys[key]
    # for output attr
    for key in output_attributes_keys:
        data_dict[key] = input_attributes_keys[key]

    # get key-list in insertion order
    keys = list(data_dict)
    # construct data: 2d array
    data = np.array([])
    for key in keys:
        data = np.concatenate((data, data_dict[key]), axis=0)
    # calc covariation matrix (all with all)
    cov_matrix_all = np.corrcoef(data)
    # get from "all" cov-matrix "all with in" cov matrix
    input_attr_count = len(input_attributes_keys)
    # delete input attr rows
    for i in range(input_attr_count):
        cov_matrix_all_in = cov_matrix_all
