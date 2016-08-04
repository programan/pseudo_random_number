cmake_minimum_required(VERSION 3.6)
project(test01)

#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
#http://stackoverflow.com/questions/31787115/setting-clion-build-and-binary-directory
#set(dir ${CMAKE_CURRENT_SOURCE_DIR})
#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${dir}/bin")

set(SOURCE_FILES test01.cpp)
# add_executable("${PROJECT_NAME}.out" ${SOURCE_FILES})
add_executable(hoge ${SOURCE_FILES})

#### cmake .
