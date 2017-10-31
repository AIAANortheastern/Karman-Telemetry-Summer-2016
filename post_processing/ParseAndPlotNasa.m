close all
wholefile = csvread('karman_nh_flight1.CSV', 1, 0);
lower = 15000;
upper = 18000;
timestamp = wholefile(15000:18000,1);
t0 = timestamp(1);
timestamp = (timestamp - t0)./(1000);
writeTime = diff(timestamp).*1000;

altitude = wholefile(lower:upper,6);
x_accel = wholefile(lower:upper,19)./10;
y_accel = wholefile(lower:upper,20)./10;
z_accel = wholefile(lower:upper,21)./10;

d = fdesign.lowpass('Fp,Fst,Ap,Ast',3,5,0.5,20,100);
Hd = design(d,'equiripple');
x_output = filter(Hd,x_accel);

magAccel = ((x_accel.^2) + (y_accel.^2) + (z_accel.^2)).^0.5;

mag_output = filter(Hd, magAccel);

%load('NASASubscale.mat')

figure;
subplot(1, 1, 1)
subplot(4, 1, 1)
plot(timestamp, altitude, '-');
title('Altitude');
xlabel('Time (s)');
ylabel('Altitude (m)');

subplot(4, 1, 2)
plot(timestamp, x_accel, '-');
title('X Acceleration');
xlabel('Time (s)');
ylabel('X Axis Acceleration (g)');

subplot(4, 1, 3)
plot(timestamp, y_accel, '-');
title('Y Acceleration');
xlabel('Time (s)');
ylabel('Y Axis Acceleration (g)');

subplot(4, 1, 4)
plot(timestamp, z_accel, '-');
title('Z Acceleration');
xlabel('Time (s)');
ylabel('Y Axis Acceleration (g)');


figure;
subplot(3, 1, 1)
plot(timestamp, altitude);
title('Altitude');
xlabel('Time (s)');
ylabel('Altitude (m)');

subplot(3, 1, 2)
plot(timestamp, x_accel);
title('X Acceleration');
xlabel('Time (s)');
ylabel('X Axis Acceleration (g)');

subplot(3, 1, 3)
plot(timestamp, x_output)
title('X Acceleration -- Low pass filter (-20dB)');
xlabel('Time (s)');
ylabel('X Axis Acceleration (g)');

figure;
subplot(3, 1, 1)
plot(timestamp, altitude);
title('Altitude');
xlabel('Time (s)');
ylabel('Altitude (m)');

subplot(3, 1, 2)
plot(timestamp, magAccel, '.')
title('Magnitude of Acceleration');
xlabel('Time (s)');
ylabel('Magnitude of Acceleration (g)');

subplot(3, 1, 3)
hold on
plot(timestamp, mag_output);
title('Magnitude of Acceleration -- Low pass filter (-20dB)');
xlabel('Time (s)');
ylabel('Magnitude of Acceleration (g)');
plot(timestamp, ones(size(timestamp)), '--r');
hold off



% plot(timestamp(1:end-1),writeTime);
% title('Altitude');
% xlabel('Time (s)');
% ylabel('Altitude (m)');



