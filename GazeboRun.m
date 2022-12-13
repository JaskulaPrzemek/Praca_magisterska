function GazeboRun(Qmatrix,map)
try
    rosnode list;
catch exp   % Error from rosnode list
    rosinit  % only if error: rosinit
end
s=map(1).StartingPoint;
i=1;
x(1)=s(1);
y(1)=s(2);
spawnPioneer(s(1),s(2))

odomSub = rossubscriber("/pioneer2dx/odom","DataFormat","struct");
vel = rospublisher("/pioneer2dx/cmd_vel","geometry_msgs/Twist","DataFormat","struct")

while (s(1) ~= map(1).Target(1) || s(2) ~= map(1).Target(2))
temp=s(1)+(s(2)-1)*20;

[~,a]=max(Qmatrix(temp,:));
switch(a)
        case 1
            s(1)=s(1)-1;
        case 2
            s(1)=s(1)+1;
        case 3
            s(2)=s(2)-1;
        case 4
            s(2)=s(2)+1;
end
setDirection(vel,odomSub,a)
moveOneF(vel,odomSub)
i=i+1;
x(i)=s(1);
y(i)=s(2);
end
%setDirection(vel,odomSub,2)
%setDirection(vel,odomSub,3)
%setDirection(vel,odomSub,4)
if ismember("pioneer2dx",getSpawnedModels())
    deleteModel("pioneer2dx");
end
rosshutdown
end
function theta=getTheta(odomSub)
odomMsg = receive(odomSub,3);
pose = odomMsg.Pose.Pose;
quat = pose.Orientation;
angles = quat2eul([quat.W quat.X quat.Y quat.Z]);
theta = rad2deg(angles(1));
end
function setDirection(velPub,odomSub,command)
twist = rosmessage(velPub);
theta=getTheta(odomSub);
switch command
    case 2
        while theta<-0.2 || theta >0.2
        theta=getTheta(odomSub);
        if theta> 0.2
        twist.Angular.Z=-0.3;
        else
        twist.Angular.Z=0.3;
        end
        send(velPub,twist);
        end
    case 4
        while theta<89.8 || theta >90.2
        theta=getTheta(odomSub);
        if theta> 90.2
        twist.Angular.Z=-0.3;
        else
        twist.Angular.Z=0.3;
        end
        send(velPub,twist);
        end
    case 1
        while theta<179.8 || theta >180.2
        theta=getTheta(odomSub);
        if theta<179.8
        twist.Angular.Z=0.3;
        else
        twist.Angular.Z=-0.3;
        end
        send(velPub,twist);
        end
    case 3
        while theta>-89.8 || theta <-90.2
        theta=getTheta(odomSub);
        if theta> -90.2
        twist.Angular.Z=-0.3;
        else
        twist.Angular.Z=0.3;
        end
        
        send(velPub,twist);
        end
 
end
twist.Angular.Z=0;
send(velPub,twist);
end
function [x,y]=getPose(odomSub)
odomMsg = receive(odomSub,3);
pose = odomMsg.Pose.Pose;
x = pose.Position.X;
y = pose.Position.Y;
end

function moveOneF(velPub,odomSub)
[xbeg,ybeg]=getPose(odomSub);
[x,y]=getPose(odomSub);
twist = rosmessage(velPub);
twist.Linear.X=0.3;
send(velPub,twist);
while x>(xbeg-1)&& x<(xbeg+1) && y>(ybeg-1) && y<(ybeg+1)
    [x,y]=getPose(odomSub);
    pause(0.001)
    %send(velPub,twist);
end
twist.Linear.X=0;
send(velPub,twist);
end
