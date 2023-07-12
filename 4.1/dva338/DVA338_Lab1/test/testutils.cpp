#include "testutils.h"
#include <math.h> // math abs
#include <stdio.h>
#include <stdlib.h>
bool Equal(float expected, float actual, char const* msg, float delta)
{
    bool testPasses = fabsf(expected-actual) <= delta;
    
    if(!testPasses)
    {
        printf("Expected: %f, Actual: %f\n", expected, actual);
        printf("Test Failed: %s\n", msg);
    }

    return testPasses;
}
bool Equal(Matrix expected, Matrix actual, char const* msg, float delta)
{
	//return !memcmp(&expected,&actual, sizeof(Matrix));
    bool testPasses = true;
    for(int i = 0; i < 16; ++i)
    {
        if(fabsf(actual.e[i] - expected.e[i]) > delta)
        {
            //Print all errors
            printf("Matrix Comparison: Index %d: Expected %f but was %f\n", i, expected.e[i], actual.e[i]);
            testPasses = false;
        }
    }
    testPasses = testPasses && true;
    
    if(!testPasses)
    {
        printf("Test Failed: %s\n", msg);
    }

    return testPasses;
}
bool Equal(Vector expected, Vector actual, char const* msg, float delta)
{
    bool testPasses = fabsf(actual.x - expected.x) <= delta && 
    fabsf(actual.y - expected.y) <= delta && 
    fabsf(actual.z - expected.z) <= delta;
    if(!testPasses)
    {
        printf("Vector Comparison: ");
        PrintVector("expected", expected);
        PrintVector("Actual", actual);
        printf("Test Failed: %s\n", msg);
    }

    return testPasses;
}

bool Equal(HomVector expected, HomVector actual, char const* msg, float delta)
{
    bool testPasses = fabsf(actual.x - expected.x) <= delta && 
        fabsf(actual.y - expected.y) <= delta && 
        fabsf(actual.z - expected.z) <= delta && 
        fabsf(actual.w - expected.w) <= delta;
    if(!testPasses)
    {
        printf("HomVector Comparison: ");
        PrintHomVector("expected", expected);
        PrintHomVector("Actual", actual);
        printf("Test Failed: %s\n", msg);
    }

    return testPasses;
}

void setupTestSuite(testsuite* ts)
{
    ts->NR_OF_TESTS = 0;
    if(NULL == ts->testfuncs)
        ts->testfuncs = (int (**)()) malloc(MAX_NR_OF_TESTS * sizeof(void*));
}

void teardownTestSuite(testsuite* ts)
{
    ts->NR_OF_TESTS = -1;
    free(ts->testfuncs);
}

void ADD_TEST(testsuite* ts, int (*testfunc)(void))
{
    ts->testfuncs[ts->NR_OF_TESTS++] = testfunc;
}

int RUN_TESTS(testsuite* ts)
{
    int failedTests = 0;

    for(int i = 0; i < ts->NR_OF_TESTS; ++i)
    {
        failedTests += ts->testfuncs[i]();
    }
    return failedTests;
}