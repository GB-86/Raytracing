from math import *
from vector3 import *

class Mesh:
    def __init__(self,position,rotation,scale,vertices,triangles):
        self.vertices,self.triangles,self.position,self.rotation,self.scale= vertices,triangles,position,rotation,scale
class Triangle:
    def __init__(self,v1,v2,v3,color,reflectionStrenght,normal=None):
        self.v1,self.v2,self.v3,self.color,self.reflectionStrenght,self.normal =v1,v2,v3,color,reflectionStrenght,normal
class Sphere:
    def __init__(self,center,radius,color,reflectionStrenght):
        self.center,self.radius,self.color,self.reflectionStrenght= center,radius,color,reflectionStrenght
class Light:
    def __init__(self,position,color):
        self.position,self.color = position,color

class Material:
    def __init__(self,albedo,normal,roughness,metallic):
        self.albedo=albedo
def loadfile(path):
    ''' 
    path : str
    return : Mesh
    read and convert an obj file into a Mesh.
    '''
    if path.split('.')[0].lower() in ['obj'] ==False: raise ValueError('unsupported file type')
    file=open(path,'rb')
    lines=file.readlines()
    vertices=[]
    normals=[]
    faces=[]
    color=Vector3(100,100,100)
    for line in lines:
        try:
            l=line.decode()
            if l!='' and l[0]!='#':
                _l=l.split(' ')
                if _l[0]=='v': vertices.append(Vector3(float(_l[1]),float(_l[2]),float(_l[3])))
                elif _l[0]=='vn': normals.append(Vector3(float(_l[1]),float(_l[2]),float(_l[3])))
                elif _l[0]=='f':
                    v=[]
                    for i in _l:
                        v.append(i.split('/'))
                    if len(_l)==4:
                        faces.append(Triangle(int(v[1][0])-1,int(v[2][0])-1,int(v[3][0])-1,color,0,(normals[int(v[1][2])]+normals[int(v[2][2])]+normals[int(v[3][2])])*(1/3)))
                    elif len(_l)==5:
                        print((normals[int(v[1][2])]+normals[int(v[2][2])]+normals[int(v[3][2])])*(1/3))
                        faces.append(Triangle(int(v[1][0])-1,int(v[2][0])-1,int(v[3][0])-1,color,0,(normals[int(v[1][2])]+normals[int(v[2][2])]+normals[int(v[3][2])])*(1/3)))
                        if v[4][2][:-2]=='\n': v[4][2]=v[4][2][-2:]
                        faces.append(Triangle(int(v[4][0])-1,int(v[1][0])-1,int(v[3][0])-1,color,0,(normals[int(v[4][2])]+normals[int(v[1][2])]+normals[int(v[3][2])])*(1/3)))
        except: continue
    return Mesh(Vector3(0,0,0),Vector3(0,0,0),Vector3(1,1,1),vertices,faces)
