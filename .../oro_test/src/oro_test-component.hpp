#ifndef OROCOS_ORO_TEST_COMPONENT_HPP
#define OROCOS_ORO_TEST_COMPONENT_HPP

#include <rtt/RTT.hpp>

class Oro_test : public RTT::TaskContext{
  public:
    Oro_test(std::string const& name);
    bool configureHook();
    bool startHook();
    void updateHook();
    void stopHook();
    void cleanupHook();
    private:
    RTT::InputPort<double> _inPort;
};
#endif
