#ifndef OROCOS_Sin_COMPONENT_HPP
#define OROCOS_Sin_COMPONENT_HPP

#include <rtt/RTT.hpp>

class Sin : public RTT::TaskContext{
  public:
    Sin(std::string const& name);
    bool configureHook();
    bool startHook();
    void updateHook();
    void stopHook();
    void cleanupHook();
    private:
    RTT::InputPort<double> _inPort;
    RTT::OutputPort<double> _outPort;
};
#endif
