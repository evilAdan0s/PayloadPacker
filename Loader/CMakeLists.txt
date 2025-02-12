cmake_minimum_required(VERSION 3.10)
project(Loader)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -static")

include_directories(${PROJECT_SOURCE_DIR}/include)

set(SOURCE_FILES src/main.cpp src/WjCryptLib_Rc4.cpp res/resource.rc)

add_executable(Loader WIN32 ${SOURCE_FILES})

target_link_libraries(Loader "${PROJECT_SOURCE_DIR}/libs/64/Wintrust.lib")
target_link_libraries(Loader psapi)