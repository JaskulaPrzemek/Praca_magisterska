function [r,s1]=Reinforcement(s,a,Map)
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
    if s(1)<=0 ||s(1)>20 || s(2)<=0 ||s(2)>20
        r=-1;
        return;
    end
  ObstaclesNR=size({Map.Polygons},2);
 
for i=1:ObstaclesNR
   if(isinterior(Map(i).Polygons,s)==1)
      r=-1;
      return;
   end
end
if s==Map(1).Target
   r=2;
   s1=s;
   return;
end
%if norm(s-Map(1).Target)>norm(s1-Map(1).Target)
%    r=0.2;
%end
%r=sqrt((Map(1).Target(1)-s(1))^2+(Map(1).Target(2)-s(2))^2);
s1=s;

end