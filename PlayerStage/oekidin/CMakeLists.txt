cmake_minimum_required(VERSION 2.8)
project( oEkidin )

set (CMAKE_MODULE_PATH "/usr/local/share/cmake/Modules")

SET( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -Wall -g -std=c++0x" )
SET( CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS} " )
include(UsePlayerC++)
include(UsePlayerPlugin)

player_add_playercpp_client(laserInfo SOURCES src/laserInfo.cpp)
player_add_playercpp_client(oztopoakEkidin SOURCES src/oztopoakEkiditen-TODO.cpp)
target_link_libraries( laserInfo ${Player_LIBS} )

install(TARGETS laserInfo
  RUNTIME DESTINATION ${PROJECT_BINARY_DIR}/bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
)
