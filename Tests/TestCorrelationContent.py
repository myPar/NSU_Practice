import unittest

import numpy as np
from data.get_attr_data import get_other_attr_keys
from data.global_data import data_set_file_name
from data.global_data import item_count
from data.global_keys import *
from enum import Enum
from data.get_attr_data import get_attributes_data
from statistic.calc_covariation import get_attributes_typical_cart
from statistic.calc_covariation import cov_matrices_names
from statistic.data_supplement import supplement_data_dict
from Tests.tools import is_close

unittest.TestLoader.sortTestMethodsUsing = None
accuracy = 0.00000000000001  # because of double numbers arithmetic there can be calculation accuracy


class Dim(Enum):
    X = 0
    Y = 1


class MatrixType(Enum):
    ALL = 0
    IN = 1
    OUT = 2


# input - attributes list; output - dict of pairs: idx - attribute
def get_attributes_idx_dict(attributes):
    result_dict = dict()
    i = 0
    for attribute in attributes:
        result_dict[i] = attribute
        i += 1
    return result_dict


class TestCorrelation(unittest.TestCase):
    # global data for all tests:
    all_attributes = None  # all attributes list
    output_other_attributes = None  # output attributes + other attributes
    input_other_attributes = None  # input attributes + other attributes
    other_attributes_keys = None  # other attributes
    all_data_dict = None  # all data dict: key - attribute name; value - attribute data
    typical_cart = None  # attributes typical cart

    # init global data:
    @classmethod
    def setUpClass(cls) -> None:
        cls.other_attributes_keys = get_other_attr_keys(data_set_file_name)
        cls.all_attributes = np.concatenate((input_attributes_keys, output_attributes_keys, cls.other_attributes_keys),
                                            axis=0)
        cls.output_other_attributes = np.concatenate((output_attributes_keys, cls.other_attributes_keys), axis=0)
        cls.input_other_attributes = np.concatenate((input_attributes_keys, cls.other_attributes_keys), axis=0)
        cls.all_data_dict = supplement_data_dict(get_attributes_data(data_set_file_name, cls.all_attributes),
                                                 expected_count=item_count)
        cls.typical_cart = get_attributes_typical_cart(cls.all_data_dict, cls.other_attributes_keys)

    @classmethod
    def get_data_by_idx(cls, dim: Dim, m_type: MatrixType, idx: int):
        # 1. get attributes idx dict 2. get attribute name by idx 3. get attribute data by name
        if m_type == MatrixType.ALL:
            attribute_name = get_attributes_idx_dict(cls.all_attributes)[idx]
        elif m_type == MatrixType.IN:
            if dim == Dim.X:
                # input attributes
                attribute_name = get_attributes_idx_dict(input_attributes_keys)[idx]
            elif dim == Dim.Y:
                # output + other attributes
                attribute_name = get_attributes_idx_dict(cls.output_other_attributes)[idx]
                pass
            else:
                assert False
        elif m_type == MatrixType.OUT:
            if dim == Dim.X:
                # output attributes
                attribute_name = get_attributes_idx_dict(output_attributes_keys)[idx]
            elif dim == Dim.Y:
                # input + other attributes
                attribute_name = get_attributes_idx_dict(cls.input_other_attributes)[idx]
            else:
                assert False
        else:
            assert False, "invalid matrix type"
        # get data by attribute name
        data = cls.all_data_dict[attribute_name]
        # item count checking
        assert len(data) == item_count, "invalid item count should be - " + str(item_count)

        # return got data
        return data

    # main check method for each correlation matrix (input - correlation matrix and its type)
    def check(self, correlation_matrix, matrix_type: MatrixType):
        for y in range(len(correlation_matrix)):
            line = correlation_matrix[y]
            for x in range(len(line)):
                data_x = TestCorrelation.get_data_by_idx(Dim.X, matrix_type, x)
                data_y = TestCorrelation.get_data_by_idx(Dim.Y, matrix_type, y)

                actual_coefficient = np.corrcoef(np.concatenate(([data_x], [data_y]), axis=0))[0][1]
                expected_coefficient = correlation_matrix[y][x]

                # check nan with nan case:
                nan_flag1 = np.isnan(actual_coefficient)
                nan_flag2 = np.isnan(expected_coefficient)

                if nan_flag1 or nan_flag2:
                    # both items should be nan values
                    self.assertTrue(nan_flag1 and nan_flag2)
                else:
                    # actual calculated coeff should be equal to expected coefficient in matrix
                    self.assertTrue(is_close(actual_coefficient, expected_coefficient, accuracy))

    def test_all_with_all(self):
        # get all with all correlation matrix
        matrix_name = cov_matrices_names[0]
        correlation_matrix = TestCorrelation.typical_cart[matrix_name]
        self.check(correlation_matrix, MatrixType.ALL)

    def test_all_with_in(self):
        # get all with in correlation matrix
        matrix_name = cov_matrices_names[1]
        correlation_matrix = TestCorrelation.typical_cart[matrix_name]
        self.check(correlation_matrix, MatrixType.IN)

    def test_all_with_out(self):
        # get all with in correlation matrix
        matrix_name = cov_matrices_names[2]
        correlation_matrix = TestCorrelation.typical_cart[matrix_name]
        self.check(correlation_matrix, MatrixType.OUT)


if __name__ == '__main__':
    unittest.main()
