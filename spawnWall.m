function spawnWall(x1,y1,x2,y2)
midx=(x1+x2)/2;
midy=(y1+y2)/2;
lenght=sqrt((x1-x2)^2 +(y1-y2)^2);
if (x2-x1)==0
angle=pi/2;
else
angle=atan((y2-y1)/(x2-x1));
end
sizeval=string(num2str(lenght,6)) +" 0.01 2.5";
pose1val=num2str(midx,6)+" " +num2str(midy,6)+" 0 0 -0 0";
pose2val="-0 0 0 0 -0 "+num2str(angle,6);
obj.SpawnClient = rossvcclient('gazebo/spawn_sdf_model','DataFormat','struct');
serviceMsg = rosmessage(obj.SpawnClient);
buildModel.ModelObj = parseFile(matlab.io.xml.dom.Parser, '/home/pszemek/Desktop/Projekt_Specjalnosciowy/catkin_ws/src/Wall/model.sdf');
posy=buildModel.ModelObj.getElementsByTagName("pose");
posy.item(0).setTextContent(pose1val);
posy.item(3).setTextContent(pose2val);
sizy=buildModel.ModelObj.getElementsByTagName("size");
sizy.item(0).setTextContent(sizeval )
sizy.item(1).setTextContent( sizeval)

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
          orientation = [1 0 0 0];
            position = [0 0 0]; 
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
