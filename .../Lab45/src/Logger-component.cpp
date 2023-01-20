#include "Logger-component.hpp"
#include <rtt/Component.hpp>
#include <iostream>
#include <fstream>

Logger::Logger(std::string const& name) : TaskContext(name){
  ports()->addEventPort("inPort", _inPort).doc("Input port");
  //std::cout<<this.name<<std::endl;
}

bool Logger::configureHook(){
  std::cout << "Logger configured !" <<std::endl;
  return true;
}

bool Logger::startHook(){
  std::cout << "Logger started !" <<std::endl;
  return true;
}

void Logger::updateHook(){
  double msg;
  std::ofstream outfile;
  //std::cout<<this.name<<std::endl;
 if(_inPort.read(msg) == RTT::NewData){
  outfile.open(getName(), std::ios_base::app); // append instead of overwrite
  outfile << msg<<std::endl;
  outfile.close(); 
 }
 
}

void Logger::stopHook() {
  std::cout << "Logger executes stopping !" <<std::endl;
}

void Logger::cleanupHook() {
  std::cout << "Logger cleaning up !" <<std::endl;
}

/*
 * Using this macro, only one component may live
 * in one library *and* you may *not* link this library
 * with another component library. Use
 * ORO_CREATE_COMPONENT_TYPE()
 * ORO_LIST_COMPONENT_TYPE(Logger)
 * In case you want to link with another library that
 * already contains components.
 *
 * If you have put your component class
 * in a namespace, don't forget to add it here too:
 */
ORO_CREATE_COMPONENT(Logger)
