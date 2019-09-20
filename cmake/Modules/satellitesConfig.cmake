INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_SATELLITES satellites)

FIND_PATH(
    SATELLITES_INCLUDE_DIRS
    NAMES satellites/api.h
    HINTS $ENV{SATELLITES_DIR}/include
        ${PC_SATELLITES_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    SATELLITES_LIBRARIES
    NAMES gnuradio-satellites
    HINTS $ENV{SATELLITES_DIR}/lib
        ${PC_SATELLITES_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/satellitesTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(SATELLITES DEFAULT_MSG SATELLITES_LIBRARIES SATELLITES_INCLUDE_DIRS)
MARK_AS_ADVANCED(SATELLITES_LIBRARIES SATELLITES_INCLUDE_DIRS)
