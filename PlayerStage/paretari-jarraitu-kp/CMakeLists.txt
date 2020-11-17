cmake_minimum_required(VERSION 2.8)
project( oztopoakEkidin )
#find_package( OpenCV REQUIRED)
#find_package( Curses REQUIRED)
set (CMAKE_MODULE_PATH "/usr/local/share/cmake/Modules")


SET( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -Wall -g -std=c++0x" )
SET( CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS} -lpthread -lncurses" )
include(UsePlayerC++)
include(UsePlayerPlugin)

#include_directories(${CURSES_INCLUDE_DIR})
player_add_playercpp_client(paretariJarraitu SOURCES src/paretariJarraitu.cpp)
#add_executable(playerMapping mapping.cc)
target_link_libraries( paretariJarraitu ${Player_LIBS})

install(TARGETS paretariJarraitu
  RUNTIME DESTINATION ${PROJECT_BINARY_DIR}/bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
)
