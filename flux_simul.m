function [flux_noisy] = flux_simul(T_in,maxx,sampling_period,duty_cycle,total_sim_time, noise_std)
    if nargin < 6
        noise_std = 0; % default: no noise
    end

    T = T_in;
    sigma = T * duty_cycle / 6;
    mu    = T * duty_cycle / 2;

    num_samples_per_cycle = 1000; 
    t_cycle = linspace(0, T, num_samples_per_cycle);

    template = maxx * exp(-((t_cycle - mu).^2) / (2*sigma^2));
    template = template - min(template);
    figure;plot(t_cycle,template);xlabel('Time (s)');ylabel('Pulsar signal');saveas(gcf,'Template.bmp');
    
    num_cycles = ceil(total_sim_time / T);
    t = linspace(0, num_cycles*T, num_cycles*num_samples_per_cycle);
    gaussian_curve = repmat(template, 1, num_cycles);
    figure;plot(t,gaussian_curve);xlabel('Time (s)');ylabel('Pulsar signal');saveas(gcf,'replicate.bmp');
    
    num_samples = floor(total_sim_time / sampling_period);
    flux = zeros(1, num_samples);
    t_flux = (0:num_samples-1) * sampling_period;

    for i = 1:num_samples
        t_start = t_flux(i);
        t_end   = t_start + sampling_period;
        indices = (t >= t_start & t < t_end);

        if any(indices)
            flux(i) = trapz(t(indices), gaussian_curve(indices));
        end
    end
    
    mflux = mean(flux,'all');
    x = flux-mean(flux,'all');
    Fs = 1 / sampling_period;
    N = length(x);     
    X = fft(x);
    
    figure;
    subplot(1,2,1);plot(t_flux, flux, '-k')
    xlabel('Time (s)');
    ylabel('Integrated flux');

    X_mag0 = abs(X)/N;
    X_mag0 = X_mag0(1:floor(N/2)+1);
    f = Fs*(0:floor(N/2))/N;
    subplot(1,2,2);
    plot(f, X_mag0, '-b');
    xlabel('Frequency (Hz)');
    ylabel('Magnitude');
    title('Frequency Spectrum');
    grid on;
    
    saveas(gcf,'noiseless.bmp');

    if noise_std > 0
        magX = abs(X);
        phaseX = angle(X);

        max_mag = max(magX);
        threshold = 0.1 * max_mag;
        small_indices = magX < threshold;

        noise_vector = noise_std * randn(1, sum(small_indices));
        magX_noisy = magX;
        magX_noisy(small_indices) = magX(small_indices) .* (1 + noise_vector);

        X_noisy = magX_noisy .* exp(1i*phaseX);
    else
        X_noisy = X;
    end

    flux_noisy = real(ifft(X_noisy)) + mflux;
    flux_noisy(flux_noisy<0) = 0;
    
    figure;
    subplot(1,2,1);plot(t_flux, flux_noisy, '-k')
    xlabel('Time (s)');
    ylabel('Integrated flux');

    X_mag = abs(X_noisy)/N;
    X_mag = X_mag(1:floor(N/2)+1);
    f = Fs*(0:floor(N/2))/N;
    subplot(1,2,2);
    plot(f, X_mag, '-b');
    xlabel('Frequency (Hz)');
    ylabel('Magnitude');
    title('Frequency Spectrum');
    grid on;
    saveas(gcf,'noisy.bmp');
end