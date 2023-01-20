#ifndef OROCOS_Cos_COMPONENT_HPP
#define OROCOS_Cos_COMPONENT_HPP

#include <rtt/RTT.hpp>

class Cos : public RTT::TaskContext{
  public:
    Cos(std::string const& name);
    bool configureHook();
    bool startHook();
    void updateHook();
    void stopHook();
    void cleanupHook();
    protected:
    double Hz;
    private:
    RTT::InputPort<double> _inPort;
    RTT::OutputPort<double> _outPort;
};
#endif
