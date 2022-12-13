function [Steps]=Qlearning(MapNR,isFPA,Egreedy,Render,Gazebo)
%PossibleActions=[1,2,3,4];
if(Gazebo)
    try
        rosnode list;
    catch exp   % Error from rosnode list
        rosinit;  % only if error: rosinit
    end
end
Map=CreateMap(MapNR,Gazebo);

if Render
ViewMap(Map);
end
if(isFPA)
Qmatrix=FPA(Map,0.5,Gazebo);
else
  Qmatrix=zeros(Map(1).Size(1)*Map(1).Size(2),4);  
end
Steps=zeros(1,100);
for i=1:100
    State=Map.StartingPoint;
    step=0;
    spawnPioneer(State(1),State(2))
while(State(1) ~= Map(1).Target(1)||State(2) ~= Map(1).Target(2))
    
   a=NextAction(State,Qmatrix,Map,Egreedy);
   [r,Sp]=Reinforcement(State,a,Map,Gazebo);
   Qmatrix=Update(State,Sp,a,r,Qmatrix);
   State=Sp;
   step=step+1;
    %Path(step).step=State;
end
if ismember("pioneer2dx",getSpawnedModels())
    deleteModel("pioneer2dx");
end
Steps(i)=step;
end
if Render
WritePath(Qmatrix,Map);
end
if Gazebo
GazeboRun(Qmatrix,Map)
end    
end
function [a]=NextAction(s,Qmatrix,Map,Egreedy)
   e=rand();
   
    if(e<Egreedy)
        a=randi(4);
    else
        Pos(1).s=[s(1)-1,s(2)];
        Pos(2).s=[s(1)+1,s(2)];
        Pos(3).s=[s(1),s(2)-1];
        Pos(4).s=[s(1),s(2)+1];
     for i=1:4
        if(Pos(i).s(1)<=0||Pos(i).s(1)>20||Pos(i).s(2)<=0||Pos(i).s(2)>20)
            Q(i)=-100;
        else
            if(Pos(i).s(1)==Map(1).Target(1)&&Pos(i).s(2)==Map(1).Target(2))
                Q(i)=100;
            else
                Q(i)=max(Qmatrix(Pos(i).s(1)+(Pos(i).s(2)-1)*20,:));
            end

        end
    end
    
    maxval = max(Q);
    idx = find(Q == maxval);
    if size(idx,2)>1
        temp =randi(size(idx,2));
        a=idx(temp);
        return
    end
    a=idx;
    end
   end
   function [Q]= Update(s,Sp,a,r,Qmatrix)
   alpha=0.2;
   gamma=0.8;
   Pos=s(1)+(s(2)-1)*20;
   Qmatrix(Pos,a)=(1-alpha)*Qmatrix(Pos,a)+alpha*(r+gamma*max(Qmatrix(Sp(1)+(Sp(2)-1)*20,:)));
   Q=Qmatrix;
   
   end