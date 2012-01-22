import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
import bullet
from . import vector3


class Edge(object):
    def __init__(self):
        self.n=[(0, 0, 0), (0, 0, 0)]
        self.v=[(0, 0, 0), (0, 0, 0)]

class ShapeCache(object):
    def __init__(self, s):
        self.m_shapehull=s
        self.m_edges=[]

class VertexArray(object):
    def __init__(self, vertices, indices):
        self.vertices=numpy.array(vertices, 'f')
        self.indices=numpy.array(indices, 'u4')

    def draw(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)
        glDrawElements(GL_TRIANGLES, len(self.indices),
                GL_UNSIGNED_INT, self.indices)
        glDisableClientState(GL_VERTEX_ARRAY)


tex1=numpy.array([1, 0, 0, 0], 'f')
tex2=numpy.array([0, 0, 1, 0], 'f')

print 'create box'
indices = [
        0,1,2,
        3,2,1,
        4,0,6,
        6,0,2,
        5,1,4,
        4,1,0,
        7,3,1,
        7,1,5,
        5,4,7,
        7,4,6,
        7,2,3,
        7,6,2,
            ];

vertices=[
        (1,1,1),
        (-1,1,1),
        (1,-1,1),
        (-1,-1,1),
        (1,1,-1),
        (-1,1,-1),
        (1,-1,-1),
        (-1,-1,-1)];

""" ToDo normal
for i0, i1, i2 in indices:
    v1 = vertices[i0];
    v2 = vertices[i1];
    v3 = vertices[i2];
    normal = vector3.normalize(vector3.cross(
        vector3.sub(v3, v1), 
        vector3.sub(v2, v1)));
    glNormal3f(normal[0], normal[1], normal[2]);
    glVertex3f (v1[0], v1[1], v1[2]);
    glVertex3f (v2[0], v2[1], v2[2]);
    glVertex3f (v3[0], v3[1], v3[2]);
"""
gBox=VertexArray(vertices, indices)


class GL_ShapeDrawer(object):
    def __init__(self):
        # clean-up memory of dynamically created shape hulls
        self.m_shapecaches=[]
        self.m_texturehandle=0
        self.m_textureenabled=False
        self.m_textureinitialized=False
        self.m_vertexArray={}

    def cache(self, cache):
        pass

    def __drawCustomConvexShape(self, m, shape):
        org=(m[12], m[13], m[14]);
        dx=(m[0], m[1], m[2]);
        dy=(m[4], m[5], m[6]);
        # dz=(m[8], m[9], m[10]);
        boxShape = bullet.btBoxShape.downcast(shape);
        halfExtent = boxShape.getHalfExtentsWithMargin();
        dx *= halfExtent[0];
        dy *= halfExtent[1];
        # dz *= halfExtent[2];
        glColor3f(1,1,1);
        glDisable(GL_LIGHTING);
        glLineWidth(2);

        glBegin(GL_LINE_LOOP);
        glDrawVector(org - dx - dy);
        glDrawVector(org - dx + dy);
        glDrawVector(org + dx + dy);
        glDrawVector(org + dx - dy);
        glEnd();

    def __drawBoxShape(self, m, shape):
        org=(m[12], m[13], m[14]);
        dx=(m[0], m[1], m[2]);
        dy=(m[4], m[5], m[6]);
        dz=(m[8], m[9], m[10]);
        boxShape = bullet.btBoxShape.downcast(shape);
        halfExtent = boxShape.getHalfExtentsWithMargin();
        dx *= halfExtent[0];
        dy *= halfExtent[1];
        dz *= halfExtent[2];
        glBegin(GL_LINE_LOOP);
        glDrawVector(org - dx - dy - dz);
        glDrawVector(org + dx - dy - dz);
        glDrawVector(org + dx + dy - dz);
        glDrawVector(org - dx + dy - dz);
        glDrawVector(org - dx + dy + dz);
        glDrawVector(org + dx + dy + dz);
        glDrawVector(org + dx - dy + dz);
        glDrawVector(org - dx - dy + dz);
        glEnd();
        glBegin(GL_LINES);
        glDrawVector(org + dx - dy - dz);
        glDrawVector(org + dx - dy + dz);
        glDrawVector(org + dx + dy - dz);
        glDrawVector(org + dx + dy + dz);
        glDrawVector(org - dx - dy - dz);
        glDrawVector(org - dx + dy - dz);
        glDrawVector(org - dx - dy + dz);
        glDrawVector(org - dx + dy + dz);
        glEnd();

    def __drawScalingShape(self, m, shape, color, debugMode, worldBoundsMin, worldBoundsMax):
        glPushMatrix();
        glMultMatrixf(m);
        scalingShape = bullet.btUniformScalingShape.downcast(shape);
        convexShape = scalingShape.getChildShape();
        scalingFactor = float(scalingShape.getUniformScalingFactor());
        tmpScaling[4][4]=[
                [scalingFactor,0,0,0],
                [0,scalingFactor,0,0],
                [0,0,scalingFactor,0],
                [0,0,0,1]
                ];
        self.drawOpenGL(tmpScaling,convexShape,color,debugMode,worldBoundsMin,worldBoundsMax);
        glPopMatrix();

    def __drawCompoundShape(self, m, shape, color, debugMode, worldBoundsMin, worldBoundsMax):
        glPushMatrix();
        glMultMatrixf(m);
        compoundShape = bullet.btCompoundShape.case(shape);
        for i in range(compoundShape.getNumChildShapes()-1, -1, -1):
            childTrans = compoundShape.getChildTransform(i);
            colShape = compoundShape.getChildShape(i);
            childMat=childTrans.getOpenGLMatrix();
            self.drawOpenGL(childMat,colShape,color,debugMode,worldBoundsMin,worldBoundsMax);
        glPopMatrix();

    def __drawShape(self, shape):
        # you can comment out any of the specific cases, and use the default

        # the benefit of 'default' is that it approximates the actual 
        # collision shape including collision margin
        # int shapetype=m_textureenabled?MAX_BROADPHASE_COLLISION_TYPES:shape.getShapeType();
        shapetype=shape.getShapeType();

        if shapetype== bullet.SPHERE_SHAPE_PROXYTYPE:
            print 'SPHERE_SHAPE_PROXYTYPE'
            sphereShape = bullet.btSphereShape.downcast(shape);
            # radius doesn't include the margin, so draw with margin
            radius = sphereShape.getMargin();
            drawSphere(radius,10,10);
            useWireframeFallback = False;

        elif shapetype== bullet.BOX_SHAPE_PROXYTYPE:
            boxShape = bullet.btBoxShape.downcast(shape);
            halfExtent = boxShape.getHalfExtentsWithMargin();
            glPushMatrix()
            glScalef(halfExtent[0], halfExtent[1], halfExtent[2])
            gBox.draw()
            glPopMatrix()

            useWireframeFallback = False;

        elif shapetype== bullet.STATIC_PLANE_PROXYTYPE:
            print 'STATIC_PLANE_PROXYTYPE'
            staticPlaneShape = bullet.btStaticPlaneShape.downcast(shape);
            planeConst = staticPlaneShape.getPlaneConstant();
            planeNormal = staticPlaneShape.getPlaneNormal();
            planeOrigin = planeNormal * planeConst;
            vec0, vec1=btPlaneSpace1(planeNormal);
            vecLen = 100.0;
            pt0 = planeOrigin + vec0*vecLen;
            pt1 = planeOrigin - vec0*vecLen;
            pt2 = planeOrigin + vec1*vecLen;
            pt3 = planeOrigin - vec1*vecLen;
            glBegin(GL_LINES);
            glVertex3f(pt0[0], pt0[1], pt0[2]);
            glVertex3f(pt1[0], pt1[1], pt1[2]);
            glVertex3f(pt2[0], pt2[1], pt2[2]);
            glVertex3f(pt3[0], pt3[1], pt3[2]);
            glEnd();

        elif shapetype== bullet.MULTI_SPHERE_SHAPE_PROXYTYPE:
            print 'MULTI_SPHERE_SHAPE_PROXYTYPE'
            multiSphereShape = bullet.btMultiSphereShape.downcast(shape);

            childTransform=bullet.btTransform();
            childTransform.setIdentity();

            for i in range(multiSphereShape.getSphereCount()-1, -1, -1):
                sc=bullet.btSphereShape (multiSphereShape.getSphereRadius(i));
                childTransform.setOrigin(multiSphereShape.getSpherePosition(i));
                childMat=childTransform.getOpenGLMatrix();
                self.drawOpenGL(childMat,sc,color,debugMode,worldBoundsMin,worldBoundsMax);

        else:
            print 'other'
            if (shape.isConvex()):
                poly = (shape.isPolyhedral()
                        and bullet.btPolyhedralConvexShape.downcast(shape).getConvexPolyhedron()
                        or 0);
                if (poly):
                    glBegin (GL_TRIANGLES);
                    for i in range(poly.m_faces.size()):
                        centroid=(0,0,0);
                        numVerts = poly.m_faces[i].m_indices.size();
                        if (numVerts>2):
                            v1 = poly.m_vertices[poly.m_faces[i].m_indices[0]];
                            for v in range(poly.m_faces[i].m_indices.size()-2):
                                v2 = poly.m_vertices[poly.m_faces[i].m_indices[v+1]];
                                v3 = poly.m_vertices[poly.m_faces[i].m_indices[v+2]];
                                normal = vector3.normalize(vector3.cross(
                                    vector3.sub(v3, v1), 
                                    vector3.sub(v2, v1)
                                    ));
                                glNormal3f(normal.getX(),normal.getY(),normal.getZ());
                                glVertex3f (v1[0], v1[1], v1[2]);
                                glVertex3f (v2[0], v2[1], v2[2]);
                                glVertex3f (v3[0], v3[1], v3[2]);
                    glEnd ();
                else:
                    sc=self.cache(bullet.btConvexShape.downcast(shape));
                    # glutSolidCube(1.0);
                    hull = sc.m_shapehull

                    if (hull.numTriangles () > 0):
                        index = 0;
                        idx = hull.getIndexPointer();
                        vtx = hull.getVertexPointer();

                        glBegin (GL_TRIANGLES);

                        for i in range(hull.numTriangles()):
                            i1 = index;
                            i2 = index+1;
                            i3 = index+2;
                            index+=3
                            assert(i1 < hull.numIndices () and
                                    i2 < hull.numIndices () and
                                    i3 < hull.numIndices ());

                            index1 = idx[i1];
                            index2 = idx[i2];
                            index3 = idx[i3];
                            assert(index1 < hull.numVertices () and
                                    index2 < hull.numVertices () and
                                    index3 < hull.numVertices ());

                            v1 = vtx[index1];
                            v2 = vtx[index2];
                            v3 = vtx[index3];
                            normal = (v3-v1).cross(v2-v1);
                            normal.normalize ();
                            glNormal3f(normal.getX(),normal.getY(),normal.getZ());
                            glVertex3f (v1.x(), v1.y(), v1.z());
                            glVertex3f (v2.x(), v2.y(), v2.z());
                            glVertex3f (v3.x(), v3.y(), v3.z());

                        glEnd ();

    def drawOpenGL(self, m, shape, color, debugMode, worldBoundsMin, worldBoundsMax):
        if (shape.getShapeType() == bullet.CUSTOM_CONVEX_SHAPE_TYPE):
            self.__drawCustomConvexShape(m, shape)
            return
        if((shape.getShapeType() == bullet.BOX_SHAPE_PROXYTYPE)
                and  (debugMode & bullet.btIDebugDraw.DBG_FastWireframe)):
            self.__drawBoxShape(m, shape)
            return
        if (shape.getShapeType() == bullet.UNIFORM_SCALING_SHAPE_PROXYTYPE):
            self.__drawScalingShape(m, shape, color, debugMode, worldBoundsMin, worldBoundsMax)
            return
        if (shape.getShapeType() == bullet.COMPOUND_SHAPE_PROXYTYPE):
            self.__drawCompoundShape(m, shape, color, debugMode, worldBoundsMin, worldBoundsMax)
            return

        glPushMatrix();
        glMultMatrixf(m);

        if(self.m_textureenabled and (not self.m_textureinitialized)):
            print 'create texture'
            image=[]
            for y in range(256):
                t=y>>4;
                for x in range(256):
                    s=x>>4;
                    b=180;
                    c=b+((s+t&1)&1)*(255-b);
                    image.append(c)
                    image.append(c)
                    image.append(c)
            image=numpy.array(image, numpy.uint8)
            self.m_texturehandle=glGenTextures(1);
            glBindTexture(GL_TEXTURE_2D,self.m_texturehandle);
            glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE);
            #glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_LINEAR);
            #glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR_MIPMAP_LINEAR);
            glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT);
            glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT);
            gluBuild2DMipmaps(GL_TEXTURE_2D,3,256,256,GL_RGB,GL_UNSIGNED_BYTE,image);
            glTexGenfv(GL_S,GL_OBJECT_PLANE, tex1);
            glTexGenfv(GL_T,GL_OBJECT_PLANE, tex2);

        glMatrixMode(GL_TEXTURE);
        glLoadIdentity();
        glScalef(0.025,0.025,0.025);
        glMatrixMode(GL_MODELVIEW);

        glTexGeni(GL_S,GL_TEXTURE_GEN_MODE,GL_OBJECT_LINEAR);
        glTexGeni(GL_T,GL_TEXTURE_GEN_MODE,GL_OBJECT_LINEAR);
        glEnable(GL_TEXTURE_GEN_S);
        glEnable(GL_TEXTURE_GEN_T);
        glEnable(GL_TEXTURE_GEN_R);
        self.m_textureinitialized=True;

        glEnable(GL_COLOR_MATERIAL);
        if(self.m_textureenabled):
            glEnable(GL_TEXTURE_2D);
            glBindTexture(GL_TEXTURE_2D,self.m_texturehandle);
        else:
            glDisable(GL_TEXTURE_2D);

        glColor3f(color[0], color[1], color[2]);

        useWireframeFallback = True;
        if (not (debugMode & bullet.btIDebugDraw.DBG_DrawWireframe)):
            self.__drawShape(shape)

        glNormal3f(0.0, 1.0, 0.0);

        # for polyhedral shapes
        if (debugMode==bullet.btIDebugDraw.DBG_DrawFeaturesText
                and (shape.isPolyhedral())):
            polyshape = bullet.btPolyhedralConvexShape.downcast(shape);
            print 'polyshape'
            glColor3f(1.0, 1.0, 1.0);

        if (shape.isConcave() and not shape.isInfinite()):
            concaveMesh = bullet.btConcaveShape.downcast(shape);
            print 'concaveMesh'
            drawCallback=GlDrawcallback();
            drawCallback.m_wireframe = (debugMode & bullet.btIDebugDraw.DBG_DrawWireframe)!=0;
            concaveMesh.processAllTriangles(drawCallback,worldBoundsMin,worldBoundsMax);

        glPopMatrix();

    def drawShadow(self, m, extrusion, shape, worldBoundsMin, worldBoundsMax):
        #print 'drawShadow'
        pass

    def enableTexture(self, enable):
        p=self.m_textureenabled
        self.m_textureenabled=enable
        return(p)

    def hasTextureEnabled(self):
        return self.m_textureenabled;

    def drawSphere(self, r, lats, longs):
        print 'drawSphere'
        pass

    @staticmethod
    def drawCylinder(self, radius, halfHeight, upAxis):
        pass

    @staticmethod
    def drawCoordSystem(self):
        glBegin(GL_LINES);
        glColor3f(1, 0, 0);
        glVertex3d(0, 0, 0);
        glVertex3d(1, 0, 0);
        glColor3f(0, 1, 0);
        glVertex3d(0, 0, 0);
        glVertex3d(0, 1, 0);
        glColor3f(0, 0, 1);
        glVertex3d(0, 0, 0);
        glVertex3d(0, 0, 1);

