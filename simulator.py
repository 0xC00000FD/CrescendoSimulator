from ring import Ring
from math import radians
import vector
import matplotlib.pyplot as plt

def closest(lst, K):
     return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

distance = 1 # m
speed = 25 #m / s
angle = radians(75) # rad

ring1 = Ring(0.12, 0.253, 1, 0.254, 0.3556, 0.0508)
ring1.shoot(angle, speed, distance)
ring1.addForce(vector.obj(x = 0.0, y = -9.81))

ringHeights = []
ringXPos = []

while ring1.getPosition().y >= 0 and not ring1.checkCollisions():    
    ringHeights.append(ring1.getPosition().y)
    ringXPos.append(ring1.getPosition().x)
        
    ring1.update()
    
print(max(ringHeights))

ringHeights[ringXPos.index(closest(ringXPos, distance))] = 1.9812

plt.scatter(ringXPos, ringHeights)
plt.show()

