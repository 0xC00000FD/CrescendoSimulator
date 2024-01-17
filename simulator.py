from ring import Ring
from math import radians, pi
from numpy import arange
import vector
import matplotlib.pyplot as plt
from multiprocessing import Pool, set_start_method

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
        return str.format("{},{},{},({}, {}),{}\n", self.distance, self.speed, self.angle, self.position.x, self.position.y, self.rating)
    
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

    checkCollisions = 0
    
    ring1 = Ring(dragCoefficient, mass, shooterHeightMeters, shooterLengthMeters, innerDiameterMeters, outerDiameterMeters, thicknessMeters, threadID)
    ring1.addForce(vector.obj(x = 0.0, y = -9.81 * mass)) #gravitational force
    
    f = open(str.format("solutionFile{}.txt", threadID), "w")
        
    for distance in arange(minDistance, 7, 0.1):
        for angle in arange(angleStart, angleEnd, - 2 / distance):
            st = 1
            dr = theoreticalMaxSpeed
            
            while st <= dr:
                speed = (st + dr) / 2
                
                ring1.shoot(radians(angle), speed, distance)
                
                ring1.resetTimer()
                while ring1.getPosition().y >= 0:      
                    ring1.update(0.0001)
                                  
                    checkCollisions = ring1.checkCollisions()
                    if checkCollisions != 0:
                        break
                
                print(ring1.getPosition(), angle, distance, speed, checkCollisions, flush=True)
                if checkCollisions == 1 or ring1.getPosition().y < 0:
                    st = speed + 0.5
                elif checkCollisions == 2:
                    dr = speed - 0.05
                elif checkCollisions < 0:
                    solution = Solution(distance, speed, radians(angle), ring1.getPosition(), ring1.getClosestDistance())
                    f.write(solution.getAsString())
                    f.flush()
                    
                    if checkCollisions == -1:
                        st = speed + 0.5
                    elif checkCollisions == -2:
                        dr = speed - 0.05
                        
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
    result = threadPool.starmap_async(runSimulatorFunction, angles)
    result.get()