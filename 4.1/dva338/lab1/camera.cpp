#include "camera.h"
#include <stdio.h>

//Interface function for the projection matrix
//Note: Not all parameters may be needed, but the provided tests require this signature
Matrix ProjectionMatrix(Camera cam, int screenWidth, int screenHeight, ProjectionMode mode)
{
	Matrix P;
	
	// Assignment 1: Calculate the projection transform yourself 	
	// The matrix P should be calculated from camera parameters
	// Therefore, you need to replace this hard-coded transform.
	
	if (mode == PERSPECTIVE) {
		P = PerspectiveProjection(cam.nearPlane, cam.farPlane, cam.fov, 1024.0/768.0);
	}
	else { //ORTHOGONAL
		P = OrthogonalProjection(-20.0,20.0,-10.0,10.0,1.0,10000.0);
		//P = OrthogonalProjection(-cam.position.x, cam.position.x, -cam.position.y, cam.position.y, cam.nearPlane, cam.farPlane);
	}
	/*
	P.e[0] = 1.299038f; P.e[4] = 0.000000f; P.e[8] = 0.000000f;   P.e[12] = 0.0f;
	P.e[1] = 0.000000f; P.e[5] = 1.732051f; P.e[9] = 0.000000f;   P.e[13] = 0.0f;
	P.e[2] = 0.000000f; P.e[6] = 0.000000f; P.e[10] = -1.000200f; P.e[14] = -2.000200f;
	P.e[3] = 0.000000f; P.e[7] = 0.000000f; P.e[11] = -1.000000f; P.e[15] = 0.0f;*/

	return P;
}
//Interface function for view matrix
Matrix ViewMatrix(Camera cam)
{
	Matrix T = TranslationMatrix(-cam.position.x, -cam.position.y, -cam.position.z);
	Matrix R_x = Rx(-cam.rotation.x);
	Matrix R_y = Ry(-cam.rotation.y);
	Matrix R_z = Rz(-cam.rotation.z);

	Matrix V = MatMatMul(R_z, MatMatMul(R_y, MatMatMul(R_x, T)));
	// Assignment 1: Calculate the transform to view coordinates yourself 	
	// The matrix V should be calculated from camera parameters
	// Therefore, you need to replace this hard-coded transform. 

	/*
	Matrix V;
	V.e[0] = 1.0f; V.e[4] = 0.0f; V.e[8] = 0.0f; V.e[12] = 0.0f;
	V.e[1] = 0.0f; V.e[5] = 1.0f; V.e[9] = 0.0f; V.e[13] = 0.0f;
	V.e[2] = 0.0f; V.e[6] = 0.0f; V.e[10] = 1.0f; V.e[14] = -cam.position.z;
	V.e[3] = 0.0f; V.e[7] = 0.0f; V.e[11] = 0.0f; V.e[15] = 1.0f;*/
	return V;
}