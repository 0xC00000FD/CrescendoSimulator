from ring import Ring
from math import radians, pi
from numpy import arange
from multiprocessing import Pool
import scipy.interpolate as scp
import os
import vector
import matplotlib.pyplot as plt

def closest(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

class Solution:
    def __init__(self, distance, speed, angle, position, rating):
        self.distance = distance
        self.speed = speed
        self.angle = angle
        self.rating = rating
        self.position = position
        
    def getAsString(self):
        return str.format("{:.3f},{:.3f},{:.3f},{:.3f}\n", self.distance, self.rating, self.angle, self.speed)
    
def runSimulatorFunction(angleStart, angleEnd, threadID):
    minDistance = 1.2 # m
    speed = 0 # m / s
    angle = radians(0) # rad
    theoreticalMaxRps = 6784 / 60 # Rotations / s
    wheelRadius = 0.0508 # meters
    theoreticalMaxSpeed = theoreticalMaxRps * 2 * pi * wheelRadius # m / s

    dragCoefficient = 0.2
    mass = 0.253 #kg
    shooterHeightMeters = 0.22363
    shooterLengthMeters = 0.5837
    innerDiameterMeters = 0.254
    outerDiameterMeters = 0.3556
    thicknessMeters = 0.0508

    maxIterations = 20
    tolerance = 0.5

    checkCollisions = 0
    
    ring1 = Ring(dragCoefficient, mass, shooterHeightMeters, shooterLengthMeters, innerDiameterMeters, outerDiameterMeters, thicknessMeters, threadID)
    ring1.addForce(vector.obj(x = 0.0, y = -9.81 * mass)) #gravitational force
    
    f = open(str.format("solutionFile{}.txt", threadID), "w")
        
    for distance in arange(minDistance, 7, 0.1):
        for angle in arange(angleStart, angleEnd, - 2 / distance):
            st = 1
            dr = theoreticalMaxSpeed
            n = 0
            
            while n <= maxIterations and abs(st-dr)/2 >= tolerance:
                speed = (st + dr) / 2
                
                ring1.shoot(radians(angle), speed, distance)
                
                ring1.resetTimer()
                while ring1.getPosition().y >= 0:      
                    ring1.update(0.0001)
                                  
                    checkCollisions = ring1.checkCollisions()
                    if checkCollisions != 0:
                        break
                
                n += 1
                print(ring1.getPosition(), angle, distance, speed, checkCollisions, flush=True)
                if checkCollisions == 1 or ring1.getPosition().y < 0:
                    st = speed
                elif checkCollisions == 2:
                    dr = speed
                elif checkCollisions < 0:
                    solution = Solution(distance, speed, radians(angle), ring1.getPosition(), ring1.getClosestDistance())
                    f.write(solution.getAsString())
                    f.flush()
                    
                    if checkCollisions == -1:
                        st = speed
                    elif checkCollisions == -2:
                        dr = speed
                        
if __name__ == '__main__':
    angles = []
    numOfThreads = 10
    
    minAngle = 20
    maxAngle = 65
    
    for thread in range(numOfThreads):
        startAngle = (maxAngle - minAngle) / numOfThreads * thread + minAngle
        endAngle = (maxAngle - minAngle) / (numOfThreads + 1) * thread + minAngle
        
        angles.append((startAngle, endAngle, thread))

    threadPool = Pool(numOfThreads)
    
    try:
        threadPool.starmap(runSimulatorFunction, angles)
    except KeyboardInterrupt:
        threadPool.terminate()
    
    allSolutions = []
    for file in os.listdir():
        if file.startswith("solutionFile"):
            f = open(file)
            
            for line in f.readlines():
                allSolutions.append(tuple(float(x) for x in line.split(",")))
                
            os.remove(file)
    
    allSolutions.sort(reverse = True)
    
    allSolutionsCulled = {solution[0]: solution for solution in allSolutions}
    
    allSolutions = list(allSolutionsCulled.values())
    allSolutions.sort()
    
    xAxisMeters = list(solution[0] for solution in allSolutions)
    yAxisRads = list(solution[3] for solution in allSolutions)
    yAxisMetersPerSec = list(solution[2] for solution in allSolutions)
    
    print(xAxisMeters, yAxisRads, yAxisMetersPerSec)
    
    splineAnglePerDistance = scp.KroghInterpolator(xAxisMeters, yAxisRads)
    splineSpeedPerDistance = scp.KroghInterpolator(xAxisMeters, yAxisMetersPerSec)
    
    with open("./finalSolutions.txt", "w") as solutionFile:
        solutionFile.write(str.format("Interpolated distance to angle equation coefficients: {}\n", splineAnglePerDistance.c))
        solutionFile.write(str.format("Interpolated distance to speed equation coefficients: {}\n\n", splineSpeedPerDistance.c))
        
        for solution in allSolutions:
            solutionString = str.format("{:.3f} {:.3f} {:.3f} {:.3f}\n", solution[0], solution[1], solution[2], solution[3])
            solutionFile.write(solutionString)