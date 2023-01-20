#ifndef OROCOS_Time_COMPONENT_HPP
#define OROCOS_Time_COMPONENT_HPP

#include <rtt/RTT.hpp>

class Time : public RTT::TaskContext{
  public:
    Time(std::string const& name);
    bool configureHook();
    bool startHook();
    void updateHook();
    void stopHook();
    void cleanupHook();
    protected:
    double Hz;
    private:
    double czas;
    RTT::OutputPort<double> _outPort;
};
#endif
