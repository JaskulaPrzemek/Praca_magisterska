#include "Sin-component.hpp"
#include <rtt/Component.hpp>
#include <iostream>
#include <cmath>

Sin::Sin(std::string const& name) : TaskContext(name){
  std::cout << "Sin constructed !" <<std::endl;
  ports()->addEventPort("inPort", _inPort).doc("Input port");
  ports()->addPort("outPort",_outPort).doc("Port outputowy");
}

bool Sin::configureHook(){
  std::cout << "Sin configured !" <<std::endl;
  return true;
}

bool Sin::startHook(){
  std::cout << "Sin started !" <<std::endl;
  return true;
}

void Sin::updateHook(){
  double msg;
 if(_inPort.read(msg) == RTT::NewData){
    double temp = sin(msg);
    std::cout << "Sin of "<<msg <<"is "<<temp <<std::endl;
    _outPort.write(sin(msg));
 }
}

void Sin::stopHook() {
  std::cout << "Sin executes stopping !" <<std::endl;
}

void Sin::cleanupHook() {
  std::cout << "Sin cleaning up !" <<std::endl;
}

/*
 * Using this macro, only one component may live
 * in one library *and* you may *not* link this library
 * with another component library. Use
 * ORO_CREATE_COMPONENT_TYPE()
 * ORO_LIST_COMPONENT_TYPE(Sin)
 * In case you want to link with another library that
 * already contains components.
 *
 * If you have put your component class
 * in a namespace, don't forget to add it here too:
 */
ORO_CREATE_COMPONENT(Sin)
