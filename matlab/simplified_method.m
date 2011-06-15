clear
clc

IML10=zeros(10000,1);
IML90=zeros(10000,1);
Means=zeros(10000,1);
Means_calc=zeros(10000,1);
Error=zeros(100);
pos=1;
pos_mean=1;

for mean=linspace(0.1,3,100)
   pos_std=1;
   for stddev=linspace(0.01,1,100) 
    
       mu=log((mean^2)/sqrt(stddev^2+mean^2));
       sigma=sqrt(log(stddev^2/(mean^2)+1));

       
        
       IML10(pos)=logninv(0.10,mu,sigma);
       IML90(pos)=logninv(0.90,mu,sigma);
       Means(pos)=logninv(0.50,mu,sigma);
       Means_calc(pos)=(logninv(0.10,mu,sigma) + logninv(0.90,mu,sigma))/2;
          a=(logninv(0.10,mu,sigma) + logninv(0.90,mu,sigma))/2;
b=logninv(0.50,mu,sigma);
       Error(pos_mean,pos_std)= round((abs(a-b))/a*100)  ;
 
       
       pos=pos+1;
       
   pos_std=pos_std+1;    
   end
   pos_mean=pos_mean+1;
end

x=linspace(0.001,3,1000);
y=x;
mean=0.1;
stddev=0.5; 
mu=log((mean^2)/sqrt(stddev^2+mean^2));
sigma=sqrt(log(stddev^2/(mean^2)+1));

a=(logninv(0.10,mu,sigma) + logninv(0.90,mu,sigma))/2
b=logninv(0.50,mu,sigma)

round((abs(a-b))/a*100)

for i=1:100
    y(i)=logncdf(x(i),mu,sigma);
end

figure(1)
plot(x,y)
ylim([0,1])
xlim([0,0.2])

figure(2)
scatter(Means, Means_calc)

mean=linspace(0.1,3,100);
stddev=linspace(0.01,1,100); 

figure(3)
surfc(mean,stddev,Error);
shading interp
colorbar('location','SouthOutside')
