%%audioTestBench

asiosettings
deviceReader = audioDeviceReader;
devicesIN = getAudioDevices(deviceReader)
devicesOUT = getAudioDevices(deviceWriter)

%% interface utilizada para captura do sinal de �udio a partir de um arquivo ou dsp
%% pode gravar o sinal em arquivo ou mandar para uma sa�da de �udio
%% tem funcionalidades como time scope e spectrum scope
