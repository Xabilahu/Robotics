cmake_minimum_required(VERSION 2.8)
project( square )

set (CMAKE_MODULE_PATH "/usr/local/share/cmake/Modules")


SET( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -Wall -g -std=c++0x" )
SET( CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS}") 
include(UsePlayerC++)
include(UsePlayerPlugin)

player_add_playercpp_client(square SOURCES src/square.cpp)
target_link_libraries( square ${Player_LIBS} )

install(TARGETS square
  RUNTIME DESTINATION ${PROJECT_BINARY_DIR}/bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
)
