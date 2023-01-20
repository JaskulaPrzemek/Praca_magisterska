function [Qmatrix]=FPA(map,p,Gazebo)
gamma=0.5;
Iterations=1000;
population=initialpopulation(map);
Qmatrix=zeros(map(1).Size(1)*map(1).Size(2),4);
PopSize=size(population,1);
nextPopulation=population;
Fittnes=zeros(1,PopSize);
BestFitness=0;
for j=1:Iterations
    for i=1:PopSize
    [Fittnes(i),Qmatrix]=fitness(population(i,:),Qmatrix,map,Gazebo);
    end
    [tmpBest,I]=max(Fittnes);
    if(tmpBest>=BestFitness)
        BestFitness=tmpBest;
        best=population(I,:);
    end
    for i=1:PopSize
        temp=[0,0];
        while(temp(1)<1||temp(1)>20||temp(2)<1||temp(2)>20)
            if(rand()>p)
            LevySteps=levy(2,1.4);
            temp=population(i,:)+gamma*LevySteps.*(population(i,:)-best);
            nextPopulation(i,:)=round(temp);
            else
            j=randi(PopSize);
            k=randi(PopSize);
            temp=population(i,:)+rand()*(population(j,:)-population(k,:));
            nextPopulation(i,:)=round(temp);
            end
        end
    end
    population=nextPopulation;
end
end

function [population]=initialpopulation(map)
populationSize=10;
Lx=1;
Ux=map(1).Size(1);
Ly=1;
Uy=map(1).Size(2);
population=zeros(populationSize,2);
for i=1:populationSize
    population(i,1)=randi([Lx,Ux]);
    population(i,2)=randi([Ly,Uy]);
    ObstaclesNR=size({map.Polygons},2);
    flag =0;
    while(~flag)
        flag=1;
            if(map(1).Cmap(population(i,1),population(i,2))==-1)
                flag=0;
                population(i,1)=randi([Lx,Ux]);
                population(i,2)=randi([Ly,Uy]);
                break;
            end

    end
end

end
function [z] = levy(m,beta)
%levy function comes from Multiobjective cuckoo search for design optimization, by Yang

% m     -> Number of Dimensions 
% beta  -> Power law index  % Note: 1 < beta < 2


    num = gamma(beta)*sin(pi*beta/2); % used for Numerator 
    
    den = gamma((1+beta)/2)*beta*2^((beta-1)/2); % used for Denominator

    sigma_u = (num/den)^(1/beta);% Standard deviation

    u = random('Normal',0,sigma_u^2,1,m); 
    
    v = random('Normal',0,1,1,m);

    z = u./(abs(v).^(1/beta));
end
function [MaxQ,Qmatrix]=fitness(State,Qmatrix,Map,Gazebo)
    for i=1:4
    if Gazebo
    spawnPioneer(State(1),State(2));
    end
        [r,Sp]=Reinforcement(State,i,Map,Gazebo);
        Qmatrix=Update(State,Sp,i,r,Qmatrix);
    if Gazebo
    deleteModel("pioneer2dx");
    end
    end
    MaxQ=max(Qmatrix(State(1)+(State(2)-1)*20,:));
end
  function [Q]= Update(s,Sp,a,r,Qmatrix)
   alpha=0.2;
   gamma=0.8;
   Pos=s(1)+(s(2)-1)*20;
   Qmatrix(Pos,a)=(1-alpha)*Qmatrix(Pos,a)+alpha*(r+gamma*max(Qmatrix(Sp(1)+(Sp(2)-1)*20,:)));
   Q=Qmatrix;
   end
     
