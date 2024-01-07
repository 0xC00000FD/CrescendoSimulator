import vector
from math import sin, cos, pi, radians
from time import time

AIR_DENSITY = 1.293 # kg / (m^(-3))

class Ring:
    def __init__(self, dragCoefficient, mass, shooterHeightMeters, innerDiameterMeters, outerDiameterMeters, thicknessMeters):
        self.dragCoefficient = dragCoefficient
        self.mass = mass
        self.innerDiameterMeters = innerDiameterMeters
        self.outerDiameterMeters = outerDiameterMeters
        self.thicknessMeters = thicknessMeters
        self.shooterHeightMeters = shooterHeightMeters
        
        self.acceleration = vector.obj(x = 0, y = 0)
        self.velocity = vector.obj(x = 0, y = 0)
        self.position = vector.obj(x = 0, y = shooterHeightMeters)
        self.angle = 0
        self.lastTime = 0
        
    #Provide angle in Radians and ringSpeed in m/s
    def shoot(self, angle, ringSpeed, deltaX):
        self.position = vector.obj(x = 0, y = 0, z = 0)
        self.angle = angle
        self.velocity = vector.obj(rho = ringSpeed, phi = angle)
        self.startTime = time()
        self.lastTime = time()
        self.deltaX = deltaX
    
    def update(self):
        currTime = time()
        deltaTime = currTime - self.lastTime;
        
        self.position += self.velocity * deltaTime
        
        drag = - 1 / 2 * self.dragCoefficient * AIR_DENSITY * self.getArea() * self.velocity * self.velocity.rho 
        
        self.velocity += (self.acceleration + drag) / self.mass * deltaTime
                                
        self.lastTime = currTime
        
    def checkCollisions(self):
        E = vector.obj(rho = self.outerDiameterMeters, phi = self.angle) # vector E
        A = self.position - E / 2 # vector A
            
        C = vector.obj(x = self.deltaX, y = 0)
        F =  vector.obj(rho = 1.9812, phi = radians(90))
        
        (h, g) = self.calculateHG(A, E, C, F)
                
        if 0 <= h and h <= 1 and 0 <= g and g <= 1:
            return True
        
        C =  vector.obj(x = self.deltaX - 0.4572, y = 2.0828)
        F =  vector.obj(rho = 500, phi = radians(90))
        
        (h, g) = self.calculateHG(A, E, C, F)
        
        if 0 <= h and h <= 1 and 0 <= g and g <= 1:
            return True
        
        return False
        
    def calculateHG(self, A : vector.VectorObject2D, E : vector.VectorObject2D, C : vector.VectorObject2D, F : vector.VectorObject2D):
        P = vector.obj(rho = E.rho, phi = E.phi + pi / 2)
        Q = vector.obj(rho = F.rho, phi = F.phi + pi / 2)
        
        h = ((A - C).dot(P)) / (F.dot(P))
        g = ((C - A).dot(Q)) / (E.dot(Q))
        
        return (h, g)
        
    def addForce(self, forceVector):
        self.acceleration += forceVector
        
    def getPosition(self):
        return self.position
    
    def getShooterHeight(self):
        return self.shooterHeightMeters
    
    def getCurrTime(self):
        return time() - self.startTime;
    
    def getArea(self):
        return 4 * pi * pi * (self.innerDiameterMeters / 2) * (self.outerDiameterMeters / 2)