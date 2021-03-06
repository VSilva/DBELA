clear
clc


Values=dlmread('/Users/vitorsilva/Documents/PhD/Fragility Functions Turkey/Values.txt');
no=length(Values);

Means=zeros(1,no);
Sigmas=zeros(1,no);

for i=1:no
   Means(i)=exp(Values(i,1)+Values(i,2)^2/2);
   Sigmas(i)=sqrt(   (exp(Values(i,1)^2)-1)*exp(2*Values(i,1)+Values(i,2)^2));
end

Mean_mean=mean(Means)
StdDev_mean=std(Means)
Mean_StdDev=mean(Sigmas)
StdDev_StdDev=std(Sigmas)

x=linspace(Mean_mean-3*StdDev_mean,Mean_mean+3*StdDev_mean,100);
y=normpdf(x,Mean_mean,StdDev_mean);
figure(1)
[Y,X]=HIST(Means,20);
bar(X,Y/(no*(X(2)-X(1))),1,'red');
hold on
plot(x,y,'LineWidth',2);
hold off

x=linspace(Mean_StdDev-3*StdDev_StdDev,Mean_StdDev+3*StdDev_StdDev,100);
y=normpdf(x,Mean_StdDev,StdDev_StdDev);
figure(2)
[Y,X]=HIST(Sigmas,20);
bar(X,Y/(no*(X(2)-X(1))),1,'red');
hold on
plot(x,y,'LineWidth',2);
hold off

