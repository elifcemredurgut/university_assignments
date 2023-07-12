//#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <iostream>
using namespace std;
#ifdef _WIN32
	//If you follow the setup instructions provided for Visual Studio
	//The include path specified already includes "GL", so we can ignore it
	#include <glew.h>
	#include <freeglut.h>
#elif defined(__APPLE__)
	#include <GL/glew.h>
	#include <GL/glut.h>
#else
	#include <GL/glew.h>
	#include <GL/freeglut.h>
#endif
#ifndef CAMERA_H_
#define CAMERA_H_
#endif
#include "camera.h"	//algebra is included in camera.h
#include "shaders.h"
#include "mesh.h"

//Uncomment if you want to run the tests before the graphics starts
#define ENABLE_TESTING


//Camera cam = {{-5,-5,20}, {-10,-30,-45}, 60, 1, 10000}; // Setup the global camera parameters
Camera cam = { {0,0,20},{0,0,0}, 120, 1, 10000};

int screen_width = 1024;
int screen_height = 768;

Mesh *meshList = NULL; // Global pointer to linked list of triangle meshes

GLuint shprg; // Shader program id


// Global transform matrices
// V is the view transform
// P is the projection transform
// PV = P * V is the combined view-projection transform
Matrix V, P, PV;


void prepareShaderProgram(const char ** vs_src, const char ** fs_src) {
	GLint success = GL_FALSE;

	shprg = glCreateProgram();

	GLuint vs = glCreateShader(GL_VERTEX_SHADER);
	glShaderSource(vs, 1, vs_src, NULL);
	glCompileShader(vs);
	glGetShaderiv(vs, GL_COMPILE_STATUS, &success);	
	if (!success) printf("Error in vertex shader!\n");
	else printf("Vertex shader compiled successfully!\n");

	GLuint fs = glCreateShader(GL_FRAGMENT_SHADER);
	glShaderSource(fs, 1, fs_src, NULL);
	glCompileShader(fs);
	glGetShaderiv(fs, GL_COMPILE_STATUS, &success);	
	if (!success) printf("Error in fragment shader!\n");
	else printf("Fragment shader compiled successfully!\n");

	glAttachShader(shprg, vs);
	glAttachShader(shprg, fs);
	glLinkProgram(shprg);
	GLint isLinked = GL_FALSE;
	glGetProgramiv(shprg, GL_LINK_STATUS, &isLinked);
	if (!isLinked) printf("Link error in shader program!\n");
	else printf("Shader program linked successfully!\n");
}

void prepareMesh(Mesh *mesh) {
	int sizeVerts = mesh->nv * 3 * sizeof(float);
	int sizeCols  = mesh->nv * 3 * sizeof(float);
	int sizeTris = mesh->nt * 3 * sizeof(int);
	
	// For storage of state and other buffer objects needed for vertex specification
	glGenVertexArrays(1, &mesh->vao);
	glBindVertexArray(mesh->vao);

	// Allocate VBO and load mesh data (vertices and normals)
	glGenBuffers(1, &mesh->vbo);
	glBindBuffer(GL_ARRAY_BUFFER, mesh->vbo);
	glBufferData(GL_ARRAY_BUFFER, sizeVerts + sizeCols, NULL, GL_STATIC_DRAW);
	glBufferSubData(GL_ARRAY_BUFFER, 0, sizeVerts, (void *)mesh->vertices);
	glBufferSubData(GL_ARRAY_BUFFER, sizeVerts, sizeCols, (void *)mesh->vnorms);

	// Allocate index buffer and load mesh indices
	glGenBuffers(1, &mesh->ibo);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh->ibo);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeTris, (void *)mesh->triangles, GL_STATIC_DRAW);

	// Define the format of the vertex data
	GLint vPos = glGetAttribLocation(shprg, "vPos");
	glEnableVertexAttribArray(vPos);
	glVertexAttribPointer(vPos, 3, GL_FLOAT, GL_FALSE, 0, NULL);

	// Define the format of the vertex data 
	GLint vNorm = glGetAttribLocation(shprg, "vNorm");
	glEnableVertexAttribArray(vNorm);
	glVertexAttribPointer(vNorm, 3, GL_FLOAT, GL_FALSE, 0, (void *)(mesh->nv * 3 *sizeof(float)));

	glBindVertexArray(0);

}

void renderMesh(Mesh *mesh) {
	
	// Assignment 1: Apply the transforms from local mesh coordinates to world coordinates here
	// Combine it with the viewing transform that is passed to the shader below

	Matrix T = TranslationMatrix(mesh->translation.x, mesh->translation.y, mesh->translation.z);
	Matrix S = ScaleMatrix(mesh->scaling.x, mesh->scaling.y, mesh->scaling.z);
	Matrix W = MatMatMul(T, MatMatMul(Rx(mesh->rotation.x), MatMatMul(Ry(mesh->rotation.y), MatMatMul(Rz(mesh->rotation.z), S))));

	Matrix M = MatMatMul(V, W);

	Matrix PM = MatMatMul(P, M);
	
	// Pass the viewing transform to the shader

	GLint loc_PM = glGetUniformLocation(shprg, "PV");   //It does not work
	glUniformMatrix4fv(loc_PM, 1, GL_FALSE, PM.e);

	//GLint loc_M = glGetUniformLocation(shprg, "PV");
	//glUniformMatrix4fv(loc_M, 1, GL_FALSE, PV.e);  


	// Select current resources 
	glBindVertexArray(mesh->vao);
	
	// To accomplish wireframe rendering (can be removed to get filled triangles)
	//glPolygonMode(GL_FRONT_AND_BACK, GL_LINE); 

	// Draw all triangles
	glDrawElements(GL_TRIANGLES, mesh->nt * 3, GL_UNSIGNED_INT, NULL); 
	glBindVertexArray(0);
}



void display(void) {
	Mesh *mesh;
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);  //glClear(GL_COLOR_BUFFER_BIT); 
	glEnable(GL_DEPTH_TEST);
	/*
	TODO: Assignment 1: The implementation of View- and ProjectionMatrix in camera.cpp 
	returns hardcoded matrices. Your assignment is to fix them.
	*/
	V = ViewMatrix(cam);
	
	P = ProjectionMatrix(cam, screen_width, screen_height);
	
	// This finds the combined view-projection matrix
	PV = MatMatMul(P, V);

	// Select the shader program to be used during rendering 
	glUseProgram(shprg);

	// Render all meshes in the scene
	mesh = meshList;
		
	while (mesh != NULL) {
		renderMesh(mesh);
		mesh = mesh->next;
	}

	glFlush();
}

void changeSize(int w, int h) {
	screen_width = w;
	screen_height = h;
	glViewport(0, 0, screen_width, screen_height);

}

void keypress(unsigned char key, int x, int y) {
	switch(key) {
	//POSITION
	case 'z':
		cam.position.z -= 0.2f;
		break;
	case 'Z':
		cam.position.z += 0.2f;
		break;
	case 'x':
		cam.position.x += -0.2f;
		break;
	case 'X':
		cam.position.x += 0.2f;
		break;
	case 'y':
		cam.position.y += 0.2f;
		break;
	case 'Y':
		cam.position.y += -0.2f;
		break;
	//ROTATION
	case 'i':
		cam.rotation.x += 1.0f;
		break;
	case 'Ý':
		cam.rotation.x += -1.0f;
		break;
	case 'j':
		cam.rotation.z += 1.0f;
		break;
	case 'J':
		cam.rotation.z += -1.0f;
		break;
	case 'k':
		cam.rotation.y += 1.0f;
		break;
	case 'K':
		cam.rotation.y += -1.0f;
		break;
	case 'Q':
	case 'q':		
		glutLeaveMainLoop();
		break;
	}
	glutPostRedisplay();
}

void init(void) {
	// Compile and link the given shader program (vertex shader and fragment shader)
	prepareShaderProgram(vs_n2c_src, fs_ci_src); 

	// Setup OpenGL buffers for rendering of the meshes
	Mesh * mesh = meshList;
	while (mesh != NULL) {
		prepareMesh(mesh);
		mesh = mesh->next;
	}	
}

void cleanUp(void) {	
	printf("Running cleanUp function... ");
	// Free openGL resources
	// ...

	// Free meshes
	// ...
	printf("Done!\n\n");
}


// Include data for some triangle meshes (hard coded in struct variables)
#include "./models/mesh_bunny.h"
#include "./models/mesh_cow.h"
#include "./models/mesh_cube.h"
#include "./models/mesh_frog.h"
#include "./models/mesh_knot.h"
#include "./models/mesh_sphere.h"
#include "./models/mesh_teapot.h"
#include "./models/mesh_triceratops.h"

#ifdef ENABLE_TESTING
#include "./test/camera_tests.h"
#include "./test/math_tests.h"
#endif

int main(int argc, char **argv) {
	
	// Setup freeGLUT	
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH); //!!!!!!!!!
	//glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
	glutInitWindowSize(screen_width, screen_height);
	glutCreateWindow("DVA338 Programming Assignments");
	glutDisplayFunc(display);
	glutReshapeFunc(changeSize);
	glutKeyboardFunc(keypress);
	glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS);

	// Specify your preferred OpenGL version and profile
	glutInitContextVersion(4, 5);
	//glutInitContextProfile(GLUT_COMPATIBILITY_PROFILE);	
	glutInitContextProfile(GLUT_CORE_PROFILE);

	// Uses GLEW as OpenGL Loading Library to get access to modern core features as well as extensions
	GLenum err = glewInit(); 
	if (GLEW_OK != err) { fprintf(stdout, "Error: %s\n", glewGetErrorString(err)); return 1; }

	// Output OpenGL version info
	fprintf(stdout, "GLEW version: %s\n", glewGetString(GLEW_VERSION));
	fprintf(stdout, "OpenGL version: %s\n", (const char *)glGetString(GL_VERSION));
	fprintf(stdout, "OpenGL vendor: %s\n\n", glGetString(GL_VENDOR));
	
	int count, model, tx, ty, tz, rx, ry, rz, sx, sy, sz;
	cout << "Enter the number of models you want to add: ";
	cin >> count;
	for (int i = 0; i < count; i++) {
		cout << "Enter the model: ";
		cin >> model;

		cout << "Enter the scaling factor: ";
		cin >> sx >> sy >> sz;
		Vector S = { sx, sy, sz };

		cout << "Enter the translation: ";
		cin >> tx >> ty >> tz;
		Vector T = { tx, ty, tz };

		cout << "Enter the rotation: ";
		cin >> rx >> ry >> rz;
		Vector R = { rx, ry, rz };

		if (model == 0) {
			insertModel(&meshList, cow.nov, cow.verts, cow.nof, cow.faces, T, R, S, 20.0);
		}
		else if (model == 1) {
			insertModel(&meshList, triceratops.nov, triceratops.verts, triceratops.nof, triceratops.faces, T, R, S, 3.0);
		}
		else if (model == 2) {
			insertModel(&meshList, bunny.nov, bunny.verts, bunny.nof, bunny.faces, T, R, S, 60.0);
		}
		else if (model == 3) {
			insertModel(&meshList, cube.nov, cube.verts, cube.nof, cube.faces, T, R, S, 5.0);
		}
		else if (model == 4) {
			insertModel(&meshList, frog.nov, frog.verts, frog.nof, frog.faces, T, R, S, 2.5);
		}
		else if (model == 5) {
			insertModel(&meshList, knot.nov, knot.verts, knot.nof, knot.faces, T, R, S, 1.0);
		}
		else if (model == 6) {
			insertModel(&meshList, sphere.nov, sphere.verts, sphere.nof, sphere.faces, T, R, S, 12.0);
		}
		else if (model == 7) {
			insertModel(&meshList, teapot.nov, teapot.verts, teapot.nof, teapot.faces, T, R, S, 3.0);
		}
		
	}
	

	

	// Insert the 3D models you want in your scene here in a linked list of meshes
	// Note that "meshList" is a pointer to the first mesh and new meshes are added to the front of the list	
	//insertModel(&meshList, cow.nov, cow.verts, cow.nof, cow.faces, 20.0);
	//insertModel(&meshList, triceratops.nov, triceratops.verts, triceratops.nof, triceratops.faces, 3.0);
	//insertModel(&meshList, bunny.nov, bunny.verts, bunny.nof, bunny.faces, 60.0);	
	//insertModel(&meshList, cube.nov, cube.verts, cube.nof, cube.faces, 5.0);
	//insertModel(&meshList, frog.nov, frog.verts, frog.nof, frog.faces, 2.5);
	//insertModel(&meshList, knot.nov, knot.verts, knot.nof, knot.faces, 1.0);
	//insertModel(&meshList, sphere.nov, sphere.verts, sphere.nof, sphere.faces, 12.0);
	//insertModel(&meshList, teapot.nov, teapot.verts, teapot.nof, teapot.faces, 3.0);
	
	//#ifdef ENABLE_TESTING
	//printf("----BEGIN TESTS---\n");
	/* Runs some tests. If you've done up to assignment 1.3, these should pass */
	/*if (run_camera_tests())
	{
		printf("Some camera tests did not pass\n");
	}

	/* These should pass if you've done 1.4 */
	/*if(run_math_tests())
	{
		printf("Some math tests did not pass\n");
	}
	printf("----END TESTS---\n");
	#endif*/
	
	init();
	glutMainLoop();

	cleanUp();	
	return 0;
}
