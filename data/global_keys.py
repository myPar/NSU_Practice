# init input attributes keys (columns: AO, AP, AU, AV, AW (names in csv))
input_attributes_keys = ["rgmp[Sm3/Sm3]", "N32[cps]",
                         "SampleTime[s]", "DPV[mbar]",
                         "PL[bara]"]
# init output attributes keys (columns: WaterPoint, GasPoint, OilPoint. With low energy and high energy levels)
output_attributes_keys = ["GasPointLE[1/m]", "GasPointHE[1/m]",
                          "WaterPointLE[1/m]", "WaterPointHE[1/m]",
                          "OilPointLE[1/m]", "OilPointHE[1/m]"]
# string data keys (Date, Time)
string_data_keys = ["Date", "Time"]
