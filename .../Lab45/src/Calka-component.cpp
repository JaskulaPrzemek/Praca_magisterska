#include "Calka-component.hpp"
#include <rtt/Component.hpp>
#include <iostream>
#include <rtt/Attribute.hpp>

Calka::Calka(std::string const& name) : TaskContext(name){
  ports()->addEventPort("inPort", _inPort).doc("Input port");
  ports()->addPort("outPort",_outPort).doc("Port outputowy");
  this->addAttribute("herz", Hz);
  sum=0;
}

bool Calka::configureHook(){
  std::cout << "Calka configured !" <<std::endl;
  return true;
}

bool Calka::startHook(){
  std::cout << "Calka started !" <<std::endl;
  return true;
}

void Calka::updateHook(){
  double msg;
 if(_inPort.read(msg) == RTT::NewData){
    sum+=msg/Hz;
    _outPort.write(sum);
 }
 
}

void Calka::stopHook() {
  std::cout << "Calka executes stopping !" <<std::endl;
}

void Calka::cleanupHook() {
  std::cout << "Calka cleaning up !" <<std::endl;
}

/*
 * Using this macro, only one component may live
 * in one library *and* you may *not* link this library
 * with another component library. Use
 * ORO_CREATE_COMPONENT_TYPE()
 * ORO_LIST_COMPONENT_TYPE(Calka)
 * In case you want to link with another library that
 * already contains components.
 *
 * If you have put your component class
 * in a namespace, don't forget to add it here too:
 */
ORO_CREATE_COMPONENT(Calka)
