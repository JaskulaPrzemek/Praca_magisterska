#ifndef OROCOS_ORO_TEST_COMPONENT1_HPP
#define OROCOS_ORO_TEST_COMPONENT1_HPP

#include <rtt/RTT.hpp>

class Oro_test1 : public RTT::TaskContext{
  public:
    Oro_test1(std::string const& name);
    bool configureHook();
    bool startHook();
    void updateHook();
    void stopHook();
    void cleanupHook();
    private:
    double liczbaWyslana;
    RTT::OutputPort<double> _outPort;
};
#endif
