#include <stdlib.h>
#include <stdio.h>
#include "mesh.h"
#include <assert.h>
float rnd() {
	return 2.0f * float(rand()) / float(RAND_MAX) - 1.0f;
}

void insertModel(Mesh** list, int nv, float* vArr, int nt, int* tArr, Vector T, Vector R, Vector S, float scale) {  //add transformation vertices
	Mesh* mesh = (Mesh*)malloc(sizeof(Mesh));
	mesh->nv = nv;
	mesh->nt = nt;
	mesh->vertices = (Vector*)malloc(nv * sizeof(Vector));
	mesh->vnorms = (Vector*)malloc(nv * sizeof(Vector));
	mesh->triangles = (Triangle*)malloc(nt * sizeof(Triangle));
	
	// set mesh vertices
	for (int i = 0; i < nv; i++) {
		mesh->vertices[i].x = vArr[i * 3] * scale;
		mesh->vertices[i].y = vArr[i * 3 + 1] * scale;
		mesh->vertices[i].z = vArr[i * 3 + 2] * scale;
	}

	// set mesh triangles
	for (int i = 0; i < nt; i++) {
		mesh->triangles[i].vInds[0] = tArr[i * 3];
		mesh->triangles[i].vInds[1] = tArr[i * 3 + 1];
		mesh->triangles[i].vInds[2] = tArr[i * 3 + 2];
	}

	// Assignment 1: 
	// Calculate and store suitable vertex normals for the mesh here.
	// Replace the code below that simply sets some arbitrary normal values	
	// Note: You need to fix the implementation of the SurfaceNormal function we give you
	// as currently it returns a constant value

	//initialize the vector normals as {0,0,0}
	for (int i = 0; i < nv; i++) {
		mesh->vnorms[i] = { 0,0,0 };
	}
	
	//add surface normals to vertice normals
	/*for (int i = 0; i < nt; i++) {
		Vector surfaceNormal = SurfaceNormal(mesh->vertices[tArr[i*3]], mesh->vertices[tArr[i * 3+1]], mesh->vertices[tArr[i * 3+2]]);
		mesh->vnorms[tArr[i * 3  ]] = Normalize(Add(mesh->vnorms[tArr[i * 3  ]], surfaceNormal));
		mesh->vnorms[tArr[i * 3+1]] = Normalize(Add(mesh->vnorms[tArr[i * 3+1]], surfaceNormal));
		mesh->vnorms[tArr[i * 3+2]] = Normalize(Add(mesh->vnorms[tArr[i * 3+2]], surfaceNormal));
	}*/
	for (int i = 0; i < nt; i++) {
		Vector surfaceNormal = SurfaceNormal(mesh->vertices[tArr[i * 3]], mesh->vertices[tArr[i * 3 + 1]], mesh->vertices[tArr[i * 3 + 2]]);
		mesh->vnorms[tArr[i * 3    ]] = Add(mesh->vnorms[tArr[i * 3    ]], surfaceNormal);
		mesh->vnorms[tArr[i * 3 + 1]] = Add(mesh->vnorms[tArr[i * 3 + 1]], surfaceNormal);
		mesh->vnorms[tArr[i * 3 + 2]] = Add(mesh->vnorms[tArr[i * 3 + 2]], surfaceNormal);
	}
	for (int i = 0; i < nv; i++) {
		mesh->vnorms[i] = Normalize(mesh->vnorms[i]);
	}
	mesh->translation = T;
	mesh->rotation = R;
	mesh->scaling = S;

	mesh->next = *list;
	*list = mesh;
}
