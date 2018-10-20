__author__ = "Vili Hätönen"

import os
import thor

name = "speed_data_2.txt"
data_str = ""

with open(name, "r") as file:
    data_str = file.read()

data = data_str.split("*** NEW DATA SET ***\n")
data = data[1:]

print("should be list type now", type(data))
print("data length", len(data))
print("data table length ", len(data[0]))

model = thor.ragnarok(data)

model_name = "model_1.thor"
with open(model_name, "w" ) as file:
    file.write(str(model))
