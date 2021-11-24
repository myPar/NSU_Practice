import unittest

from data.get_attr_data import *
from statistic.data_supplement import supplement_data_dict
from data.global_data import *

input_file_name = data_set_file_name
expected_item_count = item_count


def get_test_data() -> dict:
    # other attributes keys
    other_attr_keys = get_other_attr_keys(input_file_name)
    # all attributes names list
    all_attr_names = np.concatenate((input_attributes_keys, output_attributes_keys, other_attr_keys), axis=0)

    # all data dict: key - attr names; value - attr data
    all_data_dict = get_attributes_data(input_file_name, all_attr_names)

    # remove Nan items and replace it by specified value
    all_data_dict = supplement_data_dict(all_data_dict, expected_item_count)

    return all_data_dict


def get_attributes_names():
    input_file = open(input_file_name, 'r')
    key_set = set(input_file.readline().replace("\n", "").split(" "))
    input_file.close()

    # remove string data keys
    for str_data_key in string_data_keys:
        try:
            key_set.remove(str_data_key)
        except KeyError:
            assert False, "Fatal: no such string key in data header"

    return np.array(list(key_set))


def get_attribute_data(attribute_name: str):
    df = pd.read_csv(filepath_or_buffer=input_file_name, sep=' ', header=0)
    # getting file header (column names)
    header = df.columns.to_numpy()

    if not (attribute_name in header):
        assert False, "Fatal: no such attribute - " + attribute_name + " in data header"

    result = supplement_data_dict(dict({attribute_name: df[attribute_name].to_numpy()}), expected_item_count)[attribute_name]

    # return supplemented data
    return result


class CheckAttributesContent(unittest.TestCase):
    # init global data for all tests
    attributes_names = None
    testData = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.testData = get_test_data()
        cls.attributes_names = get_attributes_names()

    # check equality of expected data and actual data for all attributes
    def test_attributes_data(self):
        for attribute_name in CheckAttributesContent.attributes_names:
            with self.subTest(name=attribute_name):
                expected_data = get_attribute_data(attribute_name)
                test_data = CheckAttributesContent.testData[attribute_name]

                for i in range(len(expected_data)):
                    self.assertEqual(expected_data[i], test_data[i])

