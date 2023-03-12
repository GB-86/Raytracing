from math import *
class Vector3:
    def _abs(self):
        # return absolute absolute value of X Y  and Z 
        return Vector3(fabs(self.x),fabs(self.y),fabs(self.z))
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
    def __mul__(self,u):
        # u must be a Vector3, interger or a float/int
        if type(u)==type(self):
            return Vector3(self.x*u.x,self.y*u.y,self.z*u.z)
        return Vector3(self.x*u,self.y*u,self.z*u)
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
    def cross(self,u):
        return Vector3((self.y*u.z)-(self.z*u.y),(self.z*u.x)-(self.x*u.z),(self.x*u.y)-(self.y*u.x))
    def dotProduct(self,u,isAbs):
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
            return sqrt(sum((self-u)*(self-u)))
        return ((self-u)*(self-u))._sum()
    def color(self):
        # convert Vecotr3 to a tuple (r,g,b) where r g b are x, y and z
        r,g,b = self.x,self.y,self.z
        if(self.x>255): r=255
        if(self.y>255): g=255
        if(self.z>255): b=255
        if(self.x<0): r=0
        if(self.y<0): g=0
        if(self.z<0): b=0
        return (int(r),int(g),int(b))
