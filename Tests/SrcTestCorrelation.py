import unittest
import numpy as np
from data.global_keys import *
from data.get_attr_data import get_other_attr_keys
from data.global_data import *

step = 5
all_file_name = "../Tests/tests_src/all_attributes"
in_file_name = "../Tests/tests_src/in_attributes"
out_file_name = "../Tests/tests_src/out_attributes"

in_test_size = 2
out_test_size = 1


class SrcTestCorrelation(unittest.TestCase):
    # global data for tests
    all_attributes = None  # all attributes names
    other_attributes_keys = None
    output_other_attributes = None  # output attributes + other attributes
    input_other_attributes = None  # input attributes + other attributes

    # init global data:
    @classmethod
    def setUpClass(cls) -> None:
        cls.other_attributes_keys = get_other_attr_keys(data_set_file_name)
        cls.all_attributes = np.concatenate((input_attributes_keys, output_attributes_keys,
                                             cls.other_attributes_keys), axis=0)

        cls.output_other_attributes = np.concatenate((output_attributes_keys, cls.other_attributes_keys), axis=0)
        cls.input_other_attributes = np.concatenate((input_attributes_keys, cls.other_attributes_keys), axis=0)

        file_all = open(all_file_name, 'w')
        file_in = open(in_file_name, 'w')
        file_out = open(out_file_name, 'w')

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

    def test_all(self):
        self.assertEqual(1, 1)
