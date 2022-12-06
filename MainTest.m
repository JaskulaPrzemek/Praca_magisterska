timerVal=tic;
%filename=fullfile(pwd,"catkin_ws/start.bash");
%system(filename)
steps1=Qlearning(1,0,-0.01,1,1);
time1=toc(timerVal)
figure(2);
timerVal=tic;
%steps2=Qlearning(1,1,0.005,0);
time2=toc(timerVal)
figure(3);
plot(steps1);
hold on;
plot(steps2);
xlabel("iterations");
ylabel("Steps");
legend('ClassicQ','QFPA');