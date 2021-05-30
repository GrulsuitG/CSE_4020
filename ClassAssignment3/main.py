import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sys
import copy

lastx = 320
lasty = 320

azimuth = 45
elevation = 45
distance = 45

zoom = 10

atx=0
aty=0

viewing = True
lclick = False
rclick = False
move = False
wire = False
bvh = False

offsetlist = None
channel = None
motion = None
frames =0
f = 0
def render():
    global offsetlist, frames, f, channel
    # enable depth test (we'll see details later)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
    if wire:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    else:
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

     # persepctive
    if viewing :
        gluPerspective(90, 1, 0.1, 100)
        glTranslatef(-atx, -aty, 0)
        gluLookAt(distance*np.cos(np.radians(elevation))*np.cos(np.radians(azimuth)),
              distance*np.sin(np.radians(elevation)),
              distance*np.cos(np.radians(elevation))*np.sin(np.radians(azimuth)),
              0,0 ,0, 0,1,0)
    #orthogonal
    else:
        glOrtho(-100,100, -100,100, -100,100)
        glTranslatef(-atx, -aty, 0)
        glScalef(100/distance, 100/distance, 100/distance) 
    #  rotate "camera" position (right-multiply the current matrix by viewing matrix)
    #  try to change parameters
        gluLookAt(np.cos(np.radians(elevation))*np.cos(np.radians(azimuth)),
              np.sin(np.radians(elevation)),
              np.cos(np.radians(elevation))*np.sin(np.radians(azimuth)),
              0,0 ,0, 0,1,0)

    draw_grid()

    glEnable(GL_LIGHTING)   #comment: no lighting
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
  
    # light position
    glPushMatrix()
    lightPos0 = (1.,1.,-1.,0.)   # try to change 4th element to 0. or 1.
    lightPos1 = (-1., 1., -1., 0.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)
    glPopMatrix()

   # light intensity for each color channel
    lightColor1 = (1.,1.,1.,1.)
    lightColor2 = (.0, .0, .0, .1)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor1)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor1)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor2)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor2)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)


    #  material reflectance for each color channel
    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    if bvh :
        curDepth = -1
        glColor3ub(100,100,100)
        push = 0
        pop = 0
        glScalef(0.1, 0.1, 0.1)
        n = 3
        c = 0
        for i in offsetlist :
            #  print(i)
            if curDepth <= i[0] :
                #  print("push!")
                push +=1
                curDepth = i[0]
                glPushMatrix()
                drawLine(i)
                glPushMatrix()
                push+=1
                if i[0] == 0 :
                    glTranslatef(float(motion[f][0]), float(motion[f][1]), float(motion[f][2]))
                else :
                    glTranslatef(i[1],i[2],i[3])
                
                if move :
                    rotate(channel[c][0], channel[c][1], channel[c][2], float(motion[f][n]), float(motion[f][n+1]), float(motion[f][n+2]))
            elif i[0] < curDepth :
                while i[0] <= curDepth :
                    glPopMatrix()
                    glPopMatrix()
                    curDepth -= 1
                    pop+=2
                    #  print("pop!")
                glPushMatrix()
                push+=1
                drawLine(i)
                glTranslatef(i[1],i[2],i[3])
                glPushMatrix()
                push+=1
                #  drawBox()
                if move :
                    rotate(channel[c][0], channel[c][1], channel[c][2], float(motion[f][n]), float(motion[f][n+1]), float(motion[f][n+2]))
        while push > pop :
            glPopMatrix()
            pop +=1
            #  print("pop!")
        if move :
            n += 3
            c += 1
    #  print("end!")
    if move :
        f = (f+1) % frames
    glDisable(GL_LIGHTING)
  
def draw_obj():
    global gVertex
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    v = gVertex
    glNormalPointer(GL_FLOAT, 6*v.itemsize, v)
    glVertexPointer(3, GL_FLOAT, 6*v.itemsize, ctypes.c_void_p(v.ctypes.data + 3*v.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(v.size/6))

def rotate(first, second, third, rot1, rot2, rot3):
    if first.startswith("X")  :
        glRotatef(rot1, 1 , 0 , 0)
    elif first.startswith("Y") :
        glRotatef(rot1, 0, 1, 0)
    elif first.startswith("Z") :
        glRotatef(rot1, 0, 0, 1)
    else :
        print("somting error!")
        return;
    if second.startswith("X") :
        glRotatef(rot2, 1 , 0 , 0)
    elif second.startswith("Y") :
        glRotatef(rot2, 0, 1, 0)
    elif second.startswith("Z") :
        glRotatef(rot2, 0, 0, 1)
    else :
        print("somting error!")
        return;
    if third.startswith("X") :
        glRotatef(rot3, 1 , 0 , 0)
    elif third.startswith("Y") :
        glRotatef(rot3, 0, 1, 0)
    elif third.startswith("Z") :
        glRotatef(rot3, 0, 0, 1)
    else :
        print("somting error!")
        return;

    #  print(first, second, third)

def drawBox():
    glBegin(GL_QUADS)
    glVertex3fv(np.array([0.01,0.01,0.]))
    glVertex3fv(np.array([-0.01,0.01,0.]))
    glVertex3fv(np.array([-0.01,-0.01,0.]))
    glVertex3fv(np.array([0.01,-0.01,0.]))
    glEnd()

def drawLine(offset):
    glBegin(GL_LINES)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([offset[1],offset[2],offset[3]]))
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global viewing, wire, hierarchi, move, f
    # Toggle Persepective / orthogonal
    if action == glfw.PRESS:
        if key == glfw.KEY_V:
            viewing = not viewing
        if key == glfw.KEY_Z:
            wire = not wire
        if key == glfw.KEY_SPACE :
            move = not move
            f = 0

        
 
def mouse_callback(window, button, action, mods):
    global azimuth, lclick, rclick
    global xpos, ypos
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            lclick = True
        if action == glfw.RELEASE:  
            lclick = False 
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            rclick = True
        if action == glfw.RELEASE:  
            rclick = False 

    
def cursor_callback(window, x, y):
    global azimuth, elevation, lclick, rclick
    global lastx, lasty, atx, aty
   
    # orbit
    if lclick:  
        xoff = x - lastx
        yoff = lasty - y
        azimuth += xoff*0.1
        elevation -= yoff*0.1
    # panning
    elif rclick:  
        atxoff = lastx - x
        atyoff = y - lasty
        atx += atxoff*0.01
        aty += atyoff*0.01

    lastx =x
    lasty =y 
    

def scroll_callback(window, x, y):
    global distance
    # zooming
    if distance-y < 0 or distance-y >90:
        distance
    else:
        distance -= y 

def drop_callback(window, paths):
    global lines, bvh, offsetlist,channel, motion, frames
    path = ""+paths[0]
    name = path.split('/')[-1]
    if name.endswith(".bvh") :
        bvh = True 
        jointlist = []
        offsetlist = []
        channel = []
        motion = []
        jointNum = 0
        depth = -1
        with open(path, "r") as f:
            lines = f.readlines()
            for l in lines:
                split = l.split()
                if split[0] == "HIERARCHY" :
                    continue
                if split[0] == "Frames:" :
                    frames = int(split[1]);
                elif split[0] == "Frame" :
                    FPS = int(1/float(split[2]))
                elif split[0] == "ROOT" or split[0] == "JOINT" :
                    jointlist.append(split[1])
                    jointNum +=1
                elif split[0] == "{" :
                    depth += 1
                elif split[0] == "}" :
                    depth -= 1
                elif split[0] == "OFFSET" :
                    offsetlist.append([depth, float(split[1]), float(split[2]), float(split[3])])
                elif split[0] == "CHANNELS" :
                    if split[1] == '6' :
                        channel.append([split[5],split[6],split[7]])
                    elif split[1] == '3' :
                        channel.append([split[2],split[3],split[4]])
                elif split[0] == "End" :
                    continue
                elif split[0] == "MOTION" :
                    continue
                else:
                    motion.append(split)
        #  for i in motion :
        #      print(i[0])
        #  print(channel)
        
        print("File name: " + name)
        print("Number of frames: ", frames )
        print("FPS: ", FPS)
        print("Number of joints (including root): ", jointNum)
        print("List of all joint names: ", jointlist)
    else :
        print("Wrong file format!")
        
   
def draw_grid():
    rows = 10
    cloumns =10
    
   
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    for i in range(-rows+1, rows): 
      glVertex3f(i, -2, -rows);
      glVertex3f(i, -2, rows);
    
    glColor3ub(0,255, 0)
    for i in range(-cloumns+1, cloumns):
      glVertex3f(-cloumns, -2, i);
      glVertex3f(cloumns, -2, i);
    
    glEnd()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'ClassAssignment3', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_drop_callback(window, drop_callback)
    
    
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
        

    glfw.terminate()



if __name__ == "__main__":
    main()

