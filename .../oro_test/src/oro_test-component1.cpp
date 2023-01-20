#include "oro_test-component1.hpp"
#include <rtt/Component.hpp>
#include <iostream>

Oro_test1::Oro_test1(std::string const& name) : TaskContext(name){
  std::cout << "Oro_test constructed !" <<std::endl;
  ports()->addPort("outPort",_outPort).doc("Port outputowy");
  liczbaWyslana=0;
}

bool Oro_test1::configureHook(){
  std::cout << "Oro_test configured !" <<std::endl;
  return this->setPeriod(2);
}

bool Oro_test1::startHook(){
  std::cout << "Oro_test started !" <<std::endl;
  return true;
}

void Oro_test1::updateHook(){
  std::cout << "Oro_test1 executes updateHook !" <<std::endl;
  liczbaWyslana++;
  _outPort.write(liczbaWyslana);
}

void Oro_test1::stopHook() {
  std::cout << "Oro_test executes stopping !" <<std::endl;
}

void Oro_test1::cleanupHook() {
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
ORO_CREATE_COMPONENT(Oro_test1)
