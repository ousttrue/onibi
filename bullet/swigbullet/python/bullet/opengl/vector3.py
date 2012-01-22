import math


def cross(l, r):
    return (l[1]*r[2]-l[2]*r[1], l[2]*r[0]-l[0]*r[2], l[0]*r[1]-l[1]*r[0])

def length(v):
    return math.sqrt(length2(v))

def length2(v):
    return v[0]*v[0]+v[1]*v[1]+v[2]*v[2]

def add(l, r):
    return (l[0]+r[0], l[1]+r[1], l[2]+r[2])

def sub(l, r):
    return (l[0]-r[0], l[1]-r[1], l[2]-r[2])

def normalize(v):
    f=1.0/length(v)
    return (v[0]*f, v[1]*f, v[2]*f)

def mul(v, s):
    return (v[0]*s, v[1]*s, v[2]*s)
