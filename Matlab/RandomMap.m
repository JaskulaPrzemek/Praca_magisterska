function [Map]=RandomMap()
	Map.Size= [20,20];
    Map.StartingPoint=[randi([2,8]),randi([2,8])];
    Map.Target =[randi([13,19]),randi([3,19])];
    NrOfObstacles=randi([4,13]);
    Map(1).Cmap=2*ones(Map(1).Size(1),Map(1).Size(2));
    for i=1:NrOfObstacles
        NrOfVertices=randi([3,7]);
        for j=1:NrOfVertices
            flag=false;
            while ~flag
                x=randi([1,19]);
                y=randi([1,19]);
                if(x<20&&y<20&&Map(1).Cmap(x+1,y+1)==-1)
                    continue;
                end
                if(x<20&&Map(1).Cmap(x+1,y)==-1||y<20&&Map(1).Cmap(x,y+1)==-1)
                    continue;
                end
                if (x>2)
                    if(y>2)
                    end
                end
                if(isequal([x,y],Map.StartingPoint) || isequal([x,y],Map.Target)||Map(1).Cmap(x,y)==-1)
                    continue;
                else
                    if(j==1)
                        Map(i).Obstacles(j,1)=x;
                        Map(i).Obstacles(j,2)=y;
                        Map(1).Cmap(x,y)=-1;
                        flag=true;
                    else
                        if(x>Map(i).Obstacles(j-1,1)+2||x<Map(i).Obstacles(j-1,1)-2)
                         continue;
                        end
                        if(y>Map(i).Obstacles(j-1,2)+2||y<Map(i).Obstacles(j-1,2)-2)
                         continue;Map(1).Cmap(x,y)==-1
                        end
                        Map(i).Obstacles(j,1)=x;
                        Map(i).Obstacles(j,2)=y;
                        Map(1).Cmap(x,y)=-1;
                        flag=true;
                    end
                end
            end
        end
        Map(i).Polygons=polyshape(Map(i).Obstacles);
        for k=1:Map(1).Size(1)
            for l=1:Map(1).Size(2)
                if(isinterior(Map(i).Polygons,[k,l]))
                        Map(1).Cmap(k,l)=-1;
                        break;
                end
            end
        end
    end
    ViewMap(Map);
    end
 
