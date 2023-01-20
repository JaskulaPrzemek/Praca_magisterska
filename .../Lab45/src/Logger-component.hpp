#ifndef OROLogger_Logger_COMPONENT_HPP
#define OROLogger_Logger_COMPONENT_HPP

#include <rtt/RTT.hpp>

class Logger : public RTT::TaskContext{
  public:
    Logger(std::string const& name);
    bool configureHook();
    bool startHook();
    void updateHook();
    void stopHook();
    void cleanupHook();
    private:
    RTT::InputPort<double> _inPort;
};
#endif
