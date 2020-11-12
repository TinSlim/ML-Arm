import glfw

class controller():
    
    def on_key(self,window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return
    
        elif key == glfw.KEY_ESCAPE:
            sys.exit()