__author__ = "Vili Hätönen"

import os
import thor
import ast


name = "speed_data_test.txt"
data_str = ""

with open(name, "r") as file:
    data_str = file.read()

data = data_str.split("*** NEW DATA SET ***\n")
data = data[1:] #remove the first empty piece
for i in range(len(data)):
    data[i] = ast.literal_eval(data[i])

#print ("data 0", data[0][:10], "data 1",  data[1][:10])

print("some debug printing")
print("should be list type now", type(data))
print("data length", len(data))
print("data table length ", len(data[0]))
print("data table table length ", len(data[0][0]), data[0][0])


model = thor.ragnarok(data)

model_name = "model_1.thor"
with open(model_name, "w" ) as file:
    file.write(str(model))
