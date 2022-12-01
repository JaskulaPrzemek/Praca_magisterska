function [r,s1]=goToPoint(targetPoint,mapTarget)
odomSub = rossubscriber("/pioneer2dx/odom","DataFormat","struct");
vel = rospublisher("/pioneer2dx/cmd_vel","geometry_msgs/Twist","DataFormat","struct");
sensorSub=rossubscriber("/sonar","DataFormat","struct");
startpoint=zeros(1,2);
setDirection(vel,odomSub,targetPoint)
[~,startpoint(1),startpoint(2)]=getOdom(odomSub);
sensorMsg=receive(sensorSub,3);
flag=0;
twist = rosmessage(vel);
while(sensorMsg.Range_>0.1)
    sensorMsg=receive(sensorSub,3);
    [theta,x,y]=getOdom(odomSub);
    distance=sqrt((x-targetPoint(1))^2+(y-targetPoint(2))^2);
    if distance<0.1
        flag=1;
        twist.Angular.Z=0;
        twist.Linear.X=0;
        send(vel,twist);
        break;
    end
    if (targetPoint(1)-x)==0
        if(y>targetPoint(2))
        targetAngle=-90;
        else
        targetAngle=90;  
        end
    else
        targetAngle=rad2deg(atan((targetPoint(2)-y)/(targetPoint(1)-x)));
        if(x>targetPoint(1))
            targetAngle=targetAngle+180;
        end
    end
    twist.Angular.Z=(targetAngle-theta)/90;
    if distance<0.1
    twist.Linear.X=0.05;
    else
        if distance>0.4
            twist.Linear.X=0.4;
        else
            twist.Linear.X=distance;
        end
    end
    send(vel,twist);
end
twist.Angular.Z=0;
twist.Linear.X=0;
send(vel,twist);
if ~flag
    [theta,x,y]=getOdom(odomSub);
    distance=sqrt((x-startpoint(1))^2+(y-startpoint(2))^2);
    twist.Angular.Z=0;
    while distance>0.05
        [theta,x,y]=getOdom(odomSub);
        distance=sqrt((x-startpoint(1))^2+(y-startpoint(2))^2);
        targetAngle=rad2deg(atan((startpoint(2)-y)/(startpoint(1)-x)));
        if(x>targetPoint(1))
            targetAngle=targetAngle+180;
        end
        %targetAngle=targetAngle+180;
        twist.Angular.Z=(targetAngle-theta)/180;
        twist.Linear.X=-0.1;
        send(vel,twist)
    end
twist.Angular.Z=0;
twist.Linear.X=0;
send(vel,twist);
r=-1;
s1=startpoint;
else
    if targetPoint==mapTarget
        s1=targetPoint;
        r=2;
    else
        r=0;
        s1=targetPoint;
    end
end
end

function [theta,x,y]=getOdom(odomSub)
odomMsg = receive(odomSub,3);
pose = odomMsg.Pose.Pose;
quat = pose.Orientation;
angles = quat2eul([quat.W quat.X quat.Y quat.Z]);
theta = rad2deg(angles(1));
x = pose.Position.X;
y = pose.Position.Y;
end
function setDirection(velPub,odomSub,point)
twist = rosmessage(velPub);
[theta,x,y]=getOdom(odomSub);
distance=sqrt((x-point(1))^2+(y-point(2))^2);
if distance >0.05
    if (point(2)-y)==0
        if(y>point(2))
        targetAngle=-90;
        else
        targetAngle=90;  
        end
    else
    targetAngle=rad2deg(atan((point(2)-y)/(point(1)-x)));
    if(x>point(1))
    targetAngle=targetAngle+180;
    end
    end
else
    targetAngle=theta;
end
        while theta<targetAngle-0.2 || theta >targetAngle+0.2
        [theta,~,~]=getOdom(odomSub);
        if theta> targetAngle+0.2
        twist.Angular.Z=-0.3;
        else
        twist.Angular.Z=0.3;
        end
        send(velPub,twist);
        end
twist.Angular.Z=0;
send(velPub,twist);
end
