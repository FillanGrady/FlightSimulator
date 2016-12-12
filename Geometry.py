__author__ = 'fillan'
import math
import copy


class Point:
    def __init__(self, x, y, z):  # three points
        self.x = x
        self.y = y
        self.z = z

    def multiply(self, matrix):  # one matrix
        m = matrix.Array
        x = m[0][0] * self.x + m[0][1] * self.y + m[0][2] * self.z  # (x, y)
        y = m[1][0] * self.x + m[1][1] * self.y + m[1][2] * self.z
        z = m[2][0] * self.x + m[2][1] * self.y + m[2][2] * self.z
        self.x = x
        self.y = y
        self.z = z

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def subtract(self, v):  # Vector
        self.x = self.x - v.x
        self.y = self.y - v.y
        self.z = self.z - v.z

    @staticmethod
    def average(point_list):  # list of points
        x = 0
        y = 0
        z = 0
        for i in point_list:
            x += i.x
            y += i.y
            z += i.z
        return Point(x / len(point_list), y / len(point_list), z / len(point_list))

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"


class Vector(Point):
    def __init__(self):
        pass

    def create_from_points(self, p1, p2):  # two points
        self.x = p1.x - p2.x
        self.y = p1.y - p2.y
        self.z = p1.z - p2.z
        
    def create_from_space(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    @staticmethod
    def cross(a, b):  # Two vectors
        x = a.y * b.z - a.z * b.y
        y = a.z * b.x - a.x * b.z
        z = a.x * b.y - a.y * b.x
        v = Vector()
        v.create_from_space(x, y, z)
        return v
    
    @staticmethod
    def dot(a, b):
        return (a.x * b.x) + (a.y * b.y) + (a.z * b.z)
    
    def normalize(self):
        m = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        self.x /= m
        self.y /= m
        self.z /= m


class Surface:
    Center = None
    Color = None
    oPList = None
    Normal = None

    def __init__(self, point_first, point_second, point_third, center):
        # four Points, a tuple, an object, and another point
        self.Center = center
        self.pointList = []
        self.indexList = []
        self.pointList.append(copy.deepcopy(point_first))
        self.pointList.append(copy.deepcopy(point_second))
        self.pointList.append(copy.deepcopy(point_third))
        
    def set_color(self, color, light_source):
        self.find_normal()
        light_vector = Vector()
        light_vector.create_from_points(light_source, self.Center)
        light_vector.normalize()
        gradient = 50 * Vector.dot(light_vector, self.Normal)
        self.Color = [color[0] + gradient, color[1] + gradient, color[2] + gradient]
        for i in range(0, 3):
            if self.Color[i] < 0:
                self.Color[i] = 0
            if self.Color[i] > 255:
                self.Color[i] = 255
                
    def create_object_point_list(self, list):  # Object's list of points
        self.oPList = list
        
    def convert_to_index(self, index):  # list of three ints
        self.pointList = []
        self.indexList = index
        
    def find_normal(self):
        v1 = Vector()
        v1.create_from_points(self.oPList[self.indexList[0]], self.oPList[self.indexList[1]])
        v2 = Vector()
        v2.create_from_points(self.oPList[self.indexList[1]], self.oPList[self.indexList[2]])
        self.Normal = Vector.cross(v1, v2)
        vector_to_center = Vector()
        vector_to_center.create_from_points(self.oPList[self.indexList[1]], self.Center)
        if Vector.dot(vector_to_center, self.Normal) < 0:
            self.Normal = Vector.cross(v2, v1)
        self.Normal.normalize()
        
    def calculate_distance(self):
        l = []
        for i in self.indexList:
            l.append(self.oPList[i])
        return Point.average(l).magnitude()


class Quaternion:
    def __init__(self, w, x, y, z):  # four doubles
        self.w = w  # real coordinate
        self.x = x
        self.y = y
        self.z = z

    def multiply(self, m):  # one quaternion
        self.w = self.w * m.w - self.x * m.x - self.y * m.y - self.z * m.z
        self.x = self.w * m.x + self.x * m.w + self.y * m.z - self.z * m.y
        self.y = self.w * m.y - self.x * m.z + self.y * m.w + self.z * m.x
        self.z = self.w * m.z + self.x * m.y - self.y * m.x + self.z * m.w

    def normalize(self):
        magnitude = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)
        if math.fabs(magnitude - 1) > .05:
            self.x /= magnitude
            self.y /= magnitude
            self.z /= magnitude
            self.w /= magnitude

    def opposite(self):
        return Quaternion(-self.w, self.x, self.y, self.z)

    def __str__(self):
        r = ""
        r += "w=" + str(self.w) + "\n"
        r += "x=" + str(self.x) + "\n"
        r += "y=" + str(self.y) + "\n"
        r += "z=" + str(self.z) + "\n"
        r += "-------------\n"


class Matrix:
    def __init__(self, q):  # Quaternion
        col_1 = []
        col_1.append(1 - 2 * q.y * q.y - 2 * q.z * q.z)  # 1-2y^2-2z^2
        col_1.append(2 * q.x * q.y + 2 * q.w * q.z)  # 2xy+2zw
        col_1.append(2 * q.x * q.z - 2 * q.w * q.y)  # 2xz-2yw
        col_2 = []
        col_2.append(2 * q.x * q.y - 2 * q.w * q.z)  # 2xy-2zw
        col_2.append(1 - 2 * q.x * q.x - 2 * q.z * q.z)  # 1-2x^2-2z^2
        col_2.append(2 * q.y * q.z + 2 * q.w * q.x)  # 2yz+2xw
        col_3 = []
        col_3.append(2 * q.x * q.z + 2 * q.w * q.y)  # 2xz+2yw
        col_3.append(2 * q.y * q.z - 2 * q.w * q.x)  # 2yz-2xw
        col_3.append(1 - 2 * q.x * q.x - 2 * q.y * q.y)  # 1-2x^2-2y^2
        self.Array = [col_1, col_2, col_3]

    def __str__(self):
        s = self.Array
        r = ""
        r += str(s[0][0]) + "  " + str(s[1][0]) + "  " + str(s[2][0]) + "\n"
        r += str(s[0][1]) + "  " + str(s[1][1]) + "  " + str(s[2][1]) + "\n"
        r += str(s[0][2]) + "  " + str(s[1][2]) + "  " + str(s[2][2]) + "\n"
        r += "------------------\n"


class Object:
    pointList = []

    def __init__(self):
        self.modelSpace = []
        self.Distance = 0
        self.Center = Point(0, 0, 0)

    def convert_to_index(self):
        self.pointList = []
        for i in self.modelSpace:
            indexList = []
            for j in i.pointList:
                found = False
                for k in range(len(self.pointList)):
                    p = self.pointList[k]
                    if p.x == j.x and p.y == j.y and p.z == j.z:
                        found = True
                        indexList.append(k)
                if not found:
                    self.pointList.append(copy.deepcopy(j))
                    indexList.append(len(self.pointList) - 1)
            i.convert_to_index(indexList)

    def sort(self):
        for i in range(1, len(self.modelSpace) - 1):  # One iteration of bubble sort
            distance_a = self.modelSpace[i].calculate_distance()
            distance_b = self.modelSpace[i + 1].calculate_distance()
            if distance_a < distance_b:
                self.modelSpace[i], self.modelSpace[i + 1] = self.modelSpace[i + 1], self.modelSpace[i]


class Cube(Object):
    def __init__(self, p, s, color, light_source):  # Two points and a tuple
        Object.__init__(self)
        self.drawBoth = False
        p111 = Point(p.x, p.y, p.z)
        p112 = Point(p.x, p.y, p.z + s.z)
        p121 = Point(p.x, p.y + s.y, p.z)
        p122 = Point(p.x, p.y + s.y, p.z + s.z)
        p211 = Point(p.x + s.x, p.y, p.z)
        p212 = Point(p.x + s.x, p.y, p.z + s.z)
        p221 = Point(p.x + s.x, p.y + s.y, p.z)
        p222 = Point(p.x + s.x, p.y + s.y, p.z + s.z)
        self.Center = Point(p.x + (s.x / 2), p.y + (s.y / 2), p.z + (s.z / 2))
        self.modelSpace.append(Surface(p111, p112, p121, self.Center))  # Left
        self.modelSpace.append(Surface(p112, p121, p122, self.Center))
        self.modelSpace.append(Surface(p211, p212, p221, self.Center))  # Right
        self.modelSpace.append(Surface(p212, p221, p222, self.Center))
        self.modelSpace.append(Surface(p111, p112, p211, self.Center))  # Top
        self.modelSpace.append(Surface(p112, p211, p212, self.Center))
        self.modelSpace.append(Surface(p121, p122, p221, self.Center))  # Bottom
        self.modelSpace.append(Surface(p122, p221, p222, self.Center))
        self.modelSpace.append(Surface(p111, p121, p211, self.Center))  # Back
        self.modelSpace.append(Surface(p121, p211, p221, self.Center))
        self.modelSpace.append(Surface(p112, p122, p212, self.Center))  # Front
        self.modelSpace.append(Surface(p122, p212, p222, self.Center))
        self.convert_to_index()
        for i in self.modelSpace:
            i.create_object_point_list(self.pointList)
            i.set_color(color, light_source)

    def calculate_distance(self):  # One point
        return math.pow(self.Center.x, 2) + math.pow(self.Center.y, 2) + math.pow(self.Center.z, 2)

    def __str__(self):
        return "Cube"


class Ground(Object):
    def __init__(self, light_source):
        Object.__init__(self)
        self.drawBoth = True
        self.Center = Point(0, 100, 0)
        for i in range(-600, 600, 400):
            for j in range(-600, 600, 400):
                p11 = Point(i, 100, j)
                p12 = Point(i + 200, 110, j)
                p13 = Point(i + 400, 100, j)
                p21 = Point(i, 110, j + 200)
                p22 = Point(i + 200, 120, j + 200)
                p23 = Point(i + 400, 110, j + 200)
                p31 = Point(i, 100, j + 400)
                p32 = Point(i + 200, 110, j + 400)
                p33 = Point(i + 400, 100, j + 400)
                self.modelSpace.append(Surface(p11, p12, p21, self.Center))
                self.modelSpace.append(Surface(p22, p12, p21, self.Center))
                self.modelSpace.append(Surface(p21, p22, p31, self.Center))
                self.modelSpace.append(Surface(p32, p22, p31, self.Center))
                self.modelSpace.append(Surface(p12, p13, p22, self.Center))
                self.modelSpace.append(Surface(p23, p13, p22, self.Center))
                self.modelSpace.append(Surface(p22, p23, p32, self.Center))
                self.modelSpace.append(Surface(p33, p23, p32, self.Center))
        self.convert_to_index()
        for i in self.modelSpace:
            i.create_object_point_list(self.pointList)
            i.set_color((0, 220, 50), light_source)

    def __str__(self):
        return "Ground"


class Keyboard():
    def __init__(self):
        self.rDown = False
        self.lDown = False
        self.uDown = False
        self.dDown = False
        self.twoDown = False
        self.oneDown = False