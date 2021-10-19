import numpy as np
import pandas as pd


class DataStatistic(object):
    # statistic init method: gets np_array data and returns Statistic object for it
    def __init__(self, data, name: str):
        # remove Nan items
        cleared_data = data[~np.isnan(data)]
        self.value_count = np.size(data)    # value count
        self.average = np.mean(cleared_data)        # average value
        self.median = np.median(cleared_data)       # median
        self.quantile_first = np.quantile(cleared_data, 0.25)   # quantile of level 0.25
        self.quantile_third = np.quantile(cleared_data, 0.75)   # quantile of level 0.75
        self.cardinality = len(np.unique(cleared_data))         # cardinality - count of unique values
        self.min = np.min(cleared_data)     # min value
        self.max = np.max(cleared_data)     # max value
        self.skip_count = get_skip_count(data)  # count of empty values
        self.skip_percent = 100 * float(self.skip_count) / self.value_count   # percent of empty values
        self.name = name

    def print_statistic(self):
        print(self.name + " statistic parameters: ")

        # iterate over object attributes and print their values
        for attr, value in self.__dict__.items():
            if attr != 'name':
                print(attr + " : " + str(value))


# count Nan elements
def get_skip_count(data):
    count = 0
    for item in data:
        if pd.isna(item):
            count += 1

    return count
