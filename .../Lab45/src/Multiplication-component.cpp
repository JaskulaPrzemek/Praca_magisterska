#include "Multiplication-component.hpp"
#include <rtt/Component.hpp>
#include <iostream>
#include <cmath>

Multiplication::Multiplication(std::string const& name) : TaskContext(name){
  std::cout << "Multiplication constructed !" <<std::endl;
  ports()->addPort("outPort",_outPort).doc("Port outputowy");
  ports()->addEventPort("inPort1", _inPort1).doc("Input port");
  ports()->addEventPort("inPort2", _inPort2).doc("Input port");
  flag1=false;
  flag2=false;
}

bool Multiplication::configureHook(){
  std::cout << "Multiplication configured !" <<std::endl;
  return true;
}

bool Multiplication::startHook(){
  std::cout << "Multiplication started !" <<std::endl;
  return true;
}

void Multiplication::updateHook(){
  double msg1;
  double msg2;
 if(_inPort1.read(msg1) == RTT::NewData){
    value1=msg1;
    flag1=true;
 }
  if(_inPort2.read(msg2) == RTT::NewData){
    value2=msg2;
    flag2=true;
 }
 if(flag1&&flag2){
_outPort.write(value1*value2);
  flag1=false;
  flag2=false;
 }
}

void Multiplication::stopHook() {
  std::cout << "Multiplication executes stopping !" <<std::endl;
}

void Multiplication::cleanupHook() {
  std::cout << "Multiplication cleaning up !" <<std::endl;
}

/*
 * UMultiplicationg this macro, only one component may live
 * in one library *and* you may *not* link this library
 * with another component library. Use
 * ORO_CREATE_COMPONENT_TYPE()
 * ORO_LIST_COMPONENT_TYPE(Multiplication)
 * In case you want to link with another library that
 * already contains components.
 *
 * If you have put your component class
 * in a namespace, don't forget to add it here too:
 */
ORO_CREATE_COMPONENT(Multiplication)
