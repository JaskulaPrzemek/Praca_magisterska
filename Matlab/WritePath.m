function WritePath(Qmatrix,map)
s=map(1).StartingPoint;
i=1;
x(1)=s(1);
y(1)=s(2);
while (s(1) ~= map(1).Target(1) || s(2) ~= map(1).Target(2))
    hold on;
 

temp=s(1)+(s(2)-1)*20;

[~,a]=max(Qmatrix(temp,:));
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
i=i+1;
x(i)=s(1);
y(i)=s(2);
end
plot(x,y);
end