clear all;
close all; 
clc;
format short;                                                                   

%importando os dados do sinal do arquivo .mat

input = load('dados.mat');                                                   
stem(-300:1:299,input.x,'LineStyle','none','MarkerEdgeColor','blue');
title('Sinal de Entrada Amostrado');
ylabel('x[n]');xlabel('n');

% (a) - Utilize a equa��o de an�lise da S�rie Discreta de Fourier 
% e obtenha os valores dos coeficientes

FS = 18000;                                      % Frequ�ncia de Amostragem              
T = 1/FS;                                                % Per�odo do Sinal
L = length(input.x);                               % Quantidade de Amostras
N = L/2; %300                                        % Amostras por Per�odo
t = -N:1:N-1;                               %Invervalo onde variar a Fun��o
f = FS*(0:(N/2))/N;

% n = [0:N-1];
% k =[0:N-1];
%Para cada valor de 't', ser� necess�rio executar o somat�rio
%inteiro de -N a N

CK = zeros(1, L);         %inicializa um vetor de zeros do tamanho do sinal

%Implementa��o da equa��o da DFT
for k = t
    PNTR = k+1+N;                           %ponteiro para simplificar a EQ
    for n = 0:N-1
        CK(1,PNTR) = CK(1,PNTR) + input.x(n+1)*exp((-j*2*pi*k*n)/N);
    end
    CK(1,PNTR) = CK(1,PNTR)*(1/N);
end 

Modulo = abs(CK);
ind = abs(CK) < 10e-10;
CK(ind) = 0;
Fase = unwrap(angle(CK))*180/pi;

figure
stem(t,Modulo)
figure
stem(t,Fase)


% phase = unwrap(angle(CK))*180/pi;
% 
% subplot(2,1,2)
% plot(f,phase)
% title('Phase')
% ax = gca;


