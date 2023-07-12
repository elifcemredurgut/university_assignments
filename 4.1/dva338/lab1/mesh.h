#ifndef _MESH_H_
#define _MESH_H_

#include "algebra.h"

typedef struct _Triangle {
	int vInds[3]; //vertex indices
} Triangle;

typedef struct _Mesh { 
	int nv;				
	Vector *vertices;
	Vector *vnorms;
	int nt;				
	Triangle *triangles;
	struct _Mesh *next;
	Vector rotation;
	Vector translation;
	Vector scaling;
		
	unsigned int vbo, ibo, vao; // OpenGL handles for rendering
} Mesh;

void insertModel(Mesh ** objlist, int nv, float * vArr, int nt, int * tArr, Vector T, Vector R, Vector S, float scale = 1.0);

#endif
