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
obj = False
wire = False
hierarchi = False

varr =[]
narr =[]
faces = []
gVertex = None

handle = None
frame = None
wheel = None
gear = None
pedal = None
t =0
def render():
    global gVertex,handle,frame,wheel,gear,pedal, t
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
    
    if hierarchi :
        glPushMatrix()
        gVertex = frame
        glPushMatrix()
        glTranslate(0, 4 , 40-3*t) 
        objectColor = (1.,.0,.0,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

        draw_obj()

        glPushMatrix()
        gVertex =handle
        glTranslatef(0.1, 1.7, -2.0)
        
        objectColor = (0.5,0.5,0.5,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
        draw_obj()
        #front wheel
        glPushMatrix()
        gVertex = wheel
        glTranslatef(-0.15, -3.8, -1.1)
        glRotatef(-200*t, 0 , 0 ,0)
        draw_obj()
        glPopMatrix()
        glPopMatrix()

        #rear wheel
        glPushMatrix()
        glTranslatef(-0.07, -2.1, 4.)
        glRotatef(-200*t, 0 , 0 ,0)
        draw_obj() 

        glPopMatrix()
        
        glPushMatrix()
        gVertex = gear
        glTranslatef(0.1, -2, 0.9)
        glRotatef(-100*t, 0, 0, 0)
        draw_obj()

        #right pedal
        glPushMatrix()
        gVertex = pedal
        glTranslatef(0.85, -0.58, 0.64)
        glRotatef(100*t, 0, 0, 0)
        draw_obj()
        glPopMatrix()
        
        #left pedal
        glPushMatrix()
        glTranslatef(-1.1, 0.58, -0.64)
        glRotatef(100*t, 0, 0, 0)
        draw_obj()
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()
        t+=0.01
    else :
        glPushMatrix()
        if obj:
            draw_obj()

        glPopMatrix()
    
    glDisable(GL_LIGHTING)
  
def draw_obj():
    global gVertex
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    v = gVertex
    glNormalPointer(GL_FLOAT, 6*v.itemsize, v)
    glVertexPointer(3, GL_FLOAT, 6*v.itemsize, ctypes.c_void_p(v.ctypes.data + 3*v.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(v.size/6))

def key_callback(window, key, scancode, action, mods):
   
    global viewing, wire, hierarchi, obj
    global handle, wheel, frame, gear, pedal, t
    # Toggle Persepective / orthogonal
    if action == glfw.PRESS:
        if key == glfw.KEY_V:
            viewing = not viewing
        if key == glfw.KEY_Z:
            wire = not wire
        if key == glfw.KEY_H:
            if hierarchi:
                obj = False
                hierarchi = False
            else :
                open_obj("handle.obj")
                handle = copy.deepcopy(gVertex) 
                open_obj("wheel.obj")

                wheel = copy.deepcopy(gVertex)
                open_obj("frame.obj")
                frame = copy.deepcopy(gVertex) 
                open_obj("gear.obj")
                gear = copy.deepcopy(gVertex)
                open_obj("pedal.obj")
                pedal = copy.deepcopy(gVertex)
                t = 0
                hierarchi = True

 
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
    path = ""+paths[0]
    face3, face4, facemore = open_obj(path)


    print("File name: " + path)
    print("Total number of faces: ", face3+face4+facemore)
    print("Number of faces with 3 vertices: ", face3)
    print("Number of faces with 4 vertices: ", face4)
    print("Number of faces with more than 4 vertices: ", facemore)


def triangulation():
    global faces
    triangle = []
    polygon =[]
    for f in faces:
        if len(f.split()) == 3:
            triangle.append(f)
        else:
            polygon.append(f)
    for f in polygon:
        for i in range(1,len(f.split())-1):
            temp = f.split()
            face = [str(temp[0]),str(temp[i]), str(temp[i+1])]
            string = ' '.join(face)
            triangle.append(string)
    return triangle

def createVertex(faces):
    v = np.zeros((len(faces)*6,3),'float32')
    i =0
    vetex = 0
    normal =0
    for face in faces:
        for f in face.split():
            if '//' in f:
                vertex = int(f.split('//')[0])-1
                normal = int(f.split('//')[1])-1
            elif '/'in f:
                fs = f.split('/')
                if len(fs) == 2:
                    vertex = int(fs[0])-1
                    normal = int(fs[0])-1
                else :
                    vertex = int(fs[0])-1
                    normal = int(fs[2])-1
            else :
                vertex = int(f.split()[0])-1
                normal = int(f.split()[0])-1
            v[i] = narr[normal]
            v[i+1] = varr[vertex]
            i+=2
    return v

def draw_grid():
    rows = 10
    cloumns =10
    
   
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

def open_obj(filename):
    global varr, gVertex, narr, faces, obj
    face3 =0
    face4 =0
    facemore = 0
    varr = []
    narr = []
    faces = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            split = line.split()
            if len(split) ==0 :
                continue
            elif split[0] == "vt":
                continue
            elif split[0] == "vn":
                try:
                    temp = (float(split[1]),float(split[2]),float(split[3]))
                    narr.append(temp)
                except ValueError:
                    pass
            elif split[0] == "v":
                try:
                    temp = (float(split[1]),float(split[2]),float(split[3]))
                    varr.append(temp)
                except ValueError:
                    pass
            elif split[0] == "f":
                face = len(split)-1
                faces.append(line[2:])
                if face == 3:
                    face3+=1
                elif face == 4:
                    face4+=1
                elif face >4:
                    facemore+=1
            else:
                continue
    
    obj = True
 
    varr = np.array(varr)
    narr = np.array(narr)
    if len(narr) == 0:
        narr = varr 
    if face4 >0 or facemore >0:
        faces = triangulation()
    gVertex = createVertex(faces)

    return face3, face4, facemore

def main():
    global xpos, ypos
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'ClassAssignment2', None,None)
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

