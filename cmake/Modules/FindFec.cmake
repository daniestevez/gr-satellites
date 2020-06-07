FIND_PATH(
    FEC_INCLUDE_DIRS
    NAMES fec.h
    HINTS $ENV{FEC_DIR}/include
        ${PC_FEC_INCLUDEDIR}
    PATHS /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    FEC_LIBRARIES
    NAMES fec
    HINTS $ENV{FEC_DIR}/lib
        ${PC_FEC_LIBDIR}
    PATHS /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(Fec DEFAULT_MSG FEC_LIBRARIES FEC_INCLUDE_DIRS)
