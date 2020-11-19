cmake_minimum_required(VERSION 2.8)
project( paretariJarraituKTM )
#find_package( OpenCV REQUIRED)
#find_package( Curses REQUIRED)
#find_package( GSL REQUIRED)
#include_directories(${GSL_INCLUDE_DIRS} ${GSLCBLAS_INCLUDE_DIRS})

set (GSL_LIBRARIES "-lgsl")
set (GSLCBLAS_LIBRARIES "-lgslcblas")

set (CMAKE_MODULE_PATH "/usr/local/share/cmake/Modules")


SET( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -Wall -g -std=c++0x" )
SET( CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS}") 
include(UsePlayerC++)
include(UsePlayerPlugin)

player_add_playercpp_client(paretariJarraituKTM SOURCES src/paretariJarraituKTM.cpp)
target_link_libraries( paretariJarraituKTM ${Player_LIBS} ${GSL_LIBRARIES} ${GSLCBLAS_LIBRARIES})

install(TARGETS paretariJarraituKTM
  RUNTIME DESTINATION ${PROJECT_BINARY_DIR}/bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
)
