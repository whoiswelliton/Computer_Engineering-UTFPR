%% Impulso

clc;
N = 100;        % qtd de pontos de simula��o
A = 5;          % amplitude da senoide
Ts = 1e-1;      % per�odo de amostragem
NA = 50;        % numero de amostras/ciclo
NC = 2;         % n�mero de ciclos
To = NA*Ts;     % per^�odo fundamental
fo = 1/To;      % frequncia fundamental
NT = NA*NC;     % n�mero total de pontos
TT = NT*Ts;     % tempo total do gr�fico

t=0:Ts:TT;
y = zeros(1,N+2); %inicializa��o de y
x = zeros(1,N);   %inicializa��o de x

%La�o de repeti��o
%Contador iniciando em 3 devido ao deslocamento y(n-2) 
for n=3:N 
    if n == 3  
        x(n)=A;
    else
        x(n)=0; end
    
    %Equa��o de diferen�as y(n) obtida
    y(n) = (8*y(n-1) - 3*y(n-2) + 4*x(n-1) + x(n-2))/10;
    
    %Teste com outros coeficientes 
    %y(n) = (6*y(n-1) - 1*y(n-2) + 3*x(n-1) + 0.8*x(n-2))/10;
end
figure
%Plotando os 3 gr�ficos
subplot(2,2,1); 
stem(x); xlim([0 100]);
title('Entrada X[n]');
subplot(2,2,2); 
stem(y, 'r'); xlim([0 100]);
title('Sa�da Y[n]');
subplot(2,2,[3 4]);
title('Equa��o de diferen�as');
hold on; stem(x); stem(y,'r');xlim([0 100]);
grid;