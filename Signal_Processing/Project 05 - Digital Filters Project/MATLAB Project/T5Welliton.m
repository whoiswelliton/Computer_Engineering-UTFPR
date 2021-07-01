clc
clear all
close all

%% Invari�ncia ao Impulso

f = 250;        %Frequ�ncia na banda passante
T = 1/10000;    %Per�odo de amostragem
nc = 3;         %N�mero de ciclos
N = nc*(1/f)/T; %N�mero de pontos
A1 = zeros(1,N); %Declara��o do vetor de entrada
y = zeros(1,N); %Declara��o do vetor de sa�da
%Forma de onda da entrada

%%
% = 1/(1+1.4137*s + 999.3*(10^-3)*s^2); %FT do PB 2 Ordem

% %Polos
% p1 = -1,111*10^-3 + 1,111j*10^-3;
% p2 = -1,111*10^-3 - 1,111j*10^-3;

%A2 = ztrans(A1);

syms n z;




