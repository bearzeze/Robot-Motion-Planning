import csv


def a_star_algorithm():
    # Here will be everything about nodes in the roadmap
    node = [
        # First entry is None, because we want that second entry - node[1] be first node in list node
        None,
        # Every other node will be dictionary element - see lecture_example.py for the better understanding
    ]

    # First nodes.csv file is opened for getting all nodes and optimistic cost only
    with open('../results/nodes.csv', 'r') as nodes_file:
        csv_reader = csv.reader(nodes_file)
        for row in csv_reader:
            # We skip every row which begins with # - these are comments
            if row[0][0] == "#":
                continue

            # Every node will have these properties - some are filled with this csv file, other with other csv files
            single_node_dict = {
                # First entry in row is node label
                "id": int(row[0]),
                "past_cost": None,
                # Fourth entry in row is optimistic cost to go
                "optimist_ctg": float(row[3]),
                "total_cost": None,
                "parent_node": None,
                "cost_to": {},
            }

            node.append(single_node_dict)

    # Then edges.csv file is opened where we will get all neighbor nodes with edge cost to it
    with open('../results/edges.csv', 'r') as edges_file:
        csv_reader = csv.reader(edges_file)
        for row in csv_reader:
            # We skip every row which begins with # - these are comments
            if row[0][0] == "#":
                continue

            from_node = int(row[0])
            to_node = int(row[1])
            cost = float(row[2])

            # In one direction
            node[from_node]["cost_to"][to_node] = cost
            # and in another same cost
            node[to_node]["cost_to"][from_node] = cost

    # First node past_cost is 0 and total_cost is sum of past_cost and optimistic_cost
    node[1]["past_cost"] = 0
    node[1]["total_cost"] = node[1]["past_cost"] + node[1]["optimist_ctg"]

    OPEN = [node[1], ]
    # VISITED (CLOSED) list is initialized
    VISITED = []

    while True:
        current_node = OPEN[0]
        # If the current node is last node in the web, we finish the algorithm
        if current_node == node[len(node) - 1]:
            get_best_path(node)
            break

        # Else we examine all neighbor nodes which are keys of cost_to dictionary of current node
        for neighbor_node in current_node["cost_to"].keys():
            # If this neighbor node has already been visited then go to the next neighbor node
            if node[neighbor_node] in VISITED:
                continue

            # This is variable just for replacing nodes in open list if better path is found and node is already in open
            # which means it has been already visited but will be replaced by better cost to it
            replace_node_in_opened = False

            # First we need to examine whether this is the best path to this neighbor node from the current node
            # to neighbor node, which consists of past cost of current node and edge cost between these 2 nodes
            path_to_neighbor_node = round(current_node["past_cost"] + current_node["cost_to"][neighbor_node], 5)
            # If this value is less to the previous past_cost of the neighbor node or
            # neighbor node has None past_cost value (as the case when node is visited for the first time)
            if node[neighbor_node]["past_cost"] is None or path_to_neighbor_node < node[neighbor_node]["past_cost"]:
                # This also means that we need to replace same node in OPEN list with better past_cost
                # But only if the neighbor node is already visited before (past cost is not None)
                if node[neighbor_node]["past_cost"] is not None:
                    replace_node_in_opened = True

                # Then this path_to_neighbor_node is new best (lowest) past cost for the neighbor node
                node[neighbor_node]["past_cost"] = path_to_neighbor_node
                # Current node becomes the parent node with best lowest path to this neighbor node
                node[neighbor_node]["parent_node"] = current_node["id"]

            # Estimated total cost of neighbor node is equal to past cost and heuristic cost
            node[neighbor_node]["total_cost"] = \
                round(node[neighbor_node]["past_cost"] + node[neighbor_node]["optimist_ctg"], 5)

            # We need to replace node in OPEN list with better neighbor node (with lower past_cost)
            if replace_node_in_opened:
                for i in range(0, len(OPEN)):
                    if OPEN[i]["id"] == node[neighbor_node]["id"]:
                        OPEN[i] = node[neighbor_node]
            # Else we add this neighbor node to the OPEN list
            else:
                OPEN.append(node[neighbor_node])

        # This NEW list will be list without any duplicates in OPEN list
        NEW = []
        for i in range(0, len(OPEN)):
            if OPEN[i] not in NEW:
                NEW.append(OPEN[i])

        # OPEN list is reloaded with no duplicate elements
        OPEN = NEW.copy()

        # Sorting OPEN list by total_cost - first will have lowest one
        sorting_opened_list(OPEN)

        # Current node is now in VISITED (CLOSED) list and removed from open
        VISITED.append(current_node)
        OPEN.remove(current_node)

        # If there is no nodes in OPEN list, there are no paths available
        if len(OPEN) == 0:
            print("No path available! \n\nIncrease number of samples or increase number of connections between nodes.")

            # Path file will have only 1 in the row to indicate first node
            with open('../results/path.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["# No path available!"])
                writer.writerow([1])

            break


# Bubble sort algorithm - sorting OPEN list by total_cost
def sorting_opened_list(open_list):
    for i in range(len(open_list)):
        for j in range(0, len(open_list) - i - 1):
            if open_list[j]["total_cost"] >= open_list[j + 1]["total_cost"]:
                swap = open_list[j]
                open_list[j] = open_list[j + 1]
                open_list[j + 1] = swap


# Getting the best path as csv file and printing in command window
def get_best_path(nodes):
    # Last node is always finish line in the trace
    current_node = nodes[len(nodes) - 1]
    # path array is initialized with final node number
    path = [current_node["id"]]
    while True:
        current_node = nodes[current_node["parent_node"]]
        # When we get to the first node, path is finally created
        if current_node["id"] == 1:
            path.append(1)
            break
        else:
            path.append(current_node["id"])

    # Reversing to get first node as starting position of the path
    path.reverse()
    # Printing the best path in Command window - first making list of strings and then printing it into command window
    path_str = [str(number) for number in path]
    print(" - ".join(path_str))

    # Saving best path as row in csv file
    with open('../results/path.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["# path from the first to the last node"])
        writer.writerow(path)
