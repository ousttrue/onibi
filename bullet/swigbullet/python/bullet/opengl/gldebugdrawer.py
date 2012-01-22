import bullet


class GLDebugDrawer(bullet.btIDebugDraw):
    def __init__(self):
        bullet.btIDebugDraw.__init__(self)
        self.m_debugMode=0

    def	drawLine(self, start, to, fromColor, toColor):
        pass

    def	drawLine(self, start, to, color):
        pass

    def	drawSphere(self, p, radius, color):
        pass

    def	drawBox(self, boxMin, boxMax, color, alpha):
        pass

    def	drawTriangle(self, a, b, c, color, alpha):
        pass

    def	drawContactPoint(self, PointOnB, normalOnB, distance, lifeTime, color):
        pass

    def	reportErrorWarning(self, warningString):
        pass

    def	draw3dText(self, location, textString):
        pass

    def	setDebugMode(self, debugMode):
        pass

    def getDebugMode(self):
        return self.m_debugMode;

