function ViewMap(Map)
ObstaclesNR=size({Map.Polygons},2);
hold on;
grid on;
s=Map.Size;
for i=1:ObstaclesNR
   plot(Map(i).Polygons);
   
end
axis([0,s(1),0,s(2)]);
hold off;
end