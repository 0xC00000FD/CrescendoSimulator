import vector
from numpy import deg2rad, sin, cos, pi
from time import time

AIR_DENSITY = 1.293 # kg / (m^(-3))

class Ring:
    def __init__(self, dragCoefficient, mass, shooterHeightMeters, shooterLengthMeters, innerDiameterMeters, outerDiameterMeters, thicknessMeters, threadId):
        self.dragCoefficient = dragCoefficient
        self.mass = mass
        self.innerDiameterMeters = innerDiameterMeters
        self.outerDiameterMeters = outerDiameterMeters
        self.thicknessMeters = thicknessMeters
        self.shooterHeightMeters = shooterHeightMeters
        self.shooterLengthMeters = shooterLengthMeters
        self.area = self.getArea()
        
        self.acceleration = vector.obj(x = 0, y = 0)
        self.velocity = vector.obj(x = 0, y = 0)
        self.position = vector.obj(x = 0, y = shooterHeightMeters)
        self.angle = 0
        self.lastTime = 0
        self.closestDistance = 1000000
        self.threadId = threadId
        
    #Provide angle in Radians and ringSpeed in m/s
    def shoot(self, angle, ringSpeed, deltaX):
        self.position = vector.obj(x = -0.1882, y = self.shooterHeightMeters) + vector.obj(rho = self.shooterLengthMeters, phi=angle)
        self.angle = angle
        self.velocity = vector.obj(rho = ringSpeed, phi = angle)
        self.startTime = time()
        self.lastTime = time()
        self.deltaX = deltaX
        self.closestDistance = 1000000
    
    def updateDeltaTime(self): #only holds true and give accurate results for lim deltaTime -> 0
        currTime = time()
        deltaTime = currTime - self.lastTime
                
        drag = - 1 / 2 * self.dragCoefficient * AIR_DENSITY * self.area * self.velocity * self.velocity.rho 
        
        self.velocity += (self.acceleration + drag) / self.mass * deltaTime
        
        self.position += self.velocity * deltaTime
                                        
        self.lastTime = currTime
        
    def update(self, timeStep):
        drag = - 1 / 2 * self.dragCoefficient * AIR_DENSITY * self.area * self.velocity * self.velocity.rho 
        
        self.velocity += (self.acceleration + drag) / self.mass * timeStep
        self.position += self.velocity * timeStep
        
    def checkCollisions(self):
        E = vector.obj(rho = self.outerDiameterMeters, phi = self.angle) # vector E
        A = self.position - E / 2 # vector A
            
        C = vector.obj(x = self.deltaX, y = 0)
        F = vector.obj(rho = 1.9812, phi = deg2rad(90))
        
        (h, g) = self.calculateHG(A, E, C, F)
                
        if 0 <= h and h <= 1 and 0 <= g and g <= 1:
            return 1
        
        C = vector.obj(x = (self.deltaX - 0.4572), y = 2.0828)
        F = vector.obj(rho = 1.0, phi = deg2rad(90))
        
        (h, g) = self.calculateHG(A, E, C, F)
        if h >= -0.01 and 0 <= g and g <= 1:
            return 2
        
        C = vector.obj(x = self.deltaX, y = 1.9812)
        F = vector.obj(x = self.deltaX - 0.4572, y = 2.0828)
        f = F - C
        
        (h, g) = self.calculateHG(A, E, C, f)
        if 0 <= h and h <= 1 and 0 <= g and g <= 1:
            self.closestDistance = min(self.closestDistance, self.calculateClosestDistanceNormalized(A, E, C, F, g))
            if (C - self.position).rho < (F - self.position).rho:
                return -1
            else:
                return -2
        else:
            return 0
        
    def calculateHG(self, A : vector.VectorObject2D, E : vector.VectorObject2D, C : vector.VectorObject2D, F : vector.VectorObject2D):
        P = vector.obj(rho = E.rho, phi = E.phi + pi / 2)
        Q = vector.obj(rho = F.rho, phi = F.phi + pi / 2)
        
        h = ((A - C).dot(P)) / (F.dot(P))
        g = ((C - A).dot(Q)) / (E.dot(Q))
        
        return (h, g)
    
    def calculateClosestDistanceNormalized(self, A : vector.VectorObject2D, E : vector.VectorObject2D, C : vector.VectorObject2D, F : vector.VectorObject2D, g):
        middlePoint : vector.VectorObject2D = (C + F) / 2
        collisionPoint : vector.VectorObject2D = A + E * g
        
        return (middlePoint - collisionPoint).rho
        
    def addForce(self, forceVector):
        self.acceleration += forceVector
        
    def getPosition(self):
        return self.position
    
    def getShooterHeight(self):
        return self.shooterHeightMeters
    
    def getCurrTime(self):
        return time() - self.startTime
    
    def getArea(self):
        return 2 * pi * pi * (self.innerDiameterMeters / 2) * (self.outerDiameterMeters / 2)
    
    def getClosestDistance(self):
        return self.closestDistance
    
    def resetTimer(self):
        self.startTime = time()
        self.lastTime = time()
    
    def getThreadId(self):
        return self.threadId