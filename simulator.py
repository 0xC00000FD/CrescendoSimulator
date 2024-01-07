from ring import Ring
from math import radians, pi
import vector
import matplotlib.pyplot as plt

def closest(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

minDistance = 1 # m
speed = 0 # m / s
angle = radians(0) # rad
theoreticalMaxRps = 6784 / 60 # Rotations / s
wheelRadius = 0.0508 # meters
theoreticalMaxSpeed = theoreticalMaxRps * 2 * pi * wheelRadius # m / s

ring1 = Ring(0.12, 0.253, 1, 0.254, 0.3556, 0.0508)
ring1.addForce(vector.obj(x = 0.0, y = -9.81)) #gravitational force

class Solution:
    def __init__(self, distance, speed, angle, rating):
        self.distance = distance
        self.speed = speed
        self.angle = angle
        self.rating = rating
        
solutions = []

checkCollisions = 0
for distance in range(minDistance, 4, 1):
    for angle in range(75, 0, -1):
        st = 1
        dr = theoreticalMaxSpeed
        
        while st <= dr:
            speed = (st + dr) / 2
            
            ring1.shoot(radians(angle), speed, distance)
            
            while ring1.getPosition().y >= 0:                    
                checkCollisions = ring1.checkCollisions()
                if checkCollisions > 0:
                    break
                
                ring1.update()
                        
            if checkCollisions == 1 or ring1.getPosition().y < 0:
                st = speed + 0.5
            elif checkCollisions == 2:
                dr = speed - 0.05
            else:
                if checkCollisions == -1:
                    solutions.append(Solution(distance, speed, radians(angle), ring1.getClosestDistance))
                    st = speed + 0.5
                else:
                    solutions.append(Solution(distance, speed, radians(angle), ring1.getClosestDistance))
                    dr = speed - 0.05

print(solutions)