cmake_minimum_required(VERSION 2.8)
project( wavefrontPlanifikatzailea )
set (CMAKE_MODULE_PATH "/usr/local/share/cmake/Modules")

SET( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -Wall -g -std=c++0x" )
SET( CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS} -lpthread " )
include(UsePlayerC++)
include(UsePlayerPlugin)

player_add_playercpp_client(wavefront SOURCES src/wave.cpp)
target_link_libraries( wavefront ${Player_LIBS})


install(TARGETS wavefront 
  RUNTIME DESTINATION ${PROJECT_BINARY_DIR}/bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
)
