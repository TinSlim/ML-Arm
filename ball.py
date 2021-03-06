import modulo.transformations as tr
import modulo.basic_shapes as bs
import modulo.scene_graph as sg
import modulo.easy_shaders as es

import random

class Ball:

    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.ponderator = 1
        self.catched = False
        self.distance = (self.x**2 + self.y**2 +self.z**2)**(1/2)
        
    def actualize_distance(self):
        self.distance = (self.x**2 + self.y**2 +self.z**2)**(1/2)

    def setX(self,new_x):
        self.x = new_x
    
    def setY(self,new_y):
        self.y = new_y

    def setZ(self,new_z):
        self.z = new_z
    
    def create_parts(self):
        gpu_cube = es.toGPUShape(bs.createColorNormalsCube(1, 1, 0))
        
        node_cube = sg.SceneGraphNode("cube")
        node_cube.transform =([tr.translate(1,1,0),tr.scale(0.5,0.5,0.5)]) 
        node_cube.childs += [gpu_cube]
        
        
        node_all = sg.SceneGraphNode("all")
        node_all.childs += [node_cube]
        
        self.big_node = node_all
    
    def move(self,x,y,z):
        self.x = self.x + x
        self.y = self.y + y
        self.z = self.z + z
        cube = sg.findNode(self.big_node, "cube")
        cube.transform =([tr.translate(self.x,self.y,self.z),tr.scale(0.5,0.5,0.5)]) 
    
    def translate(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        cube = sg.findNode(self.big_node, "cube")
        cube.transform =([tr.translate(self.x,self.y,self.z),tr.scale(0.5,0.5,0.5)]) 

    def random_pos(self):
        x_r = 10
        y_r = 10
        z_r = 10
        cantidad = 0
        while ((x_r**2) + (y_r**2) + (z_r**2))**(1/2) >10.5 or z_r<0:
            a =random.choice([True, False])
            b = random.choice([True, False])
            x_r = round(random.random() * self.ponderator,3)
            y_r = round(random.random() * self.ponderator,3)
            z_r = round(random.random() * self.ponderator,3)
            if a and b:
                x_r = x_r * -1
                y_r = y_r * -1
            elif a:
                x_r = x_r * -1
            else:
                y_r = y_r *-1

            if cantidad == 3:
                self.ponderator = 1
            cantidad+=1
        
        print(x_r,",",y_r,",",z_r,",")
        self.ponderator+=0.1
        self.x = x_r
        self.y = y_r
        self.z = z_r
        return f"{x_r},{y_r},{z_r},"
        
    def actualize_img(self):
        cube = sg.findNode(self.big_node, "cube")
        cube.transform =([tr.translate(self.x,self.y,self.z),tr.scale(0.5,0.5,0.5)]) 