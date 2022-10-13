

#include <iostream>
#include <string>
#include <map>
#include <list>
#include <map>

using namespace std;

const int max_points = 100;
const int Val = 9999;

struct map_edge_cost{
    string from_node;
    string to_node;
    int cost;
    // map_edge_cost(string from_node, string to_node, int cost){
    //     from_node = from_node;
    //     to_node = to_node;
    //     cost = cost;
    // }
};

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
        void init(int point_nums, string node[],int node_map[][100], int path_map[][100], int from_node_index, int to_node_index){
            point_nums = point_nums;
            node = node;
            node_map = node_map;
            path_map = path_map;
            from_node_index = from_node_index;
            to_node_index = to_node_index;
        }

        void find_path(){
            int i,j,k;
            int tmp;
            for(k=0;k<point_nums;k++){
                for(i=0;i<point_nums;i++){
                    for(j=0;j<point_nums;j++){
                        tmp = node_map[i][k] + node_map[k][j];
                        if(tmp > node_map[i][j]){
                            node_map[i][j] = tmp;
                            path_map[i][j] = path_map[i][k];
                        }
                    }
                }
            }
            cout << "_init_Floyd is end" << endl;
        }

        string * format_path(){
            static string node_list[100];
            int temp_node = from_node_index;
            int goal_node = to_node_index;
            cout << "the shortest path is: " << endl;
            cout << node_map[temp_node][goal_node] << endl;
            node_list[0] = node[temp_node];
            int k = 0;
            while (k < max_points){
                k++;
                int temp_index = path_map[temp_node][goal_node];
                node_list[k] = node[temp_index];
                temp_node = path_map[temp_node][goal_node];
                if(temp_node == goal_node){
                    break;
                }
            }
            return node_list;
        }
};

int node_index(string node[], string s, int point_nums){

    if(point_nums <= 0 ){
        return 0;
    }
    for(int i=0;i<point_nums;i++){
        if(node[i] == s){
            return i;
        }
    }
    return 0;
}

void set_node_map(int points_num, int node_map[][100], string node[], map_edge_cost node_list[], int path_map[][100], int cost_edges){
    if(points_num <= 0){
        return;
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
    map_edge_cost map_costs[1000];
    int points_num = 0;
    int index_counts = 0;
    for(int k=0; k< 10; k++){
        for(int v=0; v<10; v++){
            int x = x_point[k];
            int y = y_point[v];
            string node = to_string(x) + "_" + to_string(y);
            str_node_map.insert(pair<string, x_y>(node, xy(x, y)));
            node_list[index_counts] = node;
            index_counts += 1;
        }
    }
    points_num = index_counts;

    int index_count = 0;
    for(int k=0; k< 10; k++){
        for(int v=0; v<10; v++){
            int x = x_point[k];
            int y = y_point[v];
            string node = to_string(x) + "_" + to_string(y);
            string right_node = to_string(x + 1) + "_" + to_string(y);
            string up_node = to_string(x) + "_" + to_string(y + 1);
            string left_node = to_string(x-1) + "_" + to_string(y);
            string down_node = to_string(x) + "_" + to_string(y-1);
            if (x == x_range[0] && y == y_range[0]){
                map_costs[index_count] = {node, up_node, edge_cost};
                map_costs[index_count+1] = {node, right_node, edge_cost};
                index_count += 2;
            }
            else if(x == x_range[0] && y_range[0] < y && y < y_range[1] - 1){
                map_costs[index_count] = {node, up_node, edge_cost};
                map_costs[index_count+1] = {node, right_node, edge_cost};
                map_costs[index_count+2] = {node, down_node, edge_cost};
                index_count += 3;
            }
            else if (x_range[0] < x && x < x_range[1] - 1 && y == y_range[0]){
                map_costs[index_count] = {node, up_node, edge_cost};
                map_costs[index_count+1] = {node, right_node, edge_cost};
                map_costs[index_count+2] = {node, left_node, edge_cost};
                index_count += 3;
            }
            else if (x_range[0] < x && x < x_range[1] - 1 && y_range[0] < y && y < y_range[1] - 1){
                map_costs[index_count] = {node, up_node, edge_cost};
                map_costs[index_count+1] = {node, right_node, edge_cost};
                map_costs[index_count+2] = {node, left_node, edge_cost};
                map_costs[index_count+3] = {node, down_node, edge_cost};
                index_count += 4;
            }
            else if (x == x_range[1] - 1 && y == y_range[1] - 1){
                map_costs[index_count] = {node, left_node, edge_cost};
                map_costs[index_count+1] = {node, down_node, edge_cost};
                index_count += 2;
             }
            else if (x == x_range[1] - 1 && y_range[0] < y && y < y_range[1] - 1){
                map_costs[index_count] = {node, up_node, edge_cost};
                map_costs[index_count+1] = {node, left_node, edge_cost};
                map_costs[index_count+2] = {node, down_node, edge_cost};
                index_count += 3;
            }
            else if (x_range[0] < x && x < x_range[1] - 1 && y == y_range[1] - 1){
                map_costs[index_count] = {node, right_node, edge_cost};
                map_costs[index_count+1] = {node, left_node, edge_cost};
                map_costs[index_count+2] = {node, down_node, edge_cost};
                index_count +=3;
            }
        }
    }

    int node_map[100][100];
    int path_map[100][100];
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
    string end_points = to_string(goal_point[0]) + "_" + to_string(goal_point[1]);

    int from_node = node_index(node_list, start_points, points_num);
    int to_node = node_index(node_list, end_points, points_num);
    Floyd_Path floyd_path;
    floyd_path.init(points_num,node_list, node_map, path_map, from_node, to_node);
    floyd_path.find_path();
    string *path;
    path = floyd_path.format_path();
    for(int i=0; i<100; i++){
        cout << "path" << endl;
        cout << *path << endl;
    }

    return 0;
}