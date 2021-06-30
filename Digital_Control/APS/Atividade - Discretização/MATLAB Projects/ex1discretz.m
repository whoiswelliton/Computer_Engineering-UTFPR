%%Defini��es iniciais
figure
hold on
T=0.01;
z=tf('z',T);
s=tf('s');
%% F.T. em tempo cont�nuo
F=(s+3)/(s*(s^2+10*s+100))
impulse(F)
%% Discret. M�todo Forward
s=(z-1)/T;
F_For=(s+3)/(s*(s^2+10*s+100))
impulse(F_For)
 %% Discret. M�todo Backward
s=(z-1)/(T*z);
F_Bac=(s+3)/(s*(s^2+10*s+100))
impulse(F_Bac)
 %% Discret. M�todo Trapezoidal
s=2/T*(z-1)/(z+1);
F_Tra=(s+3)/(s*(s^2+10*s+100))
impulse(F_Tra)
 %% Discret. M�todo c2d
F_c2d=c2d(F,T);
impulse(F_c2d)
%% Ajustes no gr�fico
set(findall(gcf,'Type','line'),'LineWidth',2)
grid on
legend