% clc; clear all
tiempoTotal = tic;
% EL EFECTO DE B1 ESTA EN VolumenSensitivo.m

% ---------------------------------------------------------------------
% ------------------------ INPUTS -------------------------------------
% ---------------------------------------------------------------------

Chi =  24.1*1e-6; % (ppm) Susceptibilidad volumetrica
B0 = 7; % T
gyromagneRatio = 103.962*1e6; %  rad/s/T)
skindepth = 0.012; % profundida de penetracion, mm

graficos = 'si';
subplots = 'no'; % MAXIMO DE SUBPLOTS: 6
iter_Index = 1; % 1=p_iter,  2=a_iter,  3=h_iter

guardar_obj = true;

% CREACION DE LA LAMINA ---------------------------------------------------

disp('- - - - - - - - - - - - - - ')
disp('CREACION DE LA LAMINA')
voxelSize = [0.001 0.001 0.001]; % mm    -  matlab convention: [dy dx dz]
n_sk = skindepth/voxelSize(1); %voxels de profundidad de penetracion

Ny = 512;
Nx = 512;
Nz = 512;
% x = 3 mm, y = 12 mm
lado_x = 0.512; lado_y = 0.512; lado_z = 0.38;

y=(1:Ny)*voxelSize(1);
x=(1:Nx)*voxelSize(2); 
z=(1:Nz)*voxelSize(3);

[X,Y,Z]= meshgrid(x,y,z);

% creo el objeto
Obj = 0.* X;
obj_x = Nx/2-round(lado_x/voxelSize(2)/2)+1 : Nx/2+round(lado_x/voxelSize(2)/2);
obj_y = Ny/2-round(lado_y/voxelSize(1)/2)+1 : Ny/2+round(lado_y/voxelSize(1)/2);

% en z está centrado en 2*lado_z
obj_z = Nz/2-round(lado_z/voxelSize(3)/2) : Nz/2+round(lado_z/voxelSize(3)/2-1);


% electrodo de abajo:
Obj(obj_y,obj_x,obj_z) = 1;
% electrodo de arriba:
% Obj(obj_y,obj_x,obj_z_2) = 1;



lado_x = length(obj_x)*voxelSize(2);
lado_y = length(obj_y)*voxelSize(1);
lado_z = length(obj_z)*voxelSize(3);
msg = ['    lamina de: ', num2str(lado_x),'x',num2str(lado_y), ...
         'x', num2str(lado_z), ' mm^3'];
disp(msg)
toc(tiempoTotal)

% ---------------------------------------------------------------------
% ------------------------ CREACION DE VOL SENS -----------------------
% ---------------------------------------------------------------------
disp('- - - - - - - - - - - - - - ')
disp('Creacion del volumen sensitivo')
resetTimer = tic;

% creo el volumen sensitivo
 Vol_Sens = VolumenSensitivo(Obj, n_sk);
toc(resetTimer)

% ---------------------------------------------------------------------
% ---------------------------------------------------------------------
% ---------------------------------------------------------------------            

% ---------------------------------------------------------------------
% ------------------------ CALCULO DE DELTA ---------------------------
% ---------------------------------------------------------------------            
disp('- - - - - - - - - - - - - - ')
disp('Calculo del corrimiento en Bz')
resetTimer = tic;

% creo la distribucion de susceptibilidad
dChi_3D = Obj .* Chi;
% Calculo el corrimiento en Bz
dB = B0*calculateFieldShift(dChi_3D, voxelSize);
Bz = B0+dB;
% dOhmega = dB*gyromagneRat  io;
delta = (Bz-B0)/B0*1e6; % ppm
toc(resetTimer)           
% ---------------------------------------------------------------------
% ---------------------------------------------------------------------
% ---------------------------------------------------------------------


%%
% ---------------------------------------------------------------------
% ------------------------ GRAFICOS -----------------------------------
% ---------------------------------------------------------------------            
disp('- - - - - - - - - - - - - - ')
disp('Graficos')
resetTimer = tic;

%%
if graficos == 'si'
    %-----------------------------------------------


    % Plot delta ----------------------------------
    c_lim = max([abs(min(min(min(delta)))), abs(max(max(max(delta))))]);
    coloraxis = [-c_lim, c_lim];

    slice_y = Ny/2;
    bz=zeros(Nx,Nz);
    bz(:,:)=delta(slice_y,:,:);
%                 bz(:,:)=delta(slice_y,:,:).*Obj(slice_y,:,:);
    figure(300)
    if strcmp(subplots,'si')
        subplot(6,1,iterador(iter_Index))
    end
    contour(x,z,bz',50)
%                 imagesc(x,z,bz');
    set(gca,'Ydir','normal');
    ylabel('z (mm)');
    xlabel('x (mm)');
    colorbar; colormap(redblue); caxis(coloraxis)
    % --------------------------------------------

end
toc(resetTimer)
% ---------------------------------------------------------------------
% ---------------------------------------------------------------------
% ---------------------------------------------------------------------            




%%
%------------------------histograma----------------------------------------
%--------------------------------------------------------------------------
% Creo la matriz de Signal y el histograma
            Signal = delta.*Vol_Sens;
            Signal = Signal(:);
            Signal(Signal==0) = [];

            figure(123456)
            h = histogram(Signal(:));%, 'Visible', 'off'); 
            % EXTRAIGO DATOS DEL HISTOGRAMA
            counts = h.Values; be1 = h.BinEdges; 
            % rotacion ciclica hacia adelante:
            be2=circshift(be1,-1);
            bc = (be1+be2)/2;
            bc(end)= []; % quito el ultimo elemento, que sobra.
            hist = [bc' counts'];

%--------------------------------------------------------------------------
%--------------------------------------------------------------------------        

%% CALCULO EL ESPECTRO
ppm = 116.64;

w = (hist(:,1)+257.3)*2*pi*ppm;
Pw = hist(:,2);

T2est = 0.5*1e-3;
t = linspace(0,0.0102400,1024);
SNR = 100;

[T,W] = meshgrid(t,w);


PW = ones(size(T)).*Pw;
Swt = PW .* exp(1i*W.*T-T/T2est);
St = sum(Swt);

noise = rand(1,length(t));

% St = St + St(1)/SNR * noise;

% Str = trapz(real(Swt),1);
% Sti = trapz(imag(Swt),1);
% Str = sum(real(Swt));
% Sti = sum(imag(Swt));
% St = Str + 1i * Sti; 




ZF = length(t);
dw = t(2)-t(1);
sw = 1/dw;
freq = zeros(ZF,1);
for ll=1:ZF
    freq(ll,1)=(ll-1)*sw/(ZF-1)-sw/2;
end


Spec = fftshift(fft(St)); Spec = Spec';
ppmAxis = freq/ppm;
salida = [ppmAxis real(Spec)];


figure(224)
subplot(2,2,1)
plot(t,real(St))

subplot(2,2,2)
hold on
plot(ppmAxis,real(Spec),'b','LineWidth',2);
set(gca,'Xdir','reverse')
xlabel('\delta (ppm)')
xlim([200 300])

subplot(2,2,4)
plot(w/2/pi/ppm,Pw,'r','LineWidth',2);
hold on;
set(gca,'Xdir','reverse')
xlabel('\delta (ppm)')
ylabel('P(\delta)')
xlim([200 300])

subplot(2,2,3)
plot(w/2/pi/ppm,Pw/max(max(Pw)),'r','LineWidth',2);
hold on;
plot(ppmAxis,real(Spec)/max(max(real(Spec))),'b','LineWidth',2);
legend2 = ['Espectro, T_2^* = ', num2str(T2est*1000), ' ms'];
legend({'Histograma', legend2})
set(gca,'Xdir','reverse')
xlabel('\delta (ppm)')
ylabel('P(\delta)')
xlim([235 275])
ylim([-0.1 1.1])




%% --------------------------------------------------------------

disp('_____________________________________________________')



tiempoTotal = toc(tiempoTotal);
disp(['Tiempo total: ', num2str(tiempoTotal/60), ' min'])

% load handel.mat;
% sound(y, Fs);


    