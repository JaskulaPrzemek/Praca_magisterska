function [QMatrix]=FPA(map,function,p)
gamma=0.5;
population=initialpopulation(map);
PopSize=size(population,1);
nextPopulation=population;
    for i=1:PopSize
    Fittnes(i)=funtion(population(i,:));
    end
    [Fmax,I]=max(Fittnes);
    best=population(I,:);
    for i=1:PopSize
        if(rand()>p)
        LevySteps=levy(2,1.4);
        temp=population(i,:)+gamma*LevySteps.*(population(i,:)-best);
        nextPopulation(i,:)=temp;
        else
        j=randi(PopSize);
        k=randi(PopSize);
        temp=population(i,:)+rand()*(population(j,:)-population(k,:))
        nextPopulation(i,:)=temp;
        end
    end
end

function [population]=initialpopulation(map)
populationSize=50;
Lx=1;
Ux=map(1).size(1);
Ly=1;
Uy=map(1).size(2);
population=zeros(populationSize,2);
for i=1:populationSize
    population(i,1)=randi([Lx,Ux]);
    population(i,2)=randi([Ly,Uy]);
    ObstaclesNR=size({map.Polygons},2);
    flag =1;
    while(flag)
        for j=1:ObstaclesNR
            if(isinterior(map(j).Polygons,population(i,:)))
                flag=0;
                population(i,1)=randi([Lx,Ux]);
                population(i,2)=randi([Ly,Uy]);
                break;
            end
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
     