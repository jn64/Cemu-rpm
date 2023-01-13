# Fix for missing glslangConfig.cmake
# From <https://github.com/KhronosGroup/glslang/issues/2570#issue-831123061>
include("${CMAKE_CURRENT_LIST_DIR}/OSDependentTargets.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/OGLCompilerTargets.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/glslangTargets.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/SPIRVTargets.cmake")
