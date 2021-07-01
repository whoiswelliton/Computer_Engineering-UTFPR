function fft_func(x)
tic
Y = fft(x);
toc
L = 0:length(x)-1; 

figure
subplot(2,1,1)
stem(L,abs(Y))
title("M�dulo com a Fun��o fft do Matlab");
xlabel('k');

subplot(2,1,2)
stem(L,angle(Y))
title("Fase com a Fun��o fft do Matlab");
xlabel('k');
end