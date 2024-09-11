# Robot Motion Planning

### Python scripts that discretize 2D C-space with cylindrical obstacles and find best possible path to the final position

## Project Description

Project is based on discretizing and finding the best possible path for the robot, given boundaries of 2D plane of C-space determined by x ∈ [-0.5, 0.5] and y ∈ [-0.5, 0.5] where the starting position is at (-0.5, -0.5) and final positon at (0.5, 0.5). Also C-space has cylindrical obstacles with properties (xC, yC, and diameter) given in `obstacles.csv` file. These obstacles can be edited with desired but possible values.

First part of the project is discretizing the space using PRM (Probabilistic RoadMap) algorithm where nodes are appointed randomly and saved in the `nodes.csv` files with 3 pieces of data (x coordinate, y coordinate, and distance from final position). Number of samples are determined by the user. Nodes cannot be inside any of obstacles so algorithm needs to check every node with every obstacle. After nodes are created, edges that connecting nodes needs to be determined. Maximum number of connections `k` for each node are also determined by user. Edge cannot cross the obstacles so for each edge it has to check for the collision with each obstacles. Then `k` shortest edges are picked and saved in the `edges.csv` file with 3 pieces of data - sequence number of the points connecting line and length of the edge.

Second part of the project is to define best possible (shortest) path from the starting to the final position, and A* algorithm is used which is given in the `a_star_algorithm.py` file

## How To Use 
In the `prm_properties.py` you need to define desired number of node samples which will be used for discretization and maximum number of connections that each node can have with other neighbor nodes, as well as the starting and final position of the motion. Also obstacles can be edited and created in `obstacles.csv` file. Running `main.py` file will create shortest path which will be saved in the `path.csv` file. Now in CoppeliaSim Application (app for Robotics) you can import `obstacles.csv`, `nodes.csv`, `edges.csv` and `path.csv` to visualize the motion of the robot in the 2D plane
