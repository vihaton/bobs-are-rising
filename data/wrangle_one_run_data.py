__author__ = "Vili Hätönen"

import os
import thor
import ast


names = ["speed_data_maze1.txt", "speed_data_maze2.txt", "speed_data_forest.txt", "speed_data_box.txt"]
data_str = ""

for i in range(len(names)):
	name = names[i]
	with open(name, "r") as file:
		data_str = file.read()

	data = data_str.split("*** NEW DATA SET ***\n")
	data = data[1:] #remove the first empty piece
	for j in range(len(data)):
		data[j] = ast.literal_eval(data[j])

	print("some debug printing")
	print("should be list type now", type(data))
	print("data length", len(data))
	print("data table length ", len(data[0]))
	print("data table table length ", len(data[0][0]), data[0][0])

	model = data[0] #model is the recorded run

	model_name = "model_" + str(i) + ".thor"
	print(model_name)
	with open(model_name, "w" ) as file:
		file.write(str(model))

print("wrote models ", names)
