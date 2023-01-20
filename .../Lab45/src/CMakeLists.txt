
#
# Components, types and plugins.
#
# The CMake 'target' names are identical to the first argument of the
# macros below, except for orocos_typegen_headers, where the target is fully
# controlled by generated code of 'typegen'.
#

# Creates a component library libLab45-<target>.so
# and installs in the directory lib/orocos/Lab45/
#
 # ...you may add multiple source files
orocos_component(Addition Addition-component.hpp Addition-component.cpp)
orocos_component(Multiplication Multiplication-component.hpp Multiplication-component.cpp)
orocos_component(Sin Sin-component.hpp Sin-component.cpp)
orocos_component(Cos Cos-component.hpp Cos-component.cpp)
orocos_component(Time Time-component.hpp Time-component.cpp)
orocos_component(Calka Calka-component.hpp Calka-component.cpp)
orocos_component(Logger Logger-component.hpp Logger-component.cpp)
# You may add multiple orocos_component statements.

#
# Additional headers:
#
# Installs in the include/orocos/Lab45/ directory
#
orocos_install_headers(Multiplication-component.hpp) # ...you may add multiple header files
orocos_install_headers(Addition-component.hpp)
orocos_install_headers(Sin-component.hpp)
orocos_install_headers(Cos-component.hpp)
orocos_install_headers(Time-component.hpp)
orocos_install_headers(Calka-component.hpp)
orocos_install_headers(Logger-component.hpp)
#
#
# You may add multiple orocos_install_headers statements.

