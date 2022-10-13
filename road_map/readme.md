1. config为配置文件，其中，xrange为x的坐标范围，yrange为y的坐标范围；start_point为起，goal_point为终点，edge_cost为每条边的代价；
2. output_path.json为输出起点到终点的路径；
3. road_map_path为主程序，构建地图矩阵，采用简单的floyd算法计算路径；