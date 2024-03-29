# -*- coding: utf-8 -*-
import sys
import pygame
import simulation_simple
#使用pygame之前必须初始化
pygame.init()
#设置主屏窗口 ；设置全屏格式：flags=pygame.FULLSCREEN
screen = pygame.display.set_mode(size=(800, 800))
#设置窗口标题
pygame.display.set_caption('万邑通')
screen.fill('black')
#创建一个 50*50 的图像,并优化显示
face = pygame.Surface((10,10),flags=pygame.HWSURFACE)
#填充颜色
face.fill(color='pink')
map_path = u'F:/QP/wanyitong插件/DEBR2_001_10.7.8allcost1.json'
_, g_coords, g_point_coord, storage_points, station_points, _, path_points = simulation_simple.preprocess_point_data(map_path)

while True:
    # 循环获取事件，监听事件
    for event in pygame.event.get():
        # 判断用户是否点了关闭按钮
        if event.type == pygame.QUIT:
            #卸载所有模块
            pygame.quit()
            #终止程序
            sys.exit()
    # 将绘制的图像添加到主屏幕上，(100,100)是位置坐标，显示屏的左上角为坐标系的(0,0)原点
    for pt in g_coords:
        screen.blit(face, pt)
    pygame.display.flip() #更新屏幕内容

