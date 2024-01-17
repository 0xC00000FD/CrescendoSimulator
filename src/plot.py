import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

f = open("solutionsFile.txt", "r")

solutionsArray = []
distances = []
speeds = []
angles = []
ratings = []
for line in f:
    nrArray = line.split(",")
    
    solutionsArray.append(nrArray)
    
solutionsArray.sort(key = lambda solution: solution[3], reverse=True)
dict1 = {solution[0]: solution for solution in solutionsArray}

solutionsArray = list(dict1.values())

for solution in solutionsArray:
    distances.append(solution[0])
    speeds.append(solution[1])
    angles.append(solution[2])
    ratings.append(solution[3])

plt.scatter(distances, angles)
plt.show()