import glfw
import sys

class Controller():
    
    def __init__(self, arm):
        self.camera_angle = 0
        self.dt = 1
        self.angle0 = 0
        self.rotation0 = 0
        self.rotation1 = 0
        self.arm = arm

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
            self.arm.add_to_angle(0.05)
            print("angle+")
        elif key == glfw.KEY_S:
            self.arm.add_to_angle(-0.05)
            print("angle-")

        elif key == glfw.KEY_D:
            self.arm.add_to_arm0_rotation(0.05)
            print("arm0+")
        elif key == glfw.KEY_F:
            self.arm.add_to_arm0_rotation(-0.05)
            print("arm0-")

        elif key == glfw.KEY_Z:
            self.arm.add_to_arm1_rotation(0.05)
            print("arm1+")
        elif key == glfw.KEY_X:
            self.arm.add_to_arm1_rotation(-0.05)
            print("arm1-")

        elif key == glfw.KEY_SPACE:
            pos = self.arm.ball.random_pos()
            self.arm.ball.actualize_img()
            rot = self.arm.get_rotations()
            print("\n \n \n \n \n \n \n \n \n \n")
            print(pos+rot)

        elif key == glfw.KEY_ESCAPE:
            sys.exit()

        else:#action != glfw.PRESS:
            return
