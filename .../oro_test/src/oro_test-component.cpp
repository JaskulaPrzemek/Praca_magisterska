#include "oro_test-component.hpp"
#include <rtt/Component.hpp>
#include <iostream>

Oro_test::Oro_test(std::string const& name) : TaskContext(name){
  std::cout << "Oro_test constructed !" <<std::endl;
  ports()->addEventPort("inPort", _inPort).doc("Input port");
}

bool Oro_test::configureHook(){
  std::cout << "Oro_test configured !" <<std::endl;
  return true;
}

bool Oro_test::startHook(){
  std::cout << "Oro_test started !" <<std::endl;
  return true;
}

void Oro_test::updateHook(){
  std::cout << "Oro_test executes updateHook !" <<std::endl;
   double msg;
 if(_inPort.read(msg) == RTT::NewData){
   std::cout << "Otrzymana Liczba " <<msg<<std::endl;
 }
}

void Oro_test::stopHook() {
  std::cout << "Oro_test executes stopping !" <<std::endl;
}

void Oro_test::cleanupHook() {
  std::cout << "Oro_test cleaning up !" <<std::endl;
}

/*
 * Using this macro, only one component may live
 * in one library *and* you may *not* link this library
 * with another component library. Use
 * ORO_CREATE_COMPONENT_TYPE()
 * ORO_LIST_COMPONENT_TYPE(Oro_test)
 * In case you want to link with another library that
 * already contains components.
 *c
 * If you have put your component class
 * in a namespace, don't forget to add it here too:
 */
ORO_CREATE_COMPONENT(Oro_test)
