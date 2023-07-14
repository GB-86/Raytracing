from math import *
from vector3 import *
from PIL import Image
class Mesh:
    def __init__(self,position,rotation,scale,vertices,triangles,materialIndex=0):
        self.vertices,self.triangles,self.position,self.rotation,self.scale,self.materialIndex= vertices,triangles,position,rotation,scale,materialIndex
class Triangle:
    def __init__(self,v1,v2,v3,uv=(Vector3(),Vector3(),Vector3()),normal=None):
        self.v1,self.v2,self.v3,self.normal,self.uv=v1,v2,v3,normal,uv
class Sphere:
    def __init__(self,center,radius,materialIndex=0):
        self.center,self.radius,self.materialIndex= center,radius,materialIndex
class Light:
    def __init__(self,position,color,intensity):
        self.position,self.color,self.intensity = position,color,intensity

class Material:
    def __init__(self,albedo,normal,roughness,metallic):
        self.albedo,self.normal,self.roughness,self.metallic=albedo,normal,roughness,metallic
        if type(self.albedo)!=type(Vector3()): self.albedo=Image.open(self.albedo,'r')
        if self.normal!=None: self.normal=Image.open(self.normal,'r')
        if type(self.roughness)!=type(float()): self.roughness=Image.open(self.roughness,'r')
        if type(self.metallic)!=type(float()): self.metallic=Image.open(self.metallic,'r')
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
    uvs=[]
    color=Vector3(100,100,100)
    for line in lines:
        #try:
        l=line.decode()
        if l!='' and l[0]!='#':
            _l=l.split(' ')
            if _l[0]=='v': vertices.append(Vector3(float(_l[1]),float(_l[2]),float(_l[3])))
            elif _l[0]=='vn': normals.append(Vector3(float(_l[1]),float(_l[2]),float(_l[3])))
            elif _l[0]=='vt': uvs.append(Vector3(float(_l[1]),float(_l[2])))
            elif _l[0]=='f': #and v[1][0]!=0:
                #print(uvs)
                v=[]
                for i in _l:
                    v.append(i.split('/'))
                if len(_l)==4:
                    faces.append(Triangle(int(v[1][0])-1,int(v[2][0])-1,int(v[3][0])-1,(uvs[int(v[1][1])-1],uvs[int(v[2][1])-1],uvs[int(v[3][1])-1]),normals[int(v[1][2])-1]))
                    print((uvs[int(v[1][1])-1],uvs[int(v[2][1])-1],uvs[int(v[3][1])-1]))
                elif len(_l)==5:
                    print((normals[int(v[1][2])]+normals[int(v[2][2])]+normals[int(v[3][2])])*(1/3))
                    faces.append(Triangle(int(v[1][0])-1,int(v[2][0])-1,int(v[3][0])-1,color,0,(normals[int(v[1][2])]+normals[int(v[2][2])]+normals[int(v[3][2])])*(1/3)))
                    if v[4][2][:-2]=='\n': v[4][2]=v[4][2][-2:]
                    faces.append(Triangle(int(v[4][0])-1,int(v[1][0])-1,int(v[3][0])-1,color,0,(normals[int(v[4][2])]+normals[int(v[1][2])]+normals[int(v[3][2])])*(1/3)))
        #except: continue
    print(uvs)
    return Mesh(Vector3(0,-5,10),Vector3(0,0,0),Vector3(1000,50,1000),vertices,faces,1)
#loadfile('scene/cube.obj')