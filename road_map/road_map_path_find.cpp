

#include <iostream>
#include <string>
#include <map>
#include <list>
#include <map>

using namespace std;

#define max_points = 10;
#define Val = 9999;

typedef struct map_edge_cost{
    string from_node;
    string to_node;
    int cost;
    map_edge_cost(string from_node, string to_node, int cost){
        from_node = from_node;
        to_node = to_node;
        cost = cost;
    }
} map_cost;

typedef struct x_y{
    int x;
    int y;
    x_y(int x, int y){
        x = x;
        y = y;
    };
} xy;

class Floyd_Path
{
    public:
        int point_nums;
        string node[max_points];
//        map<string, string> nodes_map;
        int node_map[max_points][max_points];
        int path_map[max_points][max_points];
        int from_node_index;
        int to_node_index;

    public:
        init(int point_nums, string node[],int node_map[][], int path_map[][], int from_node_index, int to_node_index){
            this.point_nums = point_nums;
            this.node = node;
            this.node_map = node_map;
            this.path_map = path_map;
            this.from_node_index = from_node_index;
            this.to_node_index = to_node_index;
        }

        find_path(){
            int i,j,k;
            int tmp;
            for(k=0;k<this.point_nums;k++){
                for(i=0;i<this.point_nums;i++){
                    for(k=0;k<this.point_nums;j++){
                        tmp = this.node_map[i][k] + this.node_map[k][j];
                        if(tmp > this.node_map[i][j]){
                            this.node_map[i][j] = tmp;
                            this.path_map[i][j] = this.path_map[i][k];
                        }
                    }
                }
            }
            cout << '_init_Floyd is end' << endl;

        }

        format_path(){
            string node_list[max_points];
            temp_node = this.from_node_index;
            goal_node = this.to_node_index;
            cout << "the shortest path is: " << endl;
            cout << this.node_map[temp_node][goal_node] << endl;
            node_list[0] = this.node[temp_node];
            int k = 0;
            while (k < max_points){
                k++;
                int temp_index = this.path_map[temp_node][goal_node];
                node_list[k] = this.node[temp_index];
                temp_node = this.path_map[temp_node][goal_node];
                if(temp_node == goal_node){
                    break;
                }
            }
            return node_list;
        }
}

void set_node_map(int points_num, int node_map[][], string node[], map_edge_cost node_list[], int path_map[][], int cost_edges){
    if(points_num <= 0){
        return
    }
    for(int i=0; i < points_num; i++){
        node[i][i] = 0;
    }

    for(int j=0;j < cost_edges; j++){
        string x = node_list[j].from_node;
        string y = node_list[j].to_node;
        int cost = node_list[j].cost;
        int x_index = node_index(node, x, points_num);
        int y_index = node_index(node, y, points_num);

        node_map[x_index][y_index] = node_map[y_index][x_index] = cost;
        node_map[x_index][y_index] = cost;
        path_map[x_index][y_index] = y_index;
        path_map[y_index][x_index] = x_index;


    }


}

int node_index(string node[], string s， int point_nums){

    if(point_nums <= 0 ){
        return 0;
    }
    for(int i=0;i<point_nums;i++){
        if(node[i] == s){
            return i;
        }
    }
}



int main(){
    int x_range[2] = {0, 10};
    int y_range[2] = {0, 10};
    //起点
    int start_point[2] = {0, 1}; //{x, y}
    //终点
    int goal_point[2] = {8, 9};
    int edge_cost = 10;
    int x_point[10];
    int y_point[10];
    for(int i=x_range[0]; i<x_range[1]; i++){
        x_point[i] = i;
    }
    for(int i=y_range[0]; i<y_range[1]; i++){
        y_point[i] = i;
    }
    map<string, x_y> str_node_map;
    string node_list[100];
    map_edge_cost map_costs[];
    int points_num = 0;
    int floor = 0;
    for(int k=0; k< 10; k++){
        for(int v=0; v<10; v++){
            int x = x_point[k];
            int y = y_point[v];
            string node = to_string(x) + "_" + to_string(y);
            str_node_map.insert(pair<string, x_y>(node, xy(x, y)));
            node_list[floor] = node;
            floor += 1;
        }
    }
    points_num = floor;

    int floor = 0;
    for(int k=0; k< 10; k++){
        for(int v=0; v<10; v++){
            int x = x_point[k];
            int y = y_point[v];
            string node = to_string(x) + "_" + to_string(y);
            string right_node = to_string(x + 1) + "_" + to_string(y);
            string up_node = to_string(x) + "_" + to_string(y + 1);
            string left_node = to_string(x-1) + "_" + to_string(y);
            string down_node = to_string(x) + "_" + to_string(y-1);
            if (x == x_range[0] and y == y_range[0]){
                map_costs[floor] = map_cost(node, up_node, edge_cost);
                map_costs[floor+1] = map_cost(node, right_node, edge_cost);
                floor += 2;
            }
            else if(x == x_range[0] and y_range[0] < y < y_range[1] - 1){
                map_costs[floor] = map_cost(node, up_node, edge_cost);
                map_costs[floor+1] = map_cost(node, right_node, edge_cost);
                map_costs[floor+2] = map_cost(node, down_node, edge_cost);
                floor += 3;
            }
            else if (x_range[0] < x < x_range[1] - 1 and y == y_range[0]){
                map_costs[floor] = map_cost(node, up_node, edge_cost);
                map_costs[floor+1] = map_cost(node, right_node, edge_cost);
                map_costs[floor+2] = map_cost(node, left_node, edge_cost);
                floor += 3;
            }
            else if (x_range[0] < x < x_range[1] - 1 and y_range[0] < y < y_range[1] - 1){
                map_costs[floor] = map_cost(node, up_node, edge_cost);
                map_costs[floor+1] = map_cost(node, right_node, edge_cost);
                map_costs[floor+2] = map_cost(node, left_node, edge_cost);
                map_costs[floor+3] = map_cost(node, down_node, edge_cost);
                floor += 4;
            }
            else if (x == x_range[1] - 1 and y == y_range[1] - 1){
                map_costs[floor] = map_cost(node, left_node, edge_cost);
                map_costs[floor+1] = map_cost(node, down_node, edge_cost);
                floor += 2;
             }
            else if (x == x_range[1] - 1 and y_range[0] < y < y_range[1] - 1){
                map_costs[floor] = map_cost(node, up_node, edge_cost);
                map_costs[floor+1] = map_cost(node, left_node, edge_cost);
                map_costs[floor+2] = map_cost(node, down_node, edge_cost);
                floor += 3;
            }
            else if (x_range[0] < x < x_range[1] - 1 and y == y_range[1] - 1){
                map_costs[floor] = map_cost(node, right_node, edge_cost);
                map_costs[floor+1] = map_cost(node, left_node, edge_cost);
                map_costs[floor+2] = map_cost(node, down_node, edge_cost);
                floor +=3;
            }
        }
    }

    int node_map[][];
    int path_map[][];
    for(int i = 0; i< points_num; i++ ){
        for(int j = 0; j < points_num; j++){
            node_map[i][j] = Val;
        }
    }

    for(int i = 0; i< points_num; i++ ){
        for(int j = 0; j < points_num; j++){
            path_map[i][j] = 0;
        }
    }

    set_node_map(points_num, node_map, node_list, map_costs, path_map, edge_cost);

    string start_points = to_string(start_point[0]) + "_" + to_string(start_point[1]);
    string end_points = to_string(start_point[0]) + "_" + to_string(start_point[1]);

    int from_node = node_index(node_list, start_points, points_num);
    int to_node = node_index(node_list, end_points, points_num);
    Floyd_Path floyd_path = Floyd_Path.init(points_num,node_list, node_map, path_map, from_node, to_node);
    floyd_path.find_path();
    string path[] = floyd_path.format_path();
    for(int i=0;i<sizeof(path); i++){
        cout << path[i] << endl;
    }

    return 0;
}