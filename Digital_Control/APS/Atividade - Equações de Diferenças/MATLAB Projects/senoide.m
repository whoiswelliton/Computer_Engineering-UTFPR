%% Sinal de entrada = Sinal Senoidal

clc;
N = 100;        % Qt de de pontos de simula��o
A = 5;          % amplitude da senoide
Ts = 1e-1;      % per�odo de amostragem
NA = 40;        % numero de amostras/ciclo
NC = 3;         % n�mero de ciclos
To = NA*Ts;     % per�odo fundamental
fo = 1/To;      % frequ�ncia fundamental
NT = NA*NC;     % n�mero total de pontos
TT = NT*Ts;     % tempo total do gr�fico

t=0:Ts:TT;
y = zeros(1,N+2);    %Ra�zes de y(n)
x = A*sin(2*pi*fo*t); %Onda senoidal

%La�o de repeti��o
%Contador iniciando em 3 devido ao deslocamento y(n-2) 
for n=3:N 
    %Equa��o de diferen�as y(n) obtida
    y(n) = (8*y(n-1) - 3*y(n-2) + 4*x(n-1) + x(n-2))/10;
    
    %Teste com outros coeficientes 
    %y(n) = (6*y(n-1) - 1*y(n-2) + 3*x(n-1) + 0.8*x(n-2))/10;
end
%Plotando os 3 gr�ficos
figure
subplot(2,2,1); stem(x); xlim([0 100]);
title('Entrada x[n]');
subplot(2,2,2); stem(y, 'r'); xlim([0 100]);
title('Sa�da y[n]');
subplot(2,2,[3 4]);
title('Equa��o de Diferen�as 2');
hold on; stem(x); stem(y,'r');xlim([0 100]);
grid;