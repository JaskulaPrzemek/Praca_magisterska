function deleteModel(modName)
            obj.RemoveModClient = rossvcclient('gazebo/delete_model','DataFormat','struct');
            serviceMsg = rosmessage(obj.RemoveModClient);
            serviceMsg.ModelName = convertStringsToChars(modName);
            msg = call(obj.RemoveModClient,serviceMsg);
            if ~msg.Success
                error('Service call to remove model failed')
            end
end