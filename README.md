# Ring Shooting Simulator  
This ring shooting simulator models the trajectory of a ring shot with given initial conditions (initial velocity, angle) and models drag and the gravitational force.

## Files:
- [Ring Class](https://github.com/0xC00000FD/CrescendoSimulator/blob/master/ring.py)
- [Main simulator file](https://github.com/0xC00000FD/CrescendoSimulator/blob/master/simulator.py)
- [Plotting tool for data verification](https://github.com/0xC00000FD/CrescendoSimulator/blob/master/plot.py)
- [Empirically finding drag coefficient](https://github.com/0xC00000FD/CrescendoSimulator/blob/master/findDragCoeff.py)

## ReadMe Contents:
1. [How to install and run](#how-to-run)
2. [Ring class](#ring-class)
3. [Simulator optimization](#simulator-optimization)
4. [How to empirically find drag coefficient](#how-to-empirically-find-drag-coefficient)


## How to install and run:
To install, simply download the file as a zip and extract all the files into the same folder.

You will first need to install the python interpreter from [the main python downloads page](https://www.python.org/downloads/).

This project depends on a couple of modules that you will have to install before being able to run the files:
1. numpy and vector for the main simulation
2. matplotlib for plotting the values  
  
To install these packages simply run the following command:
```
python -m pip install -r requirements.txt
```
or
```
python3 -m pip install -r requirements.txt
```

There are 3 files you can run (simulator.py, plot.py, findDragCoeff.py), each with their own purpose. To run them use the ```python [fileName].py``` command in the terminal.

WIP: This project is a work in progress and as such the values for the simulation can only be changed through editing the files. More features will be added later on.

## Ring Class:

### Description:
This class contains all attributes and methods necessary to simulate the ring, as well as its position, velocity and acceleration (sum of forces divided by mass). There are two primary simulation methods:

1. updateDeltaTime() - simulates the movement in real-time, useful for visualizing how the trajectory would look in real life.

2. update(timeStep) - uses the given timeStep to update location and velocity, useful for precise simulation of the trajectory


### Collision System:
The collision system is made purely using vectors, as this made it very easy to integrate with the already vectorial model of the simulation. The concept is simple:

Consider a vector A that describes the starting point of a line, and a vector E that describes the line itself (A is needed because vectors have their origin point at (0, 0)). The equation A + E describes the first line segment. 

For the ring, E is the vector (rho = outerDiameter / 2, phi = ringAngle) in polar coordinate form and A = centerLocation - E / 2.

Consider another pair of vectors, C and F, for any line that we want to detect a collision with. C is the starting point vector, and F describes the actual line.

To get the collisin points for the two pairs of vectors, we can consider the following equation:

    A + E * g = C + F * h

G and H are unknown real numbers and in this case are coefficients used to shorten/extend the two lines E and F. We are checking if, by extending or retracting E and F by any real number value, we get a collision. Thus, for values of both h and g in the range [0, 1] it means that both E and F do not have to be extended to reach the collision point. As such, the two are considered to be intersecting.

To solve this equation, we can just get two vectors perpendicular to E and F, let's call them P and Q, and do the dot product of the equation with both of those vectors as they will cancel out either E or F.

Getting the perpendicular vectors is simple as we are using polar coordinates and we can simply do the following:
```
P = vector.obj(rho = E.rho, phi = E.phi + pi / 2)
Q = vector.obj(rho = F.rho, phi = F.phi + pi / 2)
```
where phi is the angle of the vector and rho is the magnitude.

Thus, the values for h and g are: (the dot method describes the dot product)

```
h = ((A - C).dot(P)) / (F.dot(P))
g = ((C - A).dot(Q)) / (E.dot(Q))
```

We can tweak the conditions of the detection system to simulate different obstacles, like extending a wall infinitely in one direction by not checking if it is between [0, 1] but only if h >= 0 (or h <= 1, depending on the direction of F and the direction you wish to infintely extend the wall in).

The collision system gives different values depending on which wall was hit, and we will see why in the next section about simulation optimization.

## Simulator Optimization:
WIP

## How to empirically find the drag coefficient
WIP