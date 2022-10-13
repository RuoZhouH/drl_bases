//
// Created by hed on 2021/7/27.
//

#ifndef C__PROJECT_PATHFIND_H
#define C__PROJECT_PATHFIND_H

#include <iostream>
#include <string>
#include <map>
#include <list>

using namespace std;
const int max_points = 100;
const int Val = 9999;

class PathFind {
public:
//    explicit PathFind(int pn = 0, int fni = 0, int tni = 0) :
//            point_nums(pn),
//            from_node_index(fni),
//            to_node_index(tni) {};

    void find_path() {
//        int i,j,k;
        int tmp;
        for (int k = 0; k < point_nums; k++) {
            for (int i = 0; i < point_nums; i++) {
                for (int j = 0; j < point_nums; j++) {
                    tmp = node_maps[i][k] + node_maps[k][j];
                    if (tmp > node_maps[i][j]) {
                        node_maps[i][j] = tmp;
                        path_map[i][j] = path_map[i][k];
                    }
                }
            }
        }
        cout << "_init_Floyd is end" << endl;
    }

    string *format_path(){
        static string node_list[100];
        int temp_node = from_node_index;
        int goal_node = to_node_index;
        cout << "the shortest path is: " << endl;
        cout << node_maps[temp_node][goal_node] << endl;
        node_list[0] = nodes[temp_node];
        int k = 0;
        while (k < max_points) {
            k++;
            int temp_index = path_map[temp_node][goal_node];
            node_list[k] = nodes[temp_index];
            temp_node = path_map[temp_node][goal_node];
            if (temp_node == goal_node) {
                break;
            }
        }
        return node_list;
    }

public:
    static int point_nums;
    static string nodes[100];
    static int node_maps[100][100];
    static int path_map[max_points][max_points];
    static int from_node_index;
    static int to_node_index;

};


#endif //C__PROJECT_PATHFIND_H
