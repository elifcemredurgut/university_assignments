#define _USE_MATH_DEFINES // To get M_PI defined
#include <math.h>
#include <stdio.h>
#include "algebra.h"
#include "camera.h"
#include <math.h>

#define PI 3.14159265


Vector CrossProduct(Vector a, Vector b) {
	Vector v = { a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y*b.x };
	return v;
}

float DotProduct(Vector a, Vector b) {
	return a.x*b.x + a.y*b.y + a.z*b.z;
}

Vector Subtract(Vector a, Vector b) {
	Vector v = { a.x-b.x, a.y-b.y, a.z-b.z };
	return v;
}    

Vector Add(Vector a, Vector b) {
	Vector v = { a.x+b.x, a.y+b.y, a.z+b.z };
	return v;
}    

float Length(Vector a) {
	return sqrt(a.x*a.x + a.y*a.y + a.z*a.z);
}

Vector Normalize(Vector a) {
	float len = Length(a);
	Vector v = { a.x/len, a.y/len, a.z/len };
	return v;
}

Vector ScalarVecMul(float t, Vector a) {
	Vector b = { t*a.x, t*a.y, t*a.z };
	return b;
}

HomVector MatVecMul(Matrix a, Vector b) {
	HomVector h;
	h.x = b.x*a.e[0] + b.y*a.e[4] + b.z*a.e[8] + a.e[12];
	h.y = b.x*a.e[1] + b.y*a.e[5] + b.z*a.e[9] + a.e[13];
	h.z = b.x*a.e[2] + b.y*a.e[6] + b.z*a.e[10] + a.e[14];
	h.w = b.x*a.e[3] + b.y*a.e[7] + b.z*a.e[11] + a.e[15];
	return h;
}

Vector Homogenize(HomVector h) {
	Vector a;
	if (h.w == 0.0) {
		fprintf(stderr, "Homogenize: w = 0\n");
		a.x = a.y = a.z = 9999999;
		return a;
	}
	a.x = h.x / h.w;
	a.y = h.y / h.w;
	a.z = h.z / h.w;
	return a;
}

Matrix MatMatMul(Matrix a, Matrix b) {
	Matrix c;
	int i, j, k;
	for (i = 0; i < 4; i++) {
		for (j = 0; j < 4; j++) {
			c.e[j*4+i] = 0.0;
			for (k = 0; k < 4; k++)
				c.e[j*4+i] += a.e[k*4+i] * b.e[j*4+k];
		}
	}
	return c;
}

void PrintVector(char const *name, Vector a) {
	printf("%s: %6.5lf %6.5lf %6.5lf\n", name, a.x, a.y, a.z);
}

void PrintHomVector(char const *name, HomVector a) {
	printf("%s: %6.5lf %6.5lf %6.5lf %6.5lf\n", name, a.x, a.y, a.z, a.w);
}

void PrintMatrix(char const *name, Matrix a) { 
	int i,j;

	printf("%s:\n", name);
	for (i = 0; i < 4; i++) {
		for (j = 0; j < 4; j++) {
			printf("%6.5lf ", a.e[j*4+i]);
		}
		printf("\n");
	}
}

//Given three points on a surface, return the surface normal
Vector SurfaceNormal(Vector a, Vector b, Vector c)
{
	/* Lab 1: Calculate the actual surface normals */
	Vector a_b = { b.x - a.x, b.y - a.y, b.z - a.z };
	Vector a_c = { c.x - a.x, c.y - a.y, c.z - a.z };

	Vector v = CrossProduct(a_b, a_c);
	Vector normalizedV = Normalize(v);
	return normalizedV;

	//return {0.80078125f,0.34765625f, 0.1796875f};
}

Matrix TranslationMatrix(int x, int y, int z)
{
	Matrix V;
	V.e[0] = 1.0f; V.e[4] = 0.0f; V.e[8] = 0.0f;  V.e[12] = x;
	V.e[1] = 0.0f; V.e[5] = 1.0f; V.e[9] = 0.0f;  V.e[13] = y;
	V.e[2] = 0.0f; V.e[6] = 0.0f; V.e[10] = 1.0f; V.e[14] = z;
	V.e[3] = 0.0f; V.e[7] = 0.0f; V.e[11] = 0.0f; V.e[15] = 1.0f;
	return V;
}

Matrix ScaleMatrix(int x, int y, int z)
{
	Matrix V;
	V.e[0] = x;    V.e[4] = 0.0f; V.e[8] = 0.0f;  V.e[12] = x;
	V.e[1] = 0.0f; V.e[5] = y;    V.e[9] = 0.0f;  V.e[13] = y;
	V.e[2] = 0.0f; V.e[6] = 0.0f; V.e[10] = z;    V.e[14] = z;
	V.e[3] = 0.0f; V.e[7] = 0.0f; V.e[11] = 0.0f; V.e[15] = 1.0f;
	return V;
}


Matrix Rx(int x)
{
	Matrix X;
	X.e[0] = 1.0f; X.e[4] = 0.0f;                 X.e[8] = 0.0f;                 X.e[12] = 0.0f;
	X.e[1] = 0.0f; X.e[5] = cos(x * PI / 180.0);  X.e[9] = -sin(x * PI / 180.0); X.e[13] = 0.0f;
	X.e[2] = 0.0f; X.e[6] = sin(x * PI / 180.0);  X.e[10] = cos(x * PI / 180.0); X.e[14] = 0.0f;
	X.e[3] = 0.0f; X.e[7] = 0.0f;                 X.e[11] = 0.0f;                X.e[15] = 1.0f;

	return X;
}

Matrix Ry(int y)
{
	Matrix Y;
	Y.e[0] = cos(y * PI / 180.0);  Y.e[4] = 0.0f; Y.e[ 8] = sin(y * PI / 180.0);  Y.e[12] = 0.0f;
	Y.e[1] = 0.0f;                 Y.e[5] = 1.0f; Y.e[ 9] = 0.0f;                 Y.e[13] = 0.0f;
	Y.e[2] = -sin(y * PI / 180.0); Y.e[6] = 0.0f; Y.e[10] = cos(y * PI / 180.0);  Y.e[14] = 0.0f;
	Y.e[3] = 0.0f;                 Y.e[7] = 0.0f; Y.e[11] = 0.0f;                 Y.e[15] = 1.0f;

	return Y;
}

Matrix Rz(int z)
{
	Matrix Z;
	Z.e[0] = cos(z * PI / 180.0); Z.e[4] = -sin(z * PI / 180.0); Z.e[8] = 0.0f;  Z.e[12] = 0.0f;
	Z.e[1] = sin(z * PI / 180.0); Z.e[5] = cos(z * PI / 180.0);  Z.e[9] = 0.0f;  Z.e[13] = 0.0f;
	Z.e[2] = 0.0f;                Z.e[6] = 0.0f;                 Z.e[10] = 1.0f; Z.e[14] = 0.0f;
	Z.e[3] = 0.0f;                Z.e[7] = 0.0f;                 Z.e[11] = 0.0f; Z.e[15] = 1.0f;

	return Z;
}


Matrix OrthogonalProjection(int left, int right, int bottom, int top, int near, int far)
{
	Matrix X;
	X.e[0] = 2/(right-left); X.e[4] = 0.0f;           X.e[ 8] = 0.0f;         X.e[12] = -(right+left)/(right-left);
	X.e[1] = 0.0f;           X.e[5] = 2/(top-bottom); X.e[ 9] = 0.0f;         X.e[13] = -(top+bottom)/(top-bottom);
	X.e[2] = 0.0f;           X.e[6] = 0.0f;           X.e[10] = 2/(far-near); X.e[14] = -(far+near)/(far-near);
	X.e[3] = 0.0f;           X.e[7] = 0.0f;           X.e[11] = 0.0f;         X.e[15] = 1.0f;

	return X;
}

Matrix PerspectiveProjection(float near, float far, float fovy, float aspect)
{
	Matrix P;

	P.e[0] = 1/(aspect*tan(fovy/2*PI/180.0)); P.e[4] = 0.0f;                           P.e[ 8] = 0.0f;                  P.e[12] = 0.0f;
	P.e[1] = 0.000000f;                       P.e[5] = 1 / tan(fovy / 2 * PI / 180.0); P.e[ 9] = 0.0f;                  P.e[13] = 0.0f;
	P.e[2] = 0.000000f;                       P.e[6] = 0.000000f;                      P.e[10] = (far+near)/(near-far); P.e[14] = 2*far*near/(near-far);
	P.e[3] = 0.000000f;                       P.e[7] = 0.000000f;                      P.e[11] = -1.000000f;            P.e[15] = 0.0f;
	
	return P;

}

