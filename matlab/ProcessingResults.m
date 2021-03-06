clear
clc

data=dlmread('/Users/vitorsilva/Documents/PhD/DBELA/Results3.txt');
POs=dlmread('/Users/vitorsilva/Documents/PhD/DBELA/Results2.txt');
PEs=dlmread('/Users/vitorsilva/Documents/PhD/DBELA/Results.txt');

sizes=sum(data'>0);

LS1data=zeros(1,sizes(1));
LS2data=zeros(1,sizes(2));
LS3data=zeros(1,sizes(3));
pos1=1;
pos2=1;
pos3=1;

for i=1:length(data)
    if data(1,i)>0
       LS1data(pos1)=data(1,i);
       pos1=pos1+1;
    end
    if data(2,i)>0
       LS2data(pos2)=data(2,i);
       pos2=pos2+1;
    end
    if data(3,i)>0
       LS3data(pos3)=data(3,i);
       pos3=pos3+1;
    end
end

maxIML=max([max(LS1data),max(LS2data),max(LS3data)]);

par=lognfit(LS1data);
LS1mu=par(1);
LS1sigma=par(2);

par=lognfit(LS2data);
LS2mu=par(1);
LS2sigma=par(2);

par=lognfit(LS3data);
LS3mu=par(1);
LS3sigma=par(2);

x=linspace(0.0000000001,maxIML,100);

figure(1)
LS1y=zeros(1,100);
LS2y=zeros(1,100);
LS3y=zeros(1,100);

for i=1:100
   LS1y(i)=logncdf(x(i),LS1mu,LS1sigma)
   LS2y(i)=logncdf(x(i),LS2mu,LS2sigma)
   LS3y(i)=logncdf(x(i),LS3mu,LS3sigma)
end

 figure (1)
 plot(x,LS1y,x,LS2y,x,LS3y)
 
 figure (2)
 SUBPLOT(3,1,1)
 plot(x,LS1y)
 hold on
scatter(PEs(:,4),PEs(:,5))
 hold off
  logxx=log(PEs(:,4))
  
 SUBPLOT(3,1,2)
 plot(x,LS2y)
 hold on
 scatter(PEs(:,4),PEs(:,6))
 hold off
 
 SUBPLOT(3,1,3)
 plot(x,LS3y)
 hold on
 scatter(PEs(:,4),PEs(:,7))
 hold off
 
 logx=log(PEs(:,4))
 yy=POs(:,6)
 
 figure(3)
 scatter(logx,yy)
 
 sigma=sqrt(0.6516^2/2)
 mu=-2.147

y=x

for i=1:100
   y(i)=logncdf(x(i),mu,sigma)
end
 figure (4)
 plot(x,y)
 hold on
scatter(PEs(:,4),PEs(:,5))
 