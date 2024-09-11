import csv
import random
import math
from classes import *
from prm_properties import *
from a_star import *


def main():
    # 1) Creating list of obstacles - every element is instance of Obstacle class
    obstacles = load_obstacles()

    # 2) Creating nodes in C-free space
    nodes = sampling(obstacles)

    # 3) Defining edges
    creating_edges(nodes, obstacles, k=MAX_NODES_CONNECT)

    # 4) A star algorithm for finding the best available path can be called
    a_star_algorithm()


# Loading obstacles from the given obstacles.csv file into obstacles list
def load_obstacles():
    with open('../results/obstacles.csv', 'r') as file:
        csv_reader = csv.reader(file)
        obstacles = []
        for row in csv_reader:
            # If first character is # then that line is comment
            if row[0][0] != "#":
                x_coord = float(row[0].strip())
                y_coord = float(row[1].strip())
                diameter = float(row[2].strip())
                # Every obstacle is instance od class Obstacle with its x, y coordinates and diameter
                one_obstacle = Obstacle(x_coord, y_coord, diameter)
                obstacles.append(one_obstacle)
        return obstacles


# Creating nodes in the C-free space from the given C-space
def sampling(all_obstacles):
    # Starting node will be the first node in the list nodes
    starting_node = Node(x=C_SPACE_LIMITS["start"]["x"], y=C_SPACE_LIMITS["start"]["y"], id=1)
    nodes = [starting_node, ]

    # Starting node has ID of 1, so next will have ID of 2
    id_counter = 2
    # This while loop will run until list nodes have specified number of samples in nodes list
    while True:
        if len(nodes) == NUMBER_OF_SAMPLES - 1:
            break

        # Uniformly chosen node in the whole C-space
        node = Node(x=random.uniform(C_SPACE_LIMITS["start"]["x"], C_SPACE_LIMITS["goal"]["x"]),
                    y=random.uniform(C_SPACE_LIMITS["start"]["y"], C_SPACE_LIMITS["goal"]["y"]),
                    id=id_counter)

        # We need to check whether node is in the area of the obstacles
        for obstacle in all_obstacles:
            is_node_in_obstacle = node.check_is_in_circle_obstacle(obstacle)
            # If collision is detected, then new random node needs to be chosen in while loop
            if is_node_in_obstacle:
                break
        # Else, then we will append this node into list of nodes
        else:
            node.id = id_counter
            id_counter += 1
            nodes.append(node)

    # Goal node will be the last node in the list nodes
    goal_node = Node(x=C_SPACE_LIMITS["goal"]["x"], y=C_SPACE_LIMITS["goal"]["y"], id=NUMBER_OF_SAMPLES)
    nodes.append(goal_node)

    # We will save data to nodes.csv
    with open('../results/nodes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["# node_id | x | y | distance_to_the_goal_node"])
        for single_node in nodes:
            # Data needs to be in list format - as follows
            data = [single_node.id, single_node.x, single_node.y, single_node.heuristic_ctg]
            writer.writerow(data)

    return nodes


# Creating edges from the existing nodes, obstacles and maximum number of connected nodes k
def creating_edges(nodes, obstacles, k):
    # This list will be saved into csv file later on
    graph_edges = []
    # We need to find the nearest nodes to the fixed node
    for fixed_node in nodes:
        # All possible edges of this node will be saved into this list:
        edges = []
        # These are all edges to the all neighbor nodes from fixed nodes
        # All neighbor node
        for neighbor_node in nodes:
            # We need to skip same node
            if fixed_node.id == neighbor_node.id:
                continue

            edge = Edge(first_node=fixed_node, second_node=neighbor_node)
            for obstacle in obstacles:
                if edge.check_collision_with(obstacle):
                    break
            # If it is last obstacle and no collision found we need to append this edge in the list of all possible
            # edges between the current fixed node and that examined node - this will be done for all nodes in the plane
            else:
                edges.append(edge)

        # Now we have to extract edges to the k-closest nodes
        # First we need to sort edges by its cost (which is simply length)
        sorting_by_length(edges)

        # Now we need to extract only edges to the k-closest nodes
        k_edges = edges[0:k]

        # After that we need to see whether these k_edges are already in the list just to avoid duplicates in csv file
        # graph_edges is the final list which will be saved in the csv file
        # If there is no saved edges in graph_edges (length of the list is zero) we immediately append edge
        for edge in k_edges:
            if len(graph_edges) == 0:
                graph_edges.append(edge)
            else:
                # We need to check whether edge is already in the edge list
                for existing_edge in graph_edges:
                    # For example 1-5 line is the same as 5-1 line so current edge is 5-1 ids of both edges are
                    # the same
                    if edge.node1.id == existing_edge.node2.id and edge.node2.id == existing_edge.node1.id:
                        break
                # If there is no existing_edge in list of graph_edges then we append our current_edge
                else:
                    graph_edges.append(edge)

    with open('../results/edges.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["# from | to | distance"])
        for edge in graph_edges:
            data = [edge.node1.id, edge.node2.id, edge.cost]
            writer.writerow(data)


# Bubble sort - input is reference type, so we don't need to return sorted list - edges will be sorted directly
def sorting_by_length(edges):
    for i in range(len(edges)):
        for j in range(0, len(edges) - i - 1):
            if edges[j].length > edges[j + 1].length:
                swap = edges[j]
                edges[j] = edges[j + 1]
                edges[j + 1] = swap


main()