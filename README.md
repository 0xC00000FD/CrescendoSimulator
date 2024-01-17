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

To get the collision points for the two pairs of vectors, we can consider the following equation:

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
For the simulation, I went less with a mathematical approach to optimization and did more software-based optimizations.

One of the first optimizations was splitting the task of simulating to multiple processes/instances (not threads) of the python interpreter. Thus, every process checks only a small sub-range of angles, for every distance between the declared min-distance and the given max-distance. (room for optimization here, some angles do not have solutions beyond/below a certain distance)

The second optimization was that for a fixed angle and distance, decreasing the launch speed would result in a lower maximum trajectory height and distance, and increasing the speed would do the opposite. Thus, for values between 0 and a theoretical max speed (maximum speed of the wheels, in meters per second), using the different collision codes for each wall (lower wall, upper wall, or 0 for the ground) we can do a binary search type of operation to find the correct solutions for the problem. If it is to hit the ground or the lower wall, we know the speed has to be higher, and if it is to hit the upper infinite wall we know the speed must be lower.

The simulator also accounts for which edge of the opening is closer to the ring when it a solution is found, and always goes increases/decreases the speed in the direction of the center of the opening.

Being closer to the center of the opening is preffered as it gives the most room for error while in a match. Thus, every solution also includes the distance from the collision point (the intersection of the ring and the opening) to the center of the opening as a "rating function" for how good the solution is. This will be useful when culling down the solutions to just one solution per every distance checked, so that we can create a mathematical equation for angle/distance and speed/distance by interpolating the data points later. This will allow for faster on-the-go calculation of the values in the code, and make the robot code more efficient.

WIP: merging the values into one file (every process has its own file to avoid locks on the file, which would make the processes not parallel but sequential) and culling the values.

## How to empirically find the drag coefficient
To empirically find the drag coefficient, you can use the provided file by giving real-world values for the angle at which the ring is shot, the velocity of the ring as it exits the shooter and the distance that the ring traveled in the X coordinate (distance from robot center to the ring's landing location).

For the angle, we can easily calculate that from encoder values of the motors that actuate the shooter, or in the case of fixed-angle shooters, simply the angle at which the shooter is mounted.

For the exit velocity, it would be possible to calculate this using a slow-motion camera and a ruler. Take the distance traveled in the span of 2-10 frames and the time between those frames and you have the exit velocity (if distance is measured in X or Y axis you have to do a little bit of trigonometry to figure out the actual velocity of the ring).

A camera could also record the impact of the ring and the ground and figure out the precise location of the landing point (a tolerance of + or - 20 cm is probably good enough).

These values can be input into the file and the file will run the simulations to figure out the coefficient and it will output it to the terminal as a double. You can change the tolerance of the algorithm for more accurate results, but it may severely slow down the process of finding the values.

The same optimizations that we used for the actual simulator are applied here. For a given angle and speed, a bigger coefficient of drag would make the ring land closer to the robot and a smaller one would make the ring land farther. Thus we can once again use a binary search method to find the value. The simulation is once again split into several processes each with their own sub-ranges of drag coefficients to test on.

NOTE: To be tested with real rings. None of this has yet been tested with actual real-life rings and robots, this whole project is theoretical and nature and bugs/inconsistencies may arise from that. If you have anything to contribute to this, be sure to leave me a message over on Discord, my username is 0xC00000FD.