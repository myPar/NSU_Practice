import unittest
import numpy as np
from data.global_keys import *
from data.get_attr_data import get_other_attr_keys
from data.global_data import *
from data.get_attr_data import get_attributes_data
from statistic.data_supplement import supplement_data_dict
from Tests.tools import is_close

step = 5
all_attributes_file_name = "../Tests/tests_src/all_attributes"
in_attributes_file_name = "../Tests/tests_src/in_attributes"
out_attributes_file_name = "../Tests/tests_src/out_attributes"

all_test_data_file_name = "../Tests/tests_src/all_coefficients"
in_test_data_file_name = "../Tests/tests_src/in_coefficients"
out_test_data_file_name = "../Tests/tests_src/out_coefficients"

in_test_size = 2
out_test_size = 1

accuracy = 0.000001


def get_test_data(file_name):
    value = 0.0
    file = open(file_name, 'r')
    str_list = file.readline().replace("\n", "").split(" ")
    test_data = np.array([])

    for item in str_list:
        if item == "nan":
            test_data = np.append(test_data, np.nan)
        else:
            try:
                value = float(item)
                test_data = np.append(test_data, value)
            except ValueError:
                assert False, item + " should be a float value"
    file.close()
    # return result numpy array
    return test_data


class SrcTestCorrelation(unittest.TestCase):
    # global data for tests
    all_attributes = None  # all attributes names
    other_attributes_keys = None
    output_other_attributes = None  # output attributes + other attributes
    input_other_attributes = None  # input attributes + other attributes
    all_data_dict = None

    # init global data:
    @classmethod
    def setUpClass(cls) -> None:
        cls.other_attributes_keys = get_other_attr_keys(data_set_file_name)
        cls.all_attributes = np.concatenate((input_attributes_keys, output_attributes_keys,
                                             cls.other_attributes_keys), axis=0)

        cls.output_other_attributes = np.concatenate((output_attributes_keys, cls.other_attributes_keys), axis=0)
        cls.input_other_attributes = np.concatenate((input_attributes_keys, cls.other_attributes_keys), axis=0)
        cls.all_data_dict = supplement_data_dict(get_attributes_data(data_set_file_name, cls.all_attributes),
                                                 expected_count=item_count)

        file_all = open(all_attributes_file_name, 'w')
        file_in = open(in_attributes_file_name, 'w')
        file_out = open(out_attributes_file_name, 'w')

        # init test data:
        i = 0

        while i in range(len(cls.all_attributes)):  # all with all
            attribute1 = cls.all_attributes[i]
            attribute2 = cls.all_attributes[i + 1]

            file_all.write(attribute1 + " " + attribute2 + "\n")
            i += step
        file_all.close()

        i = 0
        while i in range(len(input_attributes_keys)):  # all with in
            for j in range(in_test_size):
                attribute1 = input_attributes_keys[i]
                attribute2 = cls.output_other_attributes[j * step]

                file_in.write(attribute1 + " " + attribute2 + "\n")
            i += 1
        file_in.close()

        i = 0
        while i in range(len(output_attributes_keys)):  # all with out
            for j in range(out_test_size):
                attribute1 = output_attributes_keys[i]
                attribute2 = cls.input_other_attributes[(j + 1) * step]

                file_out.write(attribute1 + " " + attribute2 + "\n")
            i += 1
        file_out.close()

    @classmethod
    def get_correlation_coefficient(cls, attribute1: str, attribute2: str):
        attributes = cls.all_data_dict.keys()
        assert attribute1 in attributes and attribute2 in attributes, "no such keys in dict"
        data1 = cls.all_data_dict[attribute1]
        data2 = cls.all_data_dict[attribute2]
        # get correlation coefficient between data1 and data2
        actual_coefficient = np.corrcoef(np.concatenate(([data1], [data2]), axis=0))[0][1]

        return actual_coefficient

    def check(self, attributes_file_name: str, test_data_file_name: str):
        test_data = get_test_data(test_data_file_name)

        input_file = open(attributes_file_name, 'r')
        i = 0

        for line in input_file:
            split_line = line.replace("\n", "").split(" ")
            assert len(split_line) == 2

            attribute1 = split_line[0]
            attribute2 = split_line[1]
            expected_coefficient = test_data[i]
            actual_coefficient = SrcTestCorrelation.get_correlation_coefficient(attribute1, attribute2)

            # actual coefficient should be close to expected
            nan_flag1 = np.isnan(actual_coefficient)
            nan_flag2 = np.isnan(expected_coefficient)

            if nan_flag1 or nan_flag2:
                self.assertTrue(nan_flag1 and nan_flag2)
            else:
                self.assertTrue(is_close(expected_coefficient, actual_coefficient, accuracy))

            i += 1
        input_file.close()

    def test_all(self):
        self.check(all_attributes_file_name, all_test_data_file_name)

    def test_in(self):
        self.check(in_attributes_file_name, in_test_data_file_name)

    def test_out(self):
        self.check(out_attributes_file_name, out_test_data_file_name)
