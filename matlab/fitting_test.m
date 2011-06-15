clear
clc

m = 0.2
s= 0.05
mu=log((m^2)/sqrt(s^2+m^2))
sigma=sqrt(log(s^2/(m^2)+1))

x=linspace(0.01,0.5,20);
y=x;

for i=1:20
 y(i)=logncdf(x(i),mu,sigma)+abs(rand(1)*0.0);
end

total_residual = 0;
y_calc=x;

for Mean=linspace(0.1,0.3,100)
 
    for stddev=linspace(0.02,0.06,100)
       
      mu=log((Mean^2)/sqrt(stddev^2+Mean^2));
       sigma=sqrt(log(stddev^2/(Mean^2)+1))  ;    

       for i=1:20
            y_calc(i)=logncdf(x(i),mu,sigma);
       
       end
       
       residuals=corr2(y,y_calc)^2;
       
       
       if residuals > total_residual
            total_residual=residuals;
            final_mean=mu;
            final_stddev=sigma;
            y_plot=y_calc;
       end
   end
end

[m,v] = lognstat(final_mean,final_stddev)
final_mean
final_stddev


for i=1:20
 y_calc(i)=logncdf(x(i),final_mean,final_stddev);
end


figure(1)
plot(x,y)
hold on
plot(x,y_plot)
hold off

r_up=0;
r_down1=0;
r_down2=0;

m=mean(y);
m2=mean(y_calc);


for i=1:20
    r_up=r_up+(y_calc(i)-m2)*(y(i)-m);
    r_down1=r_down1+(y_calc(i)-m2)^2;
    r_down2=r_down2+(y(i)-m)^2;
end



r=r_up/(sqrt(r_down1)*sqrt(r_down2))

R = corr2(y,y_plot)




figure(2)
plot(y,y_calc)


 a = mean([0.086999999999999994, 0.113, 0.13900000000000001])
 b = mean([0.26800000000000002, 0.29399999999999998, 0.31900000000000001])
 
 result=mean([log(a) log(b)])
 
 result2=(log(b)-log(a))/4




