clear
clc

VulFunc1=dlmread('/Users/vitorsilva/Documents/PhD/DBELA/vulnerabilityfunctionBase.txt');
VulFunc2=dlmread('/Users/vitorsilva/Documents/PhD/DBELA/vulnerabilityfunctionIMP2.txt');
% VulFunc3=dlmread('/Users/vitorsilva/Documents/PhD/DBELA/vulnerabilityfunctionIMP2.txt');


imls = VulFunc1(1,:);
lossRatios1 =VulFunc1(2,:);
lossRatios2 =VulFunc2(2,:);
lossRatios3 =(VulFunc2(2,:)-(VulFunc1(2,:)-VulFunc2(2,:)));
% lossRatios3 =(VulFunc2(2,:)+VulFunc1(2,:))/2;

figure(1)
plot(imls,lossRatios1,'LineWidth',2,'Color','red');
hold on
plot(imls,lossRatios2,'LineWidth',2,'Color','blue');
plot(imls,lossRatios3,'LineWidth',2,'Color','green');
xlim([min(imls),max(imls)])
ylim([0,1])
xlim([0,1])
xlabel('Peak Ground Acceleration (g)')
% ylabel('Fatality rate')
ylabel('Loss ratio')
legend('SC1','SC2','SC3','Location','SouthEast')
hold off