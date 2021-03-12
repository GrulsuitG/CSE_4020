import numpy as np
import glfw
from OpenGL.GL import *

input_key = 3

def render():
    vx = np.cos(np.arange(0, 2*np.pi, np.pi/6))
    vy = np.sin(np.arange(0, 2*np.pi, np.pi/6))
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINE_LOOP)
    for i in range(0,12):
        glVertex2f(vx[i],vy[i])
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(0,0)
    glVertex2f(vx[input_key],vy[input_key])
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global input_key
    if key in range(49,58):
        input_key = 51-key
    elif key == glfw.KEY_0:
        input_key = 5
    elif key == glfw.KEY_Q:
        input_key = 4
    elif key == glfw.KEY_W:
        input_key = 3
   
def main():
    if not glfw.init():
        return

    window = glfw.create_window(480,480,"2016025205", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.set_key_callback(window, key_callback)

    glfw.make_context_current(window)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render()

        glfw.swap_buffers(window)

glfw.terminate()

if __name__ == "__main__":
    main()
