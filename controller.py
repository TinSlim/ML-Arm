import glfw

class Controller():
    
    def __init__(self, arm, clf):
        self.camera_angle = 0
        self.dt = 1
        self.angle0 = 0
        self.rotation0 = 0
        self.rotation1 = 0
        self.arm = arm
        self.clf = clf

    def rotate_camera_angle(self,x):
        self.camera_angle += x

    def set_dt(self,new_dt):
        self.dt = new_dt     
    
    def auto_action(self,r0_r1_ang):
        if r0_r1_ang[0]:
            self.arm.add_to_arm0_rotation(0.05)
        else:
            self.arm.add_to_arm0_rotation(-0.05)

        if r0_r1_ang[1]:
            self.arm.add_to_arm1_rotation(0.05)
        else:
            self.arm.add_to_arm1_rotation(-0.05)

        if r0_r1_ang[2]:
            self.arm.add_to_angle(0.05)
        else:
            self.arm.add_to_angle(-0.05)
        
    def on_key(self,window, key, scancode, action, mods):
        if key == glfw.KEY_P:
            x = self.arm.ball.x
            y = self.arm.ball.y
            z = self.arm.ball.z
            angle = self.arm.angle
            rot0 = self.arm.arm0_rotation
            rot1 = self.arm.arm1_rotation

            prediction = self.clf.predict([[x,y,z,angle,rot0,rot1]])[0]
            print(prediction)
            switcher = {
                0: [True,True,True],
                1: [False,True,True],
                2: [False,False,True],
                3: [True,False,True],
                4: [True,True,False],
                5: [False,True,False],
                6: [False,False,False],
                7: [True,False,False]
            }
            self.auto_action(switcher[prediction])

        elif key == glfw.KEY_L:
            x = self.arm.ball.x
            y = self.arm.ball.y
            z = self.arm.ball.z
            angle = round(self.arm.angle,3)
            rot0 = round(self.arm.arm0_rotation,3)
            rot1 = round(self.arm.arm1_rotation,3)
            print(f"{x},{y},{z},{angle},{rot0},{rot1},")

        elif key == glfw.KEY_LEFT:
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
