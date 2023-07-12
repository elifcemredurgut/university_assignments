#include "test_runner.h"

#include "camera_tests.h"
#include "math_tests.h"

#include <cstdlib>

int run_all_tests()
{
    return run_math_tests() + run_camera_tests();
}

int main(int argc, char* argv[])
{
    int suiteID;    //0 = Math, 1 = Camera, ...
    if(argc > 1)
    {
        suiteID = atoi(argv[1]);
        int result = 0;
        switch (suiteID)
        {
        case 0:
            result = run_math_tests();
            break;
        case 1:
            result = run_camera_tests();
            break;
        default:
            result = run_all_tests();
            break;
        }
        return result;
    }
    else
    {
        return run_all_tests();
    }
}