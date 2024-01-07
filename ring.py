import vector
from math import sin, cos, pi
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
    def shoot(self, angle, ringSpeed):
        self.position = vector.obj(x = 0, y = 0, z = 0)
        self.angle = angle
        self.velocity = vector.obj(rho = ringSpeed, phi = angle)
        self.startTime = time()
        self.lastTime = time()
    
    def update(self):
        currTime = time()
        deltaTime = currTime - self.lastTime;
        
        self.position += self.velocity * deltaTime
        
        drag = - 1 / 2 * self.dragCoefficient * AIR_DENSITY * self.getArea() * self.velocity * self.velocity.rho
        
        self.velocity += (self.acceleration + drag) * deltaTime
                                
        self.lastTime = currTime
        
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