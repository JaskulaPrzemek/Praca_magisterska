#ifndef OROCOS_Addition_COMPONENT_HPP
#define OROCOS_Addition_COMPONENT_HPP

#include <rtt/RTT.hpp>

class Addition : public RTT::TaskContext{
  public:
    Addition(std::string const& name);
    bool configureHook();
    bool startHook();
    void updateHook();
    void stopHook();
    void cleanupHook();
    private:
    bool flag1;
    double value1;
    bool flag2;
    double value2;
    RTT::InputPort<double> _inPort1;
    RTT::InputPort<double> _inPort2;
    RTT::OutputPort<double> _outPort;
};
#endif
