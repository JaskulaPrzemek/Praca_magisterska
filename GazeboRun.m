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

[~,a]=max(Qmatrix(temp,:))
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
theta=getTheta(odomSub)
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

function deleteModel(modName)
            obj.RemoveModClient = rossvcclient('gazebo/delete_model','DataFormat','struct');
            serviceMsg = rosmessage(obj.RemoveModClient);
            serviceMsg.ModelName = convertStringsToChars(modName);
            msg = call(obj.RemoveModClient,serviceMsg);
            if ~msg.Success
                error('Service call to remove model failed')
            end
end
function spawnPioneer(x,y)
    obj.SpawnClient = rossvcclient('gazebo/spawn_sdf_model','DataFormat','struct');
    serviceMsg = rosmessage(obj.SpawnClient);
    buildModel.ModelObj = parseFile(matlab.io.xml.dom.Parser, '/home/pszemek/Desktop/Projekt_Specjalnosciowy/catkin_ws/src/pioneer2dx_test/model.sdf');
    s = writeToString(matlab.io.xml.dom.DOMWriter, buildModel.ModelObj);
    serviceMsg.ModelXml = s;

        model = buildModel.ModelObj.getElementsByTagName('model');
        modName = char(model.item(0).getAttribute('name'));
                
            
            list = getSpawnedModels();
            
            try
                if isequal(class(list{2}),'double')
                    list(2) = [];
                end
            catch
            end
            
            objnum = 0;
            Name = modName;
            while(1)
                
                
                ind = find(ismember(list,modName));
                
                if (ind)
                    modName = [Name '_' num2str(objnum)];
                    objnum = objnum+1;
                else
                    break
                end
            end
            
            serviceMsg.ModelName = modName;
            
            % Default values for position and orientation
            orientation = [1 0 0 0];
            position = [x y 0.1]; 
       pose = rosmessage('geometry_msgs/Pose','DataFormat','struct');
            point = pose.Position;
            point.X = position(1);
            point.Y = position(2);
            point.Z = position(3);
            
            orient = pose.Orientation;
            
            orient.W = orientation(1);
            orient.X = orientation(2);
            orient.Y = orientation(3);
            orient.Z = orientation(4);
            
            pose.Position = point;
            pose.Orientation = orient;
            
            serviceMsg.InitialPose = pose;
            
            % Set reference frame for spawn to absolute coordinates
            serviceMsg.ReferenceFrame = 'world';
            
            msg = call(obj.SpawnClient, serviceMsg);
            
end

function out=getSpawnedModels()
    obj.ModelListClient = rossvcclient('gazebo/get_world_properties','DataFormat','struct');
     serviceMsg = rosmessage(obj.ModelListClient);
     msg = call(obj.ModelListClient, serviceMsg);     
       out = msg.ModelNames;
end