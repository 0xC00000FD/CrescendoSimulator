import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

f = open("../finalSolutions.txt", "r")

solutionsArray = []
distances = []
speeds = []
angles = []
ratings = []
for line in f:
    nrArray = line.split(",")
    
    if len(nrArray) == 4:
        solutionsArray.append(nrArray)

for solution in solutionsArray:
    distances.append(solution[0])
    ratings.append(solution[1])
    speeds.append(solution[2])
    angles.append(solution[3])

plt.scatter(distances, angles)
plt.show()