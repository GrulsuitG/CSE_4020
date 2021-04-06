import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

lastx = 320
lasty = 320

azimuth = 45
elevation = 45
distance = 20

atx=0
aty=0

viewing = True
lclick = False
rclick = False
def render():
    # enable depth test (we'll see details later)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()

    # use orthogonal projection (we'll see details later)
    #  glOrtho(-1,1, -1,1, -1,1)
    if viewing :
        gluPerspective(90, 1, 0.1, 100)
    else:
      glOrtho(-10,10, -10,10, -10,10)
        
    # rotate "camera" position (right-multiply the current matrix by viewing matrix)
    # try to change parameters
    gluLookAt(distance*np.cos(np.radians(elevation))*np.cos(np.radians(azimuth)),
              distance*np.sin(np.radians(elevation)),
              distance*np.cos(np.radians(elevation))*np.sin(np.radians(azimuth)),
              atx,aty,0, 0,1,0)    
     
    draw_grid()

def key_callback(window, key, scancode, action, mods):
    #  global gCamAng, gCamHeight
    #  if action==glfw.PRESS or action==glfw.REPEAT:
    #      if key==glfw.KEY_1:
    #          gCamAng += np.radians(-10)
    #      elif key==glfw.KEY_3:
    #          gCamAng += np.radians(10)
    #      elif key==glfw.KEY_2:
    #          gCamHeight += .1
    #      elif key==glfw.KEY_W:
    #          gCamHeight += -.1
    global viewing
    if action == glfw.PRESS and key ==glfw.KEY_V:
        viewing = not viewing

 
def mouse_callback(window, button, action, mods):
    global azimuth, lclick
    global xpos, ypos
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            lclick = True
        if action == glfw.RELEASE:  
            lclick = False 
    if button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            rclick = True
        if action == glfw.RELEASE:  
            rclick = False 

    
def cursor_callback(window, x, y):
    global azimuth, elevation, lclick, rclick
    global lastx, lasty, atx, aty
   
    if lclick:  
        xoff = x - lastx
        yoff = lasty - y
        azimuth += xoff*0.1
        elevation -= yoff*0.1
    if rclick:  
        atxoff = lastx - x
        atyoff = y - lasty
        atx = atxoff
        aty = atyoff

    lastx =x
    lasty =y 


def scroll_callback(window, x, y):
    global distance
    
    if distance-y < 0 or distance-y >90:
        distance
    else:
        distance -= y 
   
 
def draw_grid():
    rows = 10
    cloumns =10
    
    glColor3ub(255,255,255)
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    for i in range(-rows+1, rows): 
      glVertex3f(i, 0, -rows);
      glVertex3f(i, 0, rows);
    
    glColor3ub(0,255, 0)
    for i in range(-cloumns+1, cloumns):
      glVertex3f(-cloumns, 0, i);
      glVertex3f(cloumns, 0, i);
    
    glEnd()


def main():
    global xpos, ypos
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'ClassAssignment1', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
   
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        xpos, ypos =  glfw.get_cursor_pos(window)
        glfw.swap_buffers(window)
        

    glfw.terminate()



if __name__ == "__main__":
    main()

