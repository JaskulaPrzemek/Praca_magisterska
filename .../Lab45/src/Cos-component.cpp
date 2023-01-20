#include "Cos-component.hpp"
#include <rtt/Component.hpp>
#include <iostream>
#include <cmath>
Cos::Cos(std::string const& name) : TaskContext(name){
std::cout << "COS constructed !" <<std::endl;
  ports()->addEventPort("inPort", _inPort).doc("Input port");
  ports()->addPort("outPort",_outPort).doc("Port outputowy");
}

bool Cos::configureHook(){
  std::cout << "Cos configured !" <<std::endl;
  return true;
}

bool Cos::startHook(){
  std::cout << "Cos started !" <<std::endl;
  return true;
}

void Cos::updateHook(){
  double msg;
 if(_inPort.read(msg) == RTT::NewData){
    double temp = cos(msg);
    //std::cout << "Cos of "<<msg <<"is "<<temp <<std::endl;
    _outPort.write(cos(msg));
 }
 
}

void Cos::stopHook() {
  std::cout << "Cos executes stopping !" <<std::endl;
}

void Cos::cleanupHook() {
  std::cout << "Cos cleaning up !" <<std::endl;
}

/*
 * Using this macro, only one component may live
 * in one library *and* you may *not* link this library
 * with another component library. Use
 * ORO_CREATE_COMPONENT_TYPE()
 * ORO_LIST_COMPONENT_TYPE(Cos)
 * In case you want to link with another library that
 * already contains components.
 *
 * If you have put your component class
 * in a namespace, don't forget to add it here too:
 */
ORO_CREATE_COMPONENT(Cos)
