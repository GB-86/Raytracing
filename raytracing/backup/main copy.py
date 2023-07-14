from math import *
from vector3 import *
from mesh import *
from PIL import Image
import os
imageWidth = 1080
imageHeight = 720
finalImage = Image.new(mode='RGB',size=(imageWidth,imageHeight),color=(0,0,0))
scene =[Sphere(Vector3(-1.9, -2.8, 18.5),2.2,Vector3(100, 100, 100),0.9),Sphere(Vector3(2, -3, 14),2,Vector3(220, 220, 220),0.9),Mesh(Vector3(0, 0, 15),Vector3(0,0,0),Vector3(1,1,1),[Vector3(-5, -5, 8),Vector3(-5, 5, 8),Vector3(5, -5, 8),Vector3(5, 5, 8),Vector3(-5, -5, -5),Vector3(-5, 5, -5),Vector3(5, 5, -5),Vector3(5, -5, -5)],
[Triangle(0,1,2,Vector3(220, 220, 220),0.95,Vector3(0,0,-1)),Triangle(1,2,3,Vector3(220, 220, 220),0.95,Vector3(0,0,1)),Triangle(0,2,7,Vector3(255, 186, 121),0,Vector3(0,1,0)),Triangle(0,4,7,Vector3(255, 186, 121),0,Vector3(0,-1,0)),
Triangle(0,4,5,Vector3(242, 94, 106),0,Vector3(1,0,0)),Triangle(0,1,5,Vector3(242, 94, 106),0,Vector3(-1,0,0)),Triangle(3,7,2,Vector3(87, 94, 242),0,Vector3(-1,0,0)),Triangle(7,3,6,Vector3(87, 94, 242),0,Vector3(-1,0,0)),
Triangle(1,3,5,Vector3(220, 220, 220),0,Vector3(0,1,0)),Triangle(3,6,5,Vector3(220, 220, 220),0,Vector3(0,1,0))])]
scene_Materials=[]
scene=[Sphere(Vector3(0,-1,0),5,Vector3(100,100,100),0.9)]
skybox=None
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
    normal = (hitPoint-sphere.center).normalize()
    return (distance,normal,hitPoint)
def intersectWithFace(rayOrigin,rayDirection,face,maxDistance):
    # calculate the normal of the plane
    v1= face.v2-face.v1
    if face.normal is None:
        v2=face.v3-face.v1
        normal = v1.cross(v2).normalize()
    else: normal = face.normal
    Vector pvec = rayDirection.Cross(edge2);
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
    return (distance,normal,hitPoint)      
mainLight = Light(Vector3(0,2,18),Vector3(1,1,1))
m=0
def isLightVisible(pos,dir,length):
    length=sqrt(length)
    for i in scene:
        if type(i)==type(Sphere(0,0,0,0)):
            _intersectResult = intersectWithSphere(pos,dir,i,length)
            if _intersectResult!=False:
                return False
        else:
            for j in i.triangles:
                _intersectResult =intersectWithFace(pos,dir,Triangle((i.vertices[j.v1].rotate(i.rotation)+i.position)*i.scale,(i.vertices[j.v2].rotate(i.rotation)+i.position)*i.scale,(i.vertices[j.v3].rotate(i.rotation)+i.position)*i.scale,None,None,j.normal),length)
                if _intersectResult!=False:
                    return False
    return True

def calculateLight(hitInfo,_light,face,rDir,rPos,l):
    _color=face.color
    if face.reflectionStrenght!=0 and l!=0:
        r= ray(hitInfo[2],(rDir-(hitInfo[1]*((rDir.dotProduct(hitInfo[1],False))*2))).normalize(),l-1,1000,True)
        _color=(r*face.reflectionStrenght)+_color*(1-face.reflectionStrenght)
    if isLightVisible(hitInfo[2],(_light.position-hitInfo[2]).normalize(),((_light.position-hitInfo[2])*(_light.position-hitInfo[2]))._sum()): a=1
    else: a=0.7

    if type(face)==type(Sphere):
        if (_light.position-hitInfo[2]).dotProduct(hitInfo[1],False)<0: a = 0.7
        return _color*(hitInfo[2]-_light.position).normalize().dotProduct(hitInfo[1],True)
    return _color*(hitInfo[2]-_light.position).normalize().dotProduct(hitInfo[1],True)*a
def ray(rayOrigin,rayDirection,reflectionLeft=5,length=100,doLightCal=True):
    global meshes
    length= 1000
    _obj=Sphere(Vector3(0,0,0),Vector3(0,0,0),None,Vector3(0,0,0))
    for i in scene:
        if type(i)==type(Sphere(0,0,0,0)):
            _intersectResult = intersectWithSphere(rayOrigin,rayDirection,i,length)
            if _intersectResult!=False:
                length =_intersectResult[0]
                intersectResult = _intersectResult
                _obj=i
        else:
            for j in i.triangles:
                #if j.normal is not None and (i.vertices[j.v1].rotate(i.rotation)+i.position-rayOrigin).dotProduct((i.vertices[j.v3]+j.normal).rotate(i.rotation)-i.vertices[j.v3].rotate(i.rotation),False)<0:
                #_intersectResult = intersectWithFace(rayOrigin,rayDirection,Triangle(i.vertices[j.v1].rotate(i.rotation)+i.position,i.vertices[j.v2].rotate(i.rotation)+i.position,i.vertices[j.v3].rotate(i.rotation)+i.position,None,(i.vertices[j.v3]+j.normal).rotate(i.rotation)-i.vertices[j.v3].rotate(i.rotation)),length)
                _intersectResult = intersectWithFace(rayOrigin,rayDirection,Triangle((i.vertices[j.v1].rotate(i.rotation)+i.position)*i.scale,(i.vertices[j.v2].rotate(i.rotation)+i.position)*i.scale,(i.vertices[j.v3].rotate(i.rotation)+i.position)*i.scale,None,None,j.normal),length)
                if _intersectResult!=False:
                    length =_intersectResult[0]
                    intersectResult = _intersectResult
                    _obj=j
    if doLightCal and _obj.color is not None:
        return calculateLight(intersectResult,mainLight,_obj,rayDirection,rayOrigin,reflectionLeft)
    if skybox!=None:
        c=skybox.getpixel((abs(int((atan2(rayDirection.x,rayDirection.z)/(2*pi)+0.5)*skybox.size[0]))-1,skybox.size[1]-abs(int((rayDirection.y*0.5+0.5)*skybox.size[1]))-1))
        return Vector3(c[0],c[1],c[2])
    if rayDirection.y<-0.1: return Vector3(100,100,100)
    if rayDirection.y<0.1: return Vector3(125+250*rayDirection.y,125+250*rayDirection.y,175+750*rayDirection.y)
    return Vector3(150,150,250)
    # this will change to add a skybox.
def loadScene(path):
    directories=os.listdir(path)
    global skybox
    print(directories)
    if 'skybox.png' in directories: skybox=Image.open(path+'/skybox.png','r')
def render():

    camera = (Vector3(0,0,-18),Vector3(0,0,0)) # [position,rotation] 
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
            


            r=ray(camera[0],rayDirection.rotate(camera[1]),3,100,True)

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
    