function [r,s1]=Reinforcement(s,a,Map,Gazebo)
r=0;
 s1=s;
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
if Gazebo
[r,s1]=goToPoint(s,Map(1).Target);
return
end
    if s(1)<=0 ||s(1)>20 || s(2)<=0 ||s(2)>20
        r=-1;
        return;
    end
 

   if(Map(1).Cmap(s(1),s(2))==-1)
      r=-1;
      return;
   end

if s==Map(1).Target
   r=2;
   s1=s;
   return;
end

s1=s;

end