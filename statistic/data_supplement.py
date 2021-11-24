import numpy as np


# supplement data after Nan items removing


# simple supplement: add average values to the end
def supplement_data(data, expected_count: int):
    assert expected_count >= len(data)
    # remove nan items
    data = data[~np.isnan(data)]
    cleared_data_size = len(data)

    for i in range(expected_count - cleared_data_size):
        data = np.append(data, np.mean(data))
    if len(data) != expected_count:
        assert False
    # return result data
    return data


def supplement_data_dict(data_dict: dict, expected_count: int):
    attributes = data_dict.keys()

    for attribute in attributes:
        data = data_dict[attribute]
        data = supplement_data(data, expected_count)
        data_dict[attribute] = data
    # return supplement data dict
    return data_dict
