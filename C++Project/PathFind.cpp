//
// Created by hed on 2021/7/27.
//

#include "PathFind.h"
#include <iostream>
#include <string>
#include <map>
#include <list>


using namespace std;

typedef struct MapCost {
    string from_node;
    string to_node;
    int cost;
    MapCost(string from_node, string to_node, int cost) {
        from_node = from_node;
        to_node = to_node;
        cost = cost;
    };
} MapC;

typedef struct x_y {
    int x;
    int y;

    x_y(int x, int y) {
        x = x;
        y = y;
    };
} xy;

int node_index(string node[], const string &s, int point_nums) {

    if (point_nums <= 0) {
        return 0;
    }
    for (int i = 0; i < point_nums; i++) {
        if (node[i] == s) {
            return i;
        }
    }
    return 0;
}

void set_node_map(int points_num, int node_map[][100], string node[], MapCost *node_list, int path_map[][100],
                  int cost_edges) {
    if (points_num <= 0) {
        return;
    }
    for (int i = 0; i < points_num; i++) {
        node_map[i][i] = 0;
    }

    for (int j = 0; j < 1000; j++) {
        if (node_list[j].from_node.empty()) {
            break;
        }
        string x = node_list[j].from_node;
        string y = node_list[j].to_node;
        int cost = node_list[j].cost;
        int x_index = node_index(node, x, points_num);
        int y_index = node_index(node, y, points_num);
        if (x_index == y_index) {
            continue;
        }
//        node_map[x_index][y_index] = node_map[y_index][x_index] = cost;
        node_map[x_index][y_index] = cost;
        path_map[x_index][y_index] = y_index;
        path_map[y_index][x_index] = x_index;
    }
}


int main() {
    int x_range[2] = {0, 10};
    int y_range[2] = {0, 10};
    //起点
    int start_point[2] = {0, 1}; //{x, y}
    //终点
    int goal_point[2] = {8, 9};
    int edge_cost = 10;
    int x_point[10];
    int y_point[10];
    for (int i = x_range[0]; i < x_range[1]; i++) {
        x_point[i] = i;
    }
    for (int i = y_range[0]; i < y_range[1]; i++) {
        y_point[i] = i;
    }
    map<string, x_y> str_node_map;
    string node_list[100];
    MapC *map_costs;
    int points_num;
    int index_counts = 0;
    for (int x = x_point[0]; x < x_point[9]; x++) {
        for (int y = y_point[0]; y < y_point[9];y++) {
            string node = to_string(x) + "_" + to_string(y);
            str_node_map.insert(pair<string, x_y>(node, xy(x, y)));
            node_list[index_counts] = node;
            index_counts += 1;
        }
    }
    points_num = index_counts;

    int index_count = 0;
    for (int x = x_point[0]; x < x_point[9]; x++) {
        for (int y = y_point[0]; y < y_point[9];y++) {
            string node = to_string(x) + "_" + to_string(y);
            string right_node = to_string(x + 1) + "_" + to_string(y);
            string up_node = to_string(x) + "_" + to_string(y + 1);
            string left_node = to_string(x - 1) + "_" + to_string(y);
            string down_node = to_string(x) + "_" + to_string(y - 1);
            if (x == x_range[0] && y == y_range[0]) {
                map_costs[index_count] = MapCost(node, up_node, edge_cost);
//                map_costs[index_count].from_node = node;map_costs[index_count].to_node = up_node;map_costs[index_count].cost = edge_cost;
                map_costs[index_count + 1] = MapCost(node, right_node, edge_cost);
                index_count += 2;
            } else if (x == x_range[0] && y_range[0] < y && y < y_range[1] - 1) {
                map_costs[index_count] = MapCost(node, up_node, edge_cost);
                map_costs[index_count + 1] = MapCost(node, right_node, edge_cost);
                map_costs[index_count + 2] = MapCost(node, down_node, edge_cost);
                index_count += 3;
            } else if (x_range[0] < x && x < x_range[1] - 1 && y == y_range[0]) {
                map_costs[index_count] = MapCost(node, up_node, edge_cost);
                map_costs[index_count + 1] = MapCost(node, right_node, edge_cost);
                map_costs[index_count + 2] = MapCost(node, left_node, edge_cost);
                index_count += 3;
            } else if (x_range[0] < x && x < x_range[1] - 1 && y_range[0] < y && y < y_range[1] - 1) {
                map_costs[index_count] = MapCost(node, up_node, edge_cost);
                map_costs[index_count + 1] = MapCost(node, right_node, edge_cost);
                map_costs[index_count + 2] = MapCost(node, left_node, edge_cost);
                map_costs[index_count + 3] = MapCost(node, down_node, edge_cost);
                index_count += 4;
            } else if (x == x_range[1] - 1 && y == y_range[1] - 1) {
                map_costs[index_count] = MapCost(node, left_node, edge_cost);
                map_costs[index_count + 1] = MapCost(node, down_node, edge_cost);
                index_count += 2;
            } else if (x == x_range[1] - 1 && y_range[0] < y && y < y_range[1] - 1) {
                map_costs[index_count] = MapCost(node, up_node, edge_cost);
                map_costs[index_count + 1] = MapCost(node, left_node, edge_cost);
                map_costs[index_count + 2] = MapCost(node, down_node, edge_cost);
                index_count += 3;
            } else if (x_range[0] < x && x < x_range[1] - 1 && y == y_range[1] - 1) {
                map_costs[index_count] = MapCost(node, right_node, edge_cost);
                map_costs[index_count + 1] = MapCost(node, left_node, edge_cost);
                map_costs[index_count + 2] = MapCost(node, down_node, edge_cost);
                index_count += 3;
            }
        }
    }

    int node_map[100][100];
    int path_map[100][100];
    for (int i = 0; i < points_num; i++) {
        for (int j = 0; j < points_num; j++) {
            node_map[i][j] = Val;
        }
    }

    for (int i = 0; i < points_num; i++) {
        for (int j = 0; j < points_num; j++) {
            path_map[i][j] = 0;
        }
    }

    set_node_map(points_num, node_map, node_list, map_costs, path_map, edge_cost);

    string start_points = to_string(start_point[0]) + "_" + to_string(start_point[1]);
    string end_points = to_string(goal_point[0]) + "_" + to_string(goal_point[1]);

    int from_node = node_index(node_list, start_points, points_num);
    int to_node = node_index(node_list, end_points, points_num);
//    Floyd_Path floyd_path(points_num, node_list, node_map, path_map, from_node, to_node);
//    Floyd_Path::init(points_num, node_list, node_map, path_map, from_node, to_node);

    PathFind floyd_Path;
    floyd_Path.point_nums = points_num;
    floyd_Path.from_node_index = from_node;
    floyd_Path.to_node_index = to_node;
    for(int i=0;i<points_num;i++){
        floyd_Path.nodes[i] = node_list[i];
        for(int j=0;j<points_num;j++){
            floyd_Path.node_maps[i][j] = node_map[i][j];
            floyd_Path.path_map[i][j] = path_map[i][j];
        }
    }

    floyd_Path.find_path();
    string *path;
    path = floyd_Path.format_path();
    for (int i = 0; i < 100; i++) {
        cout << "path" << endl;
        cout << *path << endl;
    }
    return 0;
}