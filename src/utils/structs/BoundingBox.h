#ifndef CarlaBoundingBox
#define CarlaBoundingBox

struct BoundingBox {
    double x1, y1; // coordinates of the left bottom corner
    double x2, y2; // coordinates of the left top corner
    double x3, y3; // coordinates of the right top corner
    double x4, y4; // coordinates of the right bottom corner
};

#endif