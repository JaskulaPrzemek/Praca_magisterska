
%filename=fullfile(pwd,"catkin_ws/start.bash");
%system(filename)
Gazebo=0
Map=CreateMap(1,Gazebo);
timerVal=tic;
steps1=Qlearning(Map,0,-0.01,1,Gazebo);
time1=toc(timerVal)
figure(2);
timerVal=tic;
steps2=Qlearning(Map,1,0.01,1,Gazebo);
time2=toc(timerVal)
figure(3);
plot(steps1);
hold on;
plot(steps2);
xlabel("iterations");
ylabel("Steps");
legend('ClassicQ','QFPA');