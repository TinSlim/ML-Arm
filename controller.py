import glfw
import sys

class Controller():
    
    def __init__(self):
        self.camera_angle = 0
        self.dt = 1
        self.angle0 = 0
        self.rotation0 = 0
        self.rotation1 = 0

    def rotate_camera_angle(self,x):
        self.camera_angle += x

    def set_dt(self,new_dt):
        self.dt = new_dt     
            
    def on_key(self,window, key, scancode, action, mods):
        if key == glfw.KEY_LEFT:
            self.rotate_camera_angle(-2 * self.dt)
        
        elif key == glfw.KEY_RIGHT:
            self.rotate_camera_angle(2 * self.dt)

        elif key == glfw.KEY_A:
            self.angle0 += 0.05
        elif key == glfw.KEY_S:
            self.angle0 -= 0.05

        elif key == glfw.KEY_D:
            self.rotation0 += 0.05
        elif key == glfw.KEY_F:
            self.rotation0 -= 0.05

        elif key == glfw.KEY_Z:
            self.rotation1 += 0.05
        elif key == glfw.KEY_X:
            self.rotation1 -= 0.05

        elif key == glfw.KEY_ESCAPE:
            sys.exit()

        else:#action != glfw.PRESS:
            return
