#include "Time-component.hpp"
#include <rtt/Component.hpp>
#include <iostream>
#include <rtt/Attribute.hpp>

Time::Time(std::string const& name) : TaskContext(name){
  std::cout << "Time constructed !" <<std::endl;
  czas=0;
  ports()->addPort("outPort",_outPort).doc("Port outputowy");
  this->addAttribute("herz", Hz);
  this->setPeriod(1);
}

bool Time::configureHook(){

 
}

bool Time::startHook(){
  std::cout << "Time started !" <<std::endl;
  return true;
}

void Time::updateHook(){
  czas+=1/Hz;
  std::cout << "Time flies!"<<czas <<std::endl;
  _outPort.write(czas);
}

void Time::stopHook() {
  std::cout << "Time executes stopping !" <<std::endl;
}

void Time::cleanupHook() {
  std::cout << "Time cleaning up !" <<std::endl;
}

/*
 * Using this macro, only one component may live
 * in one library *and* you may *not* link this library
 * with another component library. Use
 * ORO_CREATE_COMPONENT_TYPE()
 * ORO_LIST_COMPONENT_TYPE(Time)
 * In case you want to link with another library that
 * already contains components.
 *
 * If you have put your component class
 * in a namespace, don't forget to add it here too:
 */
ORO_CREATE_COMPONENT(Time)
