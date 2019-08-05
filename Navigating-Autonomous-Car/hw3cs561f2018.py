import numpy as np
import math
import copy
import mdp_new
import operator


orientations = [(0,-1), (0, 1), (1, 0), (-1, 0)]
# orientations = [(1,0), (0, -1), (-1, 0), (0, 1)]

argmax = max

def vector_add(a, b):
    return tuple(map(operator.add, a, b))


def turn_right(orientation):
    return orientations[orientations.index(orientation)-1]


def turn_left(orientation):
    return orientations[(orientations.index(orientation)+1) % len(orientations)]

def take_input(input):
    # with open('testcases/input49.txt') as fin:
    with open(input) as fin:
        file_data = fin.read()
        input = file_data.split("\n")
        grid_size = int(input[0])
        no_of_cars = int(input[1])
        no_of_obstacles = int(input[2])
        t = no_of_obstacles
        i = 3
        loc_of_obstacles = []
        while (t != 0):
            coord = input[i]
            loc_of_obstacles.append(coord)
            i = i + 1
            t = t - 1
        x = no_of_cars
        start_loc =[]
        while(x!=0):
            coord = input[i]
            start_loc.append(coord)
            i = i + 1
            x = x - 1
        x = no_of_cars
        terminal_loc =[]
        while(x!= 0):
            coord = input[i]
            terminal_loc.append(coord)
            i = i + 1
            x = x - 1
    return grid_size, no_of_cars, loc_of_obstacles, start_loc, terminal_loc
    fin.close()


def left_simulator(move):
    if move == '<':
        return 'v'
    if move == 'v':
        return '>'
    if move == '>':
        return '^'
    if move == '^':
        return '<'


def right_simulator(move):
    if move == '<':
        return '^'
    if move == 'v':
        return '<'
    if move == '>':
        return 'v'
    if move == '^':
        return '>'


def change_pos(move, pos, grid_size):
    x = pos[0]
    y = pos[1]
    if move == '<':
        if y > 0:
            y = y - 1
    elif move == '>':
        if y < grid_size - 1:
            y = y + 1
    elif move == '^':
        if x > 0:
            x = x - 1
    elif move == 'v':
        if x < grid_size - 1:
            x = x + 1
    return x, y

def optimal_policy_for_car(obstacle_matrix, end_x, end_y, grid_size):

    car_matrix = copy.deepcopy(obstacle_matrix)
    car_matrix[end_x][end_y] = 99
    if end_y < (grid_size - 1) / 2:
        y_dash = (grid_size) / 2 + ((grid_size - 1) / 2 - end_y)
    else:
        y_dash = (grid_size) / 2 - (end_y - (grid_size - 1) / 2)

    car_matrix = zip(*car_matrix)
    car_matrix_rev = copy.deepcopy(car_matrix)
    mdp = mdp_new.GridMDP(car_matrix_rev, terminals=[(end_x, y_dash)])
    vi = mdp_new.value_iteration(mdp)
    pi = mdp_new.best_policy(mdp, vi)
    # pi = mdp_new.policy_iteration(mdp)
    table = mdp.to_arrows(pi)
    # print_table(table)

    return car_matrix, table

def split_x_y(coord):
    coord = coord.split(",")
    x = int(coord[0])
    y = int(coord[1])
    return x, y

if __name__ == '__main__':
    fout = open('output.txt', 'w')
    input = 'input.txt'
    grid_size, no_of_cars, loc_of_obstacles, start_loc, terminal_loc = take_input(input)
    matrix = [[-1 for end_x in range(grid_size)] for end_y in range(grid_size)]
    while loc_of_obstacles:
        obstacle_pos = loc_of_obstacles.pop()
        obstacle_pos = obstacle_pos.split(",")
        obstacle_pos_x = int(obstacle_pos[0])
        obstacle_pos_y = int(obstacle_pos[1])
        matrix[obstacle_pos_x][obstacle_pos_y] = -101

    for i in range(0, no_of_cars):
        start_loc_pos = start_loc[i]
        end_pos = terminal_loc[i]
        start_y, start_x = split_x_y(start_loc_pos)
        end_x, end_y = split_x_y(end_pos)
        end_loc_pos = end_y, end_x
        car_matrix, table = optimal_policy_for_car(matrix, end_x, end_y, grid_size)
        reward_count = [0 for z in range(10)]
        sum = 0
        for j in range(10):
            reward_count[j] = 0
            pos = (start_x, start_y)
            np.random.seed(j)
            swerve = np.random.random_sample(1000000)
            k = 0
            while pos != end_loc_pos:
                move = table[pos[0]][pos[1]]
                if swerve[k] > 0.7:
                    if swerve[k] > 0.8:
                        if swerve[k] > 0.9:
                            move = right_simulator(right_simulator(move))
                        else:
                            move = right_simulator(move)
                    else:
                        move = left_simulator(move)
                pos = change_pos(move, pos, grid_size)
                reward_count[j] = reward_count[j] + car_matrix[pos[0]][pos[1]]
                k += 1
            sum = sum + reward_count[j]
        ans = int(math.floor(sum/10))
        fout.write(str(ans)+'\n')
        print ans
    fout.close()