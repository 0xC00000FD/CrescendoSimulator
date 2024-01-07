from ring import Ring
from math import radians
import vector
import matplotlib.pyplot as plt

ring1 = Ring(0.12, 0.253, 1, 0.254, 0.3556, 0.0508)
ring1.shoot(radians(45), 15)
ring1.addForce(vector.obj(x = 0.0, y = -9.81))

ringPosition = []
timeStamps = []

while ring1.getPosition().y >= 0:    
    ringPosition.append(ring1.getPosition().y)
    timeStamps.append(ring1.getPosition().x)
    
    ring1.update()
    
print(max(ringPosition))
plt.scatter(timeStamps, ringPosition)
plt.show()