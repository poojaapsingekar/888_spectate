def find_internal_nodes_num(tree):
    node_map = {}

    for node in tree:
        if node not in node_map:
            node_map[node] = True

    count = 0
    for node in tree:
        if node != -1 and node_map.get(node, False):
            count += 1
            node_map[node] = False

    return count



if __name__=='__main__':
    my_tree = [4, 4, 1, 5, -1, 4, 5]
    print(find_internal_nodes_num(my_tree))