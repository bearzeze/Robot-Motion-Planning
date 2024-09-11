import csv
from classes import *
from prm_properties import *
import random
import matplotlib.pyplot as plt
import numpy as np


def try_intersections_line_circle():
    node1 = Node(-0.5, -0.5, 1)
    node2 = Node(0.2, 0.32, 30)

    edge = Edge(node1, node2)
    obstacle = Obstacle(0, 0, 0.4)

    x = np.linspace(obstacle.x - obstacle.radius, obstacle.x + obstacle.radius, 300)
    y = np.zeros(len(x))
    for i in range(0, len(x)):
        y[i] = math.sqrt(math.pow(obstacle.radius, 2) - math.pow((x[i] - obstacle.x), 2))

    plt.plot(x, y + obstacle.y, 'b', x, -y + obstacle.y, 'b', obstacle.x, obstacle.y, 'bx')
    plt.grid()
    plt.plot([node1.x, node2.x], [node1.y, node2.y], 'r')
    plt.plot([node1.x, obstacle.x], [node1.y, obstacle.y], 'k--')

    e = node1.distance_between(x=obstacle.x, y=obstacle.y)

    alpha = math.atan2(obstacle.y - node1.y, obstacle.x - node1.x)
    beta = math.atan2(node2.y - node1.y, node2.x - node1.x)
    theta = alpha - beta

    t = e * math.sqrt(1 - math.pow(math.cos(theta), 2))
    print(t)
    print(obstacle.radius)

    # Distance between node2 and center of circle
    h = node2.distance_between(x=obstacle.x, y=obstacle.y)
    print(h)

    if t <= obstacle.radius:
        # We can have three case here:
        # 1) When reached the circle and perpendicular line is less than radius
        #    We need to check is distance between second node and center of circle less than radius - intersection
        if h <= obstacle.radius:
            print("Intersekcija")
        # 2) Line intersects with circle at two points, then distance between first node and center is less than length
        # of the whole line
        elif edge.length > node1.distance_between(x=obstacle.x, y=obstacle.y):
            print("Intersekcija")

    plt.show()