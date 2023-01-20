
#
# Components, types and plugins.
#
# The CMake 'target' names are identical to the first argument of the
# macros below, except for orocos_typegen_headers, where the target is fully
# controlled by generated code of 'typegen'.
#

# Creates a component library liboro_test-<target>.so
# and installs in the directory lib/orocos/oro_test/
#
orocos_component(oro_test oro_test-component.hpp oro_test-component.cpp) # ...you may add multiple source files
orocos_component(oro_test1 oro_test-component1.hpp oro_test-component1.cpp)
# You may add multiple orocos_component statements.

#
# Additional headers:
#
# Installs in the include/orocos/oro_test/ directory
#
orocos_install_headers(oro_test-component.hpp) # ...you may add multiple header files
#
# You may add multiple orocos_install_headers statements.
orocos_install_headers(oro_test-component1.hpp)
