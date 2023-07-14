from math import *
from vector3 import *
from mesh import *
from PIL import Image
from random import random
import os
imageWidth = 1080*2
imageHeight = 630*2
finalImage = Image.new(mode='RGB',size=(imageWidth,imageHeight),color=(0,0,0))
scene_Materials=[Material('materials/albedo.png','materials/normal.png',0.0,0.0),Material('materials/albedo.png',None,0.0,0.0),Material(Vector3(200,200,200),None,0.0,0.9),Material(Vector3(200,200,200),None,0.0,0.0)]
lights = [Light(Vector3(5,10,30),Vector3(1,1,1),230)]
scene=[loadfile('scene/cube.obj'),Sphere(Vector3(-13,7,15),7,2)]
skybox=None
def uvToVector3(texture,uv,doInterpolate=False):
    uv=Vector3(uv.x%1,uv.y%1)
    ts=texture.size
    tc=(ts[0]*uv.x,ts[1]*uv.y)
    pc=(maxmin(0,ts[0]-1,int(tc[0])),maxmin(0,ts[1]-1,int(tc[1])))
    x,y=tc[0]%1,tc[1]%1
    c3 = tupleToVector3(texture.getpixel(pc))
    if doInterpolate==False: return c3
    if abs(x-0.5)<0.001 and abs(y-0.5): return c3
    of=[1,1]
    if x<0.5:
        of[0]=-1
        c2=tupleToVector3(texture.getpixel((maxmin(0,ts[0]-1,pc[0]-1),pc[1])))
    else: c2=tupleToVector3(texture.getpixel((maxmin(0,ts[0]-1,pc[0]+1),pc[1])))
    if y<0.5:  
        of[1]=-1
        c1=tupleToVector3(texture.getpixel((pc[0],maxmin(0,ts[1]-1,pc[1]-1))))
    else: c1=tupleToVector3(texture.getpixel((pc[0],maxmin(0,ts[1]-1,pc[1]+1))))
    c0=tupleToVector3(texture.getpixel((maxmin(0,ts[0]-1,pc[0]+of[0]),maxmin(0,ts[1]-1,pc[1]+of[1]))))
    a=tc[0]%1
    b=tc[1]%1
    return c0+(c1-c0)*a+(c2+(c3-c2)*a-(c0+(c1-c0)*a))*b
def intersectWithSphere(rayOrigin,rayDirection,sphere,maxDistance):
    origin = rayOrigin-sphere.center
    b = 2*origin.dotProduct(rayDirection,False)
    c = origin.dotProduct(origin,False)-(sphere.radius**2)
    d = (b**2)-(4*c)
    if d<0.001:
        return False
    distance = (-b-sqrt(abs(d)))/(2)
    if distance>maxDistance or distance<0.01:
        return False
    hitPoint = (rayDirection*distance)+rayOrigin
    normal = (hitPoint-sphere.center)*(1/(sphere.radius))
    uv=Vector3(abs(atan2(normal.x,normal.z)/(2*pi)+0.5),1-asin(normal.y)/pi+0.5)
    return (distance,normal,hitPoint,uv)
def intersectWithFace(rayOrigin,rayDirection,face,maxDistance):
    uv=Vector3()
    v1= face.v2-face.v1
    v2=face.v3-face.v1
    #print((face.v1,face.v2,face.v3))
    if face.normal is None:
        normal = v1.cross(v2).normalize()
    else: normal = face.normal
    #if (rayDirection).dotProduct(normal,False)>=0: return False
    Not = normal.dotProduct(rayDirection,False)
    if fabs(Not)<0.001:
        # the Ray is parallel to the plane so it would never intersect
        return False
    d = face.v1.dotProduct(normal,False)
    distance = (d-normal.dotProduct(rayOrigin,False))/Not
    if distance<0.01 or distance>maxDistance:
        # check if the hit point is behind the rayOrigin or if the hit point if too far
        return False
    hitPoint = rayOrigin+(rayDirection*distance)
    
        
    if normal.dotProduct((v1.cross(hitPoint-face.v1)),False)<0 or normal.dotProduct(((face.v3-face.v2).cross(hitPoint-face.v2)),False)<0 or normal.dotProduct(((face.v1-face.v3).cross(hitPoint-face.v3)),False)<0:
        return False
    if face.uv!=None:
        v0 = face.v2 - face.v1
        v1 = face.v3 - face.v1
        v2 = hitPoint - face.v1
        d00 = v0.dotProduct(v0)
        d01 = v0.dotProduct(v1)
        d11 = v1.dotProduct(v1)
        d20 = v2.dotProduct(v0)
        d21 = v2.dotProduct(v1)
        denom = d00 * d11 - d01 * d01
        v = (d11 * d20 - d01 * d21) / denom
        w = (d00 * d21 - d01 * d20) / denom
        u = 1.0 - v - w
        uv=(face.uv[0]*u+face.uv[1]*v+face.uv[2]*w).frac()

    return (distance,normal,hitPoint,uv)     
    
m=0
def isLightVisible(pos,dir,length):
    for i in scene:
        if type(i)==type(Sphere(0,0)):
            _intersectResult = intersectWithSphere(pos,dir,i,length)
            if _intersectResult!=False:
                return False
        else:
            for j in i.triangles:
                _intersectResult =intersectWithFace(pos,dir,Triangle((i.vertices[j.v1].rotate(i.rotation)+i.position)*i.scale,(i.vertices[j.v2].rotate(i.rotation)+i.position)*i.scale,(i.vertices[j.v3].rotate(i.rotation)+i.position)*i.scale,None,j.normal),length)
                if _intersectResult!=False:
                    return False
    return True

def calculateLight(hitInfo,lights,face,material,rDir,rPos,l,_scene):
    uv=hitInfo[3]
    #return Vector3(255,0,0)
    #return Vector3(255*uv.x,255*uv.y,0)
    incomingLight=Vector3()
    if type(material.albedo)!=type(Vector3()): albedo=uvToVector3(material.albedo,uv,False)
    else: albedo=material.albedo
    if type(material.roughness)!=type(float()): roughness=uvToVector3(material.roughness,uv,True).x*1/255
    else: roughness=material.roughness
    if type(material.metallic)!=type(float()): 
        metallic=uvToVector3(material.metallic,uv,True).x*0.25/65535
    else: metallic=material.metallic
    normal=hitInfo[1]
    if material.normal!=None:
        n=(uvToVector3(material.normal,uv,True)/256)*2-Vector3(1,1,1)
        normal=n.normalize()
    resultColor=albedo
    
    for i in lights:
        intersectPointToLight=(i.position-hitInfo[2]).normalize()
        _intersectPointToLight=(hitInfo[2]-i.position).distance(Vector3(),True)
        if (normal.dotProduct(intersectPointToLight,False)<=0 or isLightVisible(hitInfo[2],intersectPointToLight,_intersectPointToLight)==False)==False:
            d=normal.dotProduct(intersectPointToLight)
            incomingLight+= i.color/ (_intersectPointToLight*4 * pi )*i.intensity*int(d>0)*d
        if metallic!=0:
            rct=Vector3(0,0,0)
        for i in range(int(20*roughness+1)):
            rn=normal+Vector3(0.5,0.5,0.5)*(roughness*(random()-0.5))
            relfectedDir=(rDir-(rn*((rDir.dotProduct(rn,False))*2))).normalize()
            rct+=ray(hitInfo[2],relfectedDir,l-1,1000,True,_scene.copy())
        relfectedColor=rct*(1/int(20*roughness+1))
        return relfectedColor*metallic+resultColor*incomingLight*(1-metallic)
    return resultColor*incomingLight+Vector3(0.125,0.125,0.125)-random()*0.25
    
def ray(rayOrigin,rayDirection,reflectionLeft=5,length=100,doLightCal=True,_scene=[]):
    global meshes
    length= 1000
    _obj=None
    _mat=None
    for i in _scene:
        mat=scene_Materials[i.materialIndex]
        if type(i)==type(Sphere(0,0)):
            _intersectResult = intersectWithSphere(rayOrigin,rayDirection,i,length)
            if _intersectResult!=False:
                length =_intersectResult[0]
                intersectResult = _intersectResult
                _obj=i
                _mat=mat
        else:
            for j in i.triangles:
                a=(i.vertices[j.v2]+j.normal).rotate(i.rotation)
                a1=i.vertices[j.v2].rotate(i.rotation)
                n=a-a1
                _intersectResult = intersectWithFace(rayOrigin,rayDirection,Triangle((i.vertices[j.v1].rotate(i.rotation))*i.scale+i.position,(i.vertices[j.v2].rotate(i.rotation))*i.scale+i.position,(i.vertices[j.v3].rotate(i.rotation))*i.scale+i.position,j.uv,j.normal),length)
                if _intersectResult!=False:
                    length =_intersectResult[0]
                    intersectResult = _intersectResult
                    _obj=j
                    _mat=mat
    
    if doLightCal and _obj is not None:
        #return Vector3(255,0,0)
        return calculateLight(intersectResult,lights.copy(),_obj,_mat,rayDirection,rayOrigin,reflectionLeft,_scene)
    if skybox!=None:
        return Vector3()
        return uvToVector3(skybox,Vector3(abs(atan2(rayDirection.x,rayDirection.z)/(2*pi)+0.5),1-asin(rayDirection.y)/pi+0.5))
    if rayDirection.y<-0.1: return Vector3(100,100,100)
    if rayDirection.y<0.1: return Vector3(125+250*rayDirection.y,125+250*rayDirection.y,175+750*rayDirection.y)
def loadScene(path):
    directories=os.listdir(path)
    global skybox
    if 'skybox.jpg' in directories: skybox=Image.open(path+'/skybox.png','r')
camera = [Vector3(5,6.5,5),Vector3(-20,0,0)]
camera=[Vector3(0,10,0),Vector3(20,0)]
print(camera[1])
def render(): 
    fov = 90
    finish=0
    angleK = pi/fov
    xScreen=0
    yScreen=0
    _x=-fov/2
    xReset=_x
    _y=((imageHeight*fov*0.5)/imageHeight)/2
    xStep=fov/(imageWidth)
    yStep=fov/((imageHeight)*(imageWidth/imageHeight))
    while yScreen<(imageHeight):
        while xScreen<imageWidth:
            rayDirection=Vector3(_x*angleK,_y*angleK,1).normalize()
            r=ray(camera[0],rayDirection.rotate(camera[1]),3,100,True,scene.copy())
            finalImage.putpixel((xScreen,yScreen),r.color())
            xScreen+=1
            _x+=xStep
        _x=xReset
        xScreen=0
        yScreen+=1
        _y-=yStep
        if int((yScreen/imageHeight)*100)!=finish:
            os.system("clear")
            finish=int((yScreen/imageHeight)*100)
            print('['+'#'*finish+'·'*(100-finish)+']  '+str(finish)+"%"+" done")
if __name__ == "__main__":
    loadScene('scene')
    render()
    finalImage.show()
    finalImage.save("img.png")
    