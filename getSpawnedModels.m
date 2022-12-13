function out=getSpawnedModels()
    obj.ModelListClient = rossvcclient('gazebo/get_world_properties','DataFormat','struct');
     serviceMsg = rosmessage(obj.ModelListClient);
     msg = call(obj.ModelListClient, serviceMsg);     
       out = msg.ModelNames;
end