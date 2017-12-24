close all
%{
"currTime": 0,
"temp1": 1,
"temp2": 2,
"temp3": 3,
"temp_10dof": 4,
"alt_press": 5,
"alt_strat": 6,
"alt_gps": 7,
"lat": 8,
"lat": 9,
"accel_x": 10,
"accel_y": 11,
"accel_z": 12,
"poll_flags": 13,
"pressure": 14,
"orientation.roll": 15,
"orientation.pitch": 16,
"orientation.heading": 16,
"accel_x": 18,
"accel_y": 19,
"accel_z": 20,
"mag_x": 21,
"mag_y": 22,
"mag_z": 23,
"gyro_x": 24,
"gyro_y": 25,
"gyro_z": 26 
%}



% f = 'karman_nh_flight1.CSV';
f = 'DATA3.csv';
f = 'UpperStage_Raw_Data.csv';

wholefile = csvread(f, 1, 0);
% lower = 15000;
% upper = 18000;
lower = 36000;
upper = 41400;
% timestamp = wholefile(15000:18000,1);
timestamp = wholefile(lower:upper,1);
t0 = timestamp(1);
timestamp = (timestamp - t0)./(1000);
ts = diff(timestamp).*1000;

altitude = wholefile(lower:upper,6);
x_accel = wholefile(lower:upper,19)./10;
y_accel = wholefile(lower:upper,20)./10;
z_accel = wholefile(lower:upper,21)./10;
temp1 = wholefile(lower:upper,1);
temp2 = wholefile(lower:upper,2);
temp3 = wholefile(lower:upper,3);
% pres_accel = diff(diff(altitude)./ts(1:end - 1))./ts(1:end - 2);

d = fdesign.lowpass('Fp,Fst,Ap,Ast',3,5,0.5,20,100);
d2 = fdesign.lowpass('Fp,Fst,Ap,Ast',3,5,0.5,30,100);
Hd = design(d,'equiripple');
Hd2 = design(d2,'equiripple');
x_output = filter(Hd,x_accel);
alt_lowpass = filter(Hd, altitude);
% altVel = filter(Hd, diff(altitude)./(writeTime/1000));

magAccel = ((x_accel.^2) + (y_accel.^2) + (z_accel.^2)).^0.5;

mag_output = filter(Hd, magAccel);

%load('NASASubscale.mat')





figure;
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


figure;
plot(timestamp(1:end-1),ts, '.');
title('Write time');
xlabel('Time (s)');
ylabel('Write time (ms)');
ylim([0, 100]);


% figure;
% % subplot(2,1,1);
% hold on
% plot(timestamp, temp1, '.');
% plot(timestamp, temp2, '.');
% plot(timestamp, temp3, '.');
% hold off
% title('Temps');
% xlabel('Time (s)');
% ylabel('temperature');
% % ylim([0, 100]);
% hold off


