clear
clc

POs=dlmread('/Users/vitorsilva/Documents/PhD/DBELA/Results2.txt');

size=length(POs);
x=POs(:,4);
y=POs(:,6)+0.0000000000001;

for i=1:size
   for j=i+1:size 
    if x(i)>x(j)
        temp1=x(i);
        temp2=y(i);
        x(i)=x(j);
        y(i)=y(j);
        x(j)=temp1;
        y(j)=temp2;
    end
   end
end

x=log(x);
residuals=zeros(1,size);
total_residual = 0;
y_calc=x;

for mean=linspace(-2.2,-1.8,50)
    for stddev=linspace(0.4,0.8,50)
      
       
       for i=1:size
       
            
           y_calc(i)=normpdf(x(i),mean,stddev);
       
       end
       
       residuals=corr2(y,y_calc);
       
       if residuals > total_residual
            total_residual=sum(residuals);
            final_mean=mean;
            final_stddev=stddev;
            y_plot=y_calc;
       end
       
    end
end

final_mean
final_stddev



figure(1)
scatter(x,y)
hold on
plot(x,y_plot)
hold off