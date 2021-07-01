% Fun��o FFT Radix 2 Decima��o no Tempo (DIT)   
% Processamento de Sinais
% Welliton Jhonathan Leal Babinski 

%Sinal n�o peri�dico de entrada
%x = [2; 4; 5 ;6 ;9 ;8 ;7; 2 ;12 ;13; 14 ;2; 12; 7; 2; 14];

function [y] = fftR2dit(x)                                            
tic                                                                         % iniciando a contagem do tempo

p = nextpow2(length(x));                                                    % checando o tamanho do vetor de entrada
x = [x zeros(1,(2^p)-length(x))];                                           % complementando o vetor com zeros se necess�rio
N = length(x);                                                              % calculando o tamanho do array
R = log2(N);                                                                % calculando o n�mero de est�gios de convers�o
Metade = 1;                                                                 % Setando o valor de "Metade" inicial
x = bitrevorder(x);                                                         % colocando os samples em ordem de bit-reversa

for stage = 1:R                                                             % Est�gios da transformada
    for index = 0:(2^stage):(N-1)                                           % serie de c�lulas (butterflies) pra cada est�gio
        for n = 0:(Metade-1)                                                % criando a c�lula (butterfly) e salvando os resultados
            pos = n + index + 1;                                            % indexando a amostra
            pow = (2^(R-stage))*n;                                          % parte da pot�ncia do multiplicador complexo
            WN = exp((-1i)*(2*pi)*pow/N);                                   % Multiplicador complexo
            a = x(pos) + x(pos+Metade).*WN;                                 % criando a primeira parte da c�lula 
            b = x(pos) - x(pos+Metade).*WN;                                 % criando a segunda parte da c�lula 
            x(pos) = a;                                                     % salvando o c�lculo da primeira parte
            x(pos + Metade) = b;                                            % salvando o c�lculo da segunda parte
        end
    end
    Metade = 2 * Metade;                                                    %calculando o pr�ximo valor "Metade"
end
y = x;  
toc                                                                         %finalizando a contagem do tempo

L = 0:length(x)-1;
figure                                                                      %plotando os m�dulos das amostras
subplot(2,1,1)
stem(L,abs(y))
title("M�dulo com Algoritmo de Decima��o no Tempo FFT Radix-2");
xlabel('k');

subplot(2,1,2)                                                              %plotando as fases das amostras
stem(L,angle(y))
title("Fase com Algoritmo de Decima��o no Tempo FFT Radix-2");
xlabel('k');
end