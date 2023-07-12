#ifndef _TESTUTILS_H
#define _TESTUTILS_H
#define MAX_NR_OF_TESTS 1000
#include "../algebra.h"
#include <cstddef>
bool Equal(float expected, float actual, char const* msg, float delta = 0.001f);
bool Equal(Matrix expected, Matrix actual, char const* msg, float delta = 0.001f);
bool Equal(Vector expected, Vector actual, char const* msg, float delta = 0.001f);

bool Equal(HomVector expected, HomVector actual, char const* msg, float delta = 0.001f);


/* Test Suite setup stuff */
typedef struct test_suite
{
    int NR_OF_TESTS = 0;
    int (**testfuncs)(void) = NULL;    
} testsuite;

void setupTestSuite(testsuite* ts);

void teardownTestSuite(testsuite* ts);

void ADD_TEST(testsuite* ts, int (*testfunc)(void));

int RUN_TESTS(testsuite* ts);

#endif