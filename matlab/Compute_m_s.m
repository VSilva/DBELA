clear
clc

PEs=dlmread('/Users/vitorsilva/Documents/PhD/DBELA/Results.txt');
POs=dlmread('/Users/vitorsilva/Documents/PhD/DBELA/Results2.txt');
Parameters=dlmread('/Users/vitorsilva/Documents/PhD/DBELA/curves.txt');

size=length(POs);
x=log(POs(:,1));
y=POs(:,6)+0.0000000000001;
y2=PEs(:,5)+0.0000000000001;

for i=1:size
   for j=i+1:size 
    if x(i)>x(j)
        temp1=x(i);
        temp2=y(i);
        temp3=y2(i);
        x(i)=x(j);
        y(i)=y(j);
        y2(i)=y2(j);
        x(j)=temp1;
        y(j)=temp2;
        y2(j)=temp3;
    end
   end
end

% residuals=zeros(1,size);
% total_residual = 0;
% y_calc=x;
% 
% 
% for mean=linspace(-2.3,-2.1,20)
%     for stddev=linspace(0.6,0.9,20)
%        
%   %    mu=log((mean^2)/sqrt(stddev^2+mean^2));
%   %    sigma=sqrt(log(stddev^2/(mean^2)+1));
%       mu=mean;
%       sigma=stddev;
%        
%        for i=1:size
%        
%      %   residuals(i)=abs(1-logncdf(x(i),mu,sigma)/y(i))^2;
%    
%         y_calc(i)=normpdf(x(i),mu,sigma);
%        
%        end
%        
%        residuals=abs(corr2(y,y_calc));
%        
%        if sum(residuals) > total_residual
%             total_residual=residuals;
%             final_mean=mu;
%             final_stddev=sigma;
%             y_plot = y_calc;
%        end
%        
%     end
% end
% 
% 
% final_mean
% final_stddev
% 
% 
% total_residual = inf;
% 
% 
% for mean=linspace(-2.3,-2.1,20)
%     for stddev=linspace(0.6,0.9,20)
%        
%   %    mu=log((mean^2)/sqrt(stddev^2+mean^2));
%   %    sigma=sqrt(log(stddev^2/(mean^2)+1));
%       mu=mean;
%       sigma=stddev;
% 
%        
%        for i=1:size
%          y_calc(i)=normcdf(x(i),mu,sigma);
%         residuals(i)=abs(normcdf(x(i),mu,sigma)-y2(i));   
%        end
%        
%     %   residuals=abs(corr2(y2,y_calc));
%            
%        
%         if sum(residuals) < total_residual
%           total_residual=sum(residuals);
%           final_mean2=mu;
%           final_stddev2=sigma;
%           y_plot2 = y_calc;
%        end
%      end
% end
% 
% final_mean2
% final_stddev2
% 
% 
% 
%     for i=1:size
%     
%          y_Up(i)=normcdf(x(i),-2.2352-1.645*(0.8482),0.8482);
%          y_Down(i)=normcdf(x(i),-2.2352+1.645*(0.8482),0.8482);
%   
%     end
% 
% 
% figure(1)
% scatter(x,y)
% hold on 
% plot (x,y_plot)
% hold off
% 
% figure(2)
% scatter(exp(x),y2)
% hold on 
% plot (exp(x),y_plot2)
% plot (exp(x),y_Up)
% plot (exp(x),y_Down)
% hold off
% 
% yLS1=x;
% 
% for i=1:size
%     yLS1(i)=normcdf(x(i),-2.1876452512619227, 0.86186519661045335);
% end
% 
% figure(3)
% scatter(PEs(:,4),PEs(:,5))
% hold on
% plot(exp(x),yLS1)
% hold off

yLS1=x;
yLS2=x;
yLS3=x;

x=linspace(0.0000000001,1.5,size);
x=log(x);

for i=1:size
    yLS1(i)=normcdf(x(i),-1.74822208283, 0.565799498764);
    yLS2(i)=normcdf(x(i),-0.836008551492, 0.547161092517);
    yLS3(i)=normcdf(x(i),-0.575038020153, 0.679433596065);
end

figure(4)
% scatter(PEs(:,4),PEs(:,7),'*','red')
hold on
 scatter(PEs(:,4),PEs(:,7),'o','blue')
%scatter(PEs(:,4),PEs(:,5),'+','red')
%plot(exp(x),yLS1,'Color','red','LineWidth',2)
xlim([0,1.5])
plot(exp(x),yLS3,'blue','LineWidth',2);
%plot(exp(x),yLS3,'red')
%legend('LS1','LS2','LS3','location','southeast')
hold off

% 
% R=corr2(y,y_plot)
% R2=corr2(y2,y_plot2)
%  