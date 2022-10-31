function [Map]=CreateMap(type)
switch type
case -1 %empty Map
    Map.Size= [20,20];
    Map.StartingPoint=[2,16];
    Map.Target=[19,16];
case 0 %map with one obstacle
    Map.Size= [20,20];
    Map.StartingPoint=[2,16];
    Map.Target=[19,16];
    Map(1).Obstacles=[10,16,2]; 
case 1
   Map.Size= [20,20];
   Map.StartingPoint=[2,16];
   Map.Target=[19,11];
   Map(1).Obstacles=[2,9;2,12;4,12];
   Map(2).Obstacles=[4,6,1];
   Map(3).Obstacles=[3,3;4,2;6,2;7,3];
   Map(4).Obstacles=[3,14;2,18;5,18];
   Map(5).Obstacles=[6,12;8,13;10,12;9,14;10,15;9,16;8,18;7,16;6,15;7,14];
   Map(6).Obstacles=[9,4;11,4;11,8;12,8;12,10;10,10;10,6;9,6];
   Map(7).Obstacles=[18,14;16,18;20,14];
   Map(8).Obstacles=[16,10;15,12;18,12];
   Map(9).Obstacles=[13,3;14,3;15,2;16,3;17,2;18,4;17,5;15,4;14,5;13,5];
  
otherwise
    Map.Size= [20,20];
end

%create polygons for ease of checking int point
ObstaclesNR=size({Map.Obstacles},2);
for i=1:ObstaclesNR
    if(size(Map(i).Obstacles)==[1,3])
        n=100;
        xc=Map(i).Obstacles(1);
        yc=Map(i).Obstacles(2);
        r=Map(i).Obstacles(3);
        theta = (0:n-1)*(2*pi/n);
        x = xc + r*cos(theta);
        y = yc + r*sin(theta);
        Map(i).Polygons=polyshape(x, y);
    else
        Map(i).Polygons=polyshape(Map(i).Obstacles); 
    end
   
end
end