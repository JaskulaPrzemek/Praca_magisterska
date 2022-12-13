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