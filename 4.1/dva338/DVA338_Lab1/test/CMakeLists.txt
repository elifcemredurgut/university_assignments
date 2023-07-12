cmake_minimum_required (VERSION 3.13)
if(DEV_BUILD)
    include_directories(
        ..
    )

    # Make test libraries
    # The tests are built against the library files generated
    # from different parts of the skeleton
    add_library(camera_tests 
    ../algebra.h
    ../camera.h
    testutils.h
    testutils.cpp
    camera_tests.h
    camera_tests.cpp)

    target_link_libraries(camera_tests
        lib_algebra
        lib_camera
    )

    add_library(math_tests 
    ../algebra.h
    ../mesh.h 
    testutils.h
    testutils.cpp
    math_tests.h
    math_tests.cpp)

    target_link_libraries(math_tests
        lib_algebra
        lib_mesh
    )

    set(TEST_LIBRARIES 
        camera_tests
        math_tests
    )
else()
    set(TEST_LIBRARIES 
        "./prebuilds/Release/camera_tests.lib"
        "./prebuilds/Release/math_tests.lib"
    )
endif() #end if(NOT STUDENT_BUILD)
add_executable(test_runner
    test_runner.h
    test_runner.cpp
)

target_link_libraries(test_runner 
    ${TEST_LIBRARIES}
)

add_test(NAME math_tests COMMAND test_runner 0)
add_test(NAME camera_tests COMMAND test_runner 1)