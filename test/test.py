import sys
import numpy as np
from data.get_attr_data import get_attributes_data
from data.get_attr_data import get_other_attr_keys
from data.global_keys import *

# dict of pairs: key - attribute name; value - attribute's failed status
failed_status_dict = dict()


# failed status description class for the attribute
class FailedStatus(object):
    # initialize with first failed test data
    def __init__(self, attr_name: str):
        self.attribute_name = attr_name
        self.failed_tests = []
        self.exception_messages_dict = dict()

    # print status method
    def print(self):
        print("FAILED STATUS of attribute: '" + self.attribute_name + "'")
        if len(self.failed_tests) == 0:
            # no failed tests
            print("NO")
        else:
            for test in self.failed_tests:
                print("Test '" + test + "' failed:")
                # print failed message for current test
                print(self.exception_messages_dict[test])
        print()

    # add new failed test status for the attribute
    def add_status(self, test_name: str, message: str):
        self.failed_tests.append(test_name)
        self.exception_messages_dict[test_name] = message


# check data items type function
def check_items_types(attr_name, data, expected_type):
    i = 0
    status = "PASSED"
    for item in data:
        if np.dtype(item) != expected_type:
            print("iteration: " + str(i))
            message = "invalid data type '" + str(np.dtype(item)) + "', for item: " + str(item) + "; expected: " + str(expected_type);
            print(message)
            status = "FAILED"
            # add failed status for attribute
            failed_status_dict[attr_name].add_status("CHECK_ITEMS_TYPE", message)
            break
        i += 1
    # return test status
    return status


# check data items type for all attributes
def check_all_data_types(data_dict: dict, expected_type):
    keys = list(data_dict)
    print("CHECK ATTRIBUTES ITEM'S TYPES:")

    for key in keys:
        print("check attribute " + key + ":")
        status = check_items_types(key, data_dict[key], expected_type)
        print(status)
    print("---------------")


# type of item count checking:
# by_max_count - check if data count equal or not to maximum data count
# by_input_count - check if data count equal or not to input data count
check_types = ["BY_MAX_COUNT", "BY_INPUT_COUNT"]


def check_all_data_item_count(data_dict: dict, checking_type: str, expected_items_count: int):
    keys = list(data_dict)

    # check type
    if checking_type == check_types[0]:
        max_count = 0
        # get max data count
        for key in keys:
            cur_items_count = len(data_dict[key])
            # update max count
            if cur_items_count > max_count:
                max_count = cur_items_count
        expected_items_count = max_count
    # check type
    elif checking_type == check_types[1]:
        pass
    # invalid type
    else:
        assert False

    # check counts:
    print("CHECK ATTRIBUTES ITEM'S COUNT:")

    for key in keys:
        print("check attribute: " + key + ":")
        items_count = len(data_dict[key])
        if items_count != expected_items_count:
            message = "items count - " + str(items_count) + "; expected - " + str(expected_items_count)
            print("FAILED: " + "items count - " + message)
            # add failed status for attribute
            failed_status_dict[key].add_status("CHECK_ATTRIBUTES_ITEMS_COUNT", message)
        else:
            print("PASSED")
    print("---------------")


def main():
    input_file_name = "../data/data.txt"
    # other attributes keys
    other_attr_keys = get_other_attr_keys(input_file_name)
    # all attributes names list
    all_attr_names = np.concatenate((input_attributes_keys, output_attributes_keys, other_attr_keys), axis=0)

    # all data dict: key - attr names; value - attr data
    all_data_dict = get_attributes_data(input_file_name, all_attr_names)
    # remove Nan items:
    for key in all_attr_names:
        data = all_data_dict[key]
        all_data_dict[key] = data[~np.isnan(data)]

    # init failed status objects for each attribute
    for key in all_attr_names:
        failed_status_dict[key] = FailedStatus(key)

    # run tests:
    check_all_data_types(all_data_dict, np.float64)
    check_all_data_item_count(all_data_dict, check_types[0], 0)
    # print failed status:
    for key in all_attr_names:
        failed_status_dict[key].print()


if __name__ == "__main__":
    main()
