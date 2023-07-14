from math import *
def maxmin(_min,_max,v):
    if v>_max: return _max
    if v<_min: return _min
    return v
def tupleToVector3(tup):
    if type(tup)==type(float()) or type(tup)==type(int()):
        return Vector3(tup)
    if len(tup)==2: return Vector3(tup[0],tup[1]) 
    return Vector3(tup[0],tup[1],tup[2])
class Vector3:
    def _abs(self):
        # return absolute absolute value of X Y  and Z 
        return Vector3(fabs(self.x),fabs(self.y),fabs(self.z))
    def __repr__(self):
        return "[ "+str(self.x)+" , "+str(self.y)+" , "+str(self.z)+" ]"
    def __init__(self,x=0.0,y=0.0,z=0.0):
        self.x,self.y,self.z =x,y,z
    def __str__(self):
        return "[ "+str(self.x)+" , "+str(self.y)+" , "+str(self.z)+" ]"
    def __add__(self,u):
        # u must be a Vector3, interger or a float/int
        if type(u)==type(self):
            return Vector3(self.x+u.x,self.y+u.y,self.z+u.z)
        return Vector3(self.x+u,self.y+u,self.z+u)
    def __sub__(self,u):
        # u must be a Vector3, interger or a float/int
        if type(u)==type(self):
            return Vector3(self.x-u.x,self.y-u.y,self.z-u.z)
        return Vector3(self.x-u,self.y-u,self.z-u)
    def __truediv__(self,u):
        # u must be a Vector3, interger or a float/int
        if type(u)==type(self):
            return Vector3(self.x/u.x,self.y/u.y,self.z/u.z)
        return Vector3(self.x/u,self.y/u,self.z/u)
    def __mul__(self,u):
        # u must be a Vector3, interger or a float/int
        if type(u)==type(self):
            return Vector3(self.x*u.x,self.y*u.y,self.z*u.z)
        return Vector3(self.x*u,self.y*u,self.z*u)
    def frac(self):
        return Vector3(self.x%1,self.y%1,self.z%1)
    def rotate(self,rotation):
        # rotation is Vector3 of degrees angles [X,Y,Z]  
        #https://en.wikipedia.org/wiki/Rotation_matrix
        rot = rotation * (pi/180)
        rcos = Vector3(cos(rot.x),cos(rot.y),cos(rot.z))
        rsin = Vector3(sin(rot.x),sin(rot.y),sin(rot.z))
        return Vector3(rcos.z*rcos.y*self.x+self.y*(rcos.z*rsin.y*rsin.x-rsin.z*rcos.x)+self.z*(rcos.z*rsin.y*rcos.x+rsin.z*rsin.x),rsin.z*rcos.y*self.x+self.y*(rsin.z*rsin.y*rsin.x+rcos.z*rcos.x)+self.z*(rsin.z*rsin.y*rcos.x-rcos.z*rsin.x),-rsin.y*self.x+self.y*(rcos.y*rsin.x)+self.z*(rcos.y*rcos.x))
    def normalize(self):
        # normalize the vector (self**2 =1)
        d = sqrt(self.x**2+self.y**2+self.z**2)
        return Vector3(self.x/d,self.y/d,self.z/d)
    def _fabs(self):
        return Vector3(fabs(self.x),fabs(self.y),fabs(self.z))
    def cross(self,u):
        return Vector3((self.y*u.z)-(self.z*u.y),(self.z*u.x)-(self.x*u.z),(self.x*u.y)-(self.y*u.x))
    def dotProduct(self,u,isAbs=False):
        #return the dot product of 2 vector3
        if not isAbs:
            return self.x*u.x+self.y*u.y+self.z*u.z
        return fabs(self.x*u.x)+fabs(self.y*u.y)+fabs(self.z*u.z)
    def _sum(self):
        # return the sum of x,y and z
        return self.x+self.y+self.z
    def distance(self,u,doSqrt):
        # return the distance between two points
        # doSqrt=True -> use square root 
        # else return square distance
        if doSqrt:
            return sqrt(((self-u)*(self-u))._sum())
        return ((self-u)*(self-u))._sum()
    def color(self,hexa=False):
        # convert Vecotr3 to a tuple (r,g,b) where r g b are x, y and z
        r,g,b = self.x,self.y,self.z
        if(self.x>255): r=255
        if(self.y>255): g=255
        if(self.z>255): b=255
        if(self.x<0): r=0
        if(self.y<0): g=0
        if(self.z<0): b=0

        if hexa: 
            r=int(r<17)*'0'+hex(int(r))[2:]
            g=int(g<17)*'0'+hex(int(g))[2:]
            b=int(b<17)*'0'+hex(int(b))[2:]
            return ('#'+r+g+b)[:7]
        return (int(r),int(g),int(b))
#int(r<17)*'0'
#int(g<17)*'
#int(b<17)*'0'
    def lookAt(self,target):
        n=(target-self).normalize()
        return Vector3((1-(asin(n.y)/pi))*180,atan2(n.x,n.z)/(2*pi)*90)