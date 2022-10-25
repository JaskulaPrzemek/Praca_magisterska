PossibleActions=[1,2,3,4];%lewo,prawo,dol,gora
clear;
Map=CreateMap(1);
Qmatrix=zeros(Map(1).Size(1)*Map(1).Size(2),4);
ViewMap(Map);
State=Map.StartingPoint;
for i=1:100
    State=Map.StartingPoint;
    step=0;
while(State(1) ~= Map(1).Target(1)||State(2) ~= Map(1).Target(2))
    
   a=NextAction(State,Qmatrix);
   [r,Sp]=Reinforcement(State,a,Map);
   Qmatrix=Update(State,Sp,a,r,Qmatrix);
   State=Sp;
   step=step+1;
   if i==100
        Path(step).step=State;
    end
    end
Steps(i)=step;
end
t=312;
plot(Steps);
xlabel("iterations");
ylabel("Steps");
   function [a]=NextAction(s,Qmatrix)
   e=rand();
    if(e<0.01)
        a=randi(4);
    else
   Pos(1).s=[s(1)-1,s(2)];
  Pos(2).s=[s(1)+1,s(2)];
  Pos(3).s=[s(1),s(2)-1];
  Pos(4).s=[s(1),s(2)+1];
  tempmax=0;
    for i=1:4
        if(Pos(i).s(1)<=0||Pos(i).s(1)>20||Pos(i).s(2)<=0||Pos(i).s(2)>20)
            Q(i)=-100;
        else
            Q(i)=Qmatrix(Pos(i).s(1)+(Pos(i).s(2)-1)*20,i);
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