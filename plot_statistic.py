import plotly.express as px
import pandas as pd


# returns np_array of column/row data by idx
def get_plot_data(file_name: str, d_type: str, key: str):
    try:
        key = int(key)
    except ValueError:
        pass

    df = pd.read_csv(filepath_or_buffer=file_name, sep=' ', header=0)
    # getting file header (column names)
    header = df.columns.to_numpy()

    if d_type == "row":
        return df.loc[key].to_numpy()
    elif d_type == "column":
        if type(key) == int:
            return df[header[key]].to_numpy()
        else:
            return df[key].to_numpy()


# getting input parameters data: columns: AO, AP, AU, AV, AW (names in csv)
# AO - rgmp[Sm3/Sm3] AP - N32[cps] AU - SampleTime[s] AV - DPV[mbar] AW - PL[bara]
def get_input_parameters_data(input_file_name: str):
    # init keys
    keys = ["rgmp[Sm3/Sm3]", "N32[cps]", "SampleTime[s]", "DPV[mbar]", "PL[bara]"]

    result = dict()
    # add data in dict for each key
    for key in keys:
        result[key] = get_plot_data(input_file_name, "column", key)

    return result


# getting output parameters data: columns: WaterPoint, GasPoint, OilPoint
def get_output_parameters_data(input_file_name: str):
    keys = ["GasPointLE[1/m]", "GasPointHE[1/m]",
            "WaterPointLE[1/m]", "WaterPointHE[1/m]",
            "OilPointLE[1/m]", "OilPointHE[1/m]"]
    result = dict()

    # add data in dict for each key
    for key in keys:
        result[key] = get_plot_data(input_file_name, "column", key)

    return result


def main():
    input_file_name = "data.txt"
    input_data = get_input_parameters_data(input_file_name)
    output_data = get_output_parameters_data(input_file_name)

    # print data for debugging
    print(input_data["rgmp[Sm3/Sm3]"])
    print(input_data["N32[cps]"])
    print(input_data["SampleTime[s]"])
    print(input_data["DPV[mbar]"])
    print(input_data["PL[bara]"])
    print()
    print(output_data["GasPointLE[1/m]"])
    print(output_data["GasPointHE[1/m]"])
    print(output_data["WaterPointLE[1/m]"])
    print(output_data["WaterPointHE[1/m]"])
    print(output_data["OilPointLE[1/m]"])
    print(output_data["OilPointHE[1/m]"])


if __name__ == "__main__":
    main()
