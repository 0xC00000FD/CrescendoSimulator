import vector
from ring import Ring
from math import pi, radians
import multiprocessing.pool as pool

def isClose(targetX, ringPosition, tolerance):
    return abs(targetX - ringPosition) < tolerance

def runSimulatorFunction(dragCoefficientStart, dragCoefficientEnd, angle, speed, targetX, threadID):
    mass = 0.253 #kg
    shooterHeightMeters = 0.22363
    shooterLengthMeters = 0.5837
    innerDiameterMeters = 0.254
    outerDiameterMeters = 0.3556
    thicknessMeters = 0.0508

    correctCoef = -100
    
    left = dragCoefficientStart
    right = dragCoefficientEnd

    while left <= right and correctCoef == -100:
        currCoef = (left + right) / 2

        ring1 = Ring(currCoef, mass, shooterHeightMeters, shooterLengthMeters, innerDiameterMeters, outerDiameterMeters, thicknessMeters, threadID)
        ring1.addForce(vector.obj(x = 0.0, y = -9.81 * mass)) #gravitational force
        
        ring1.shoot(angle, speed, 0)
        while ring1.getPosition().y >= 0:                    
            ring1.update(0.0001)

        print(targetX, ring1.getPosition().x, flush=True)
        if isClose(targetX, ring1.getPosition().x, 0.1):
            correctCoef = currCoef
        elif targetX - ring1.getPosition().x > 0:
            right = currCoef
        else:
            left = currCoef
            
        del ring1
        
        
    if correctCoef != -100:
        print(correctCoef, flush = True)


if __name__ == '__main__':
    coeffs = []
    numOfThreads = 10
    maxCoeff = 1
    minCoeff = 0

    #Customize these values based on empirical data
    angle = radians(45)
    speed = 15
    targetX = 6.136970409934492

    for thread in range(numOfThreads):
        endCoeff = (maxCoeff - minCoeff) / numOfThreads * thread + minCoeff
        startCoeff = (maxCoeff - minCoeff) / (numOfThreads + 1) * thread + minCoeff
        
        coeffs.append((startCoeff, endCoeff, angle, speed, targetX, thread))

    print(coeffs)
    threadPool = pool.ThreadPool(numOfThreads)
    result = threadPool.starmap_async(runSimulatorFunction, coeffs)
    result.get()