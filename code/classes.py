import math

class Obstacle:
    def __init__(self, x: float, y: float, d: float):
        self.x = x
        self.y = y
        self.diameter = d
        self.radius = d / 2


class Node:
    def __init__(self, x: float, y: float, id: int, heuristic=None):
        self.id = id
        self.x = round(x, 3)
        self.y = round(y, 3)
        # Heuristic cost to go is Euclidian distance from the current node to the goal node
        if heuristic is None:
            self.heuristic_ctg = round(math.sqrt(math.pow(0.5 - x, 2) + math.pow(0.5 - y, 2)), 5)
        else:
            self.heuristic_ctg = heuristic

    # Method for determining distance between two nodes placed in the xy plane
    # There are two overloads of the method:
    # 1) checking distance between self node and second_node
    # 2) checking distance between self node and x,y
    def distance_between(self, second_node=None, x=None, y=None):
        if second_node is None:
            x_seg = x
            y_seg = y
        else:
            x_seg = second_node.x
            y_seg = second_node.y
        distance = math.sqrt(math.pow(x_seg - self.x, 2) + math.pow(y_seg - self.y, 2))
        return round(distance, 4)

    def check_is_in_circle_obstacle(self, obstacle: Obstacle):
        # Distance between center of obstacle and node can be found using Pythagorean theorem
        distance_center_node = self.distance_between(x=obstacle.x, y=obstacle.y)

        # If that distance is less than obstacle RADIUS + 0.02 (just to blue circle of node doesn't hit the obstacle)
        # it means that node is outside the obstacle area and return True for the collision
        if distance_center_node < obstacle.radius + 0.02:
            return True

        return False


class Edge:
    def __init__(self, first_node: Node, second_node: Node):
        # Every edge has 2 nodes and distance between them
        self.node1 = first_node
        self.node2 = second_node
        # Cost is simply distance between two nodes - length of the edge
        self.cost = first_node.distance_between(second_node=second_node)
        self.length = self.cost

    # Some basic trignometry - draw line and circle and connect first point and center of circle
    # then we check whether perpendicular line t is less than radius of the circle and that is my algorithm
    def check_collision_with(self, circle_obstacle: Obstacle):

        # Length of the edge
        L = self.length
        # Distance between first node and center of circle obstacle
        e = self.node1.distance_between(x=circle_obstacle.x, y=circle_obstacle.y)

        alpha = math.atan2(circle_obstacle.y - self.node1.y, circle_obstacle.x - self.node1.x)
        beta = math.atan2(self.node2.y - self.node1.y, self.node2.x - self.node1.x)
        theta = alpha - beta

        # Line perpendicular from the center of the obstacle to the line going through edge
        t = e * math.sqrt(1 - math.pow(math.cos(theta), 2))

        # Distance between node2 and center of circle obstacle
        h = self.node2.distance_between(x=circle_obstacle.x, y=circle_obstacle.y)

        if t <= circle_obstacle.radius:
            # We can have two case of intersections:
            # 1) When reached the circle and perpendicular line is less than radius
            #    We need to check is distance between second node and center of circle less than radius - intersection
            if h <= circle_obstacle.radius:
                return True
            # 2) Line intersects with circle at two points, then distance between first node and center e is
            # less than length of the whole line L
            elif e < L:
                return True
