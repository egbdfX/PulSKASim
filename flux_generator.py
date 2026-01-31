import numpy as np
import matplotlib.pyplot as plt
from scipy.io import savemat

def flux_simul(T_in, maxx, sampling_period, duty_cycle, total_sim_time, noise_std=0):
    T = T_in
    sigma = T * duty_cycle / 6
    mu = T * duty_cycle / 2

    num_samples_per_cycle = 1000
    t_cycle = np.linspace(0, T, num_samples_per_cycle)

    template = maxx * np.exp(-((t_cycle - mu) ** 2) / (2 * sigma ** 2))
    template = template - np.min(template)

    plt.figure()
    plt.plot(t_cycle, template)
    plt.xlabel("Time (s)")
    plt.ylabel("Pulsar signal")
    plt.savefig("Template.png")
    plt.close()

    num_cycles = int(np.ceil(total_sim_time / T))
    t = np.linspace(0, num_cycles * T, num_cycles * num_samples_per_cycle)
    gaussian_curve = np.tile(template, num_cycles)

    plt.figure()
    plt.plot(t, gaussian_curve)
    plt.xlabel("Time (s)")
    plt.ylabel("Pulsar signal")
    plt.savefig("replicate.png")
    plt.close()

    num_samples = int(np.floor(total_sim_time / sampling_period))
    flux = np.zeros(num_samples)
    t_flux = np.arange(num_samples) * sampling_period

    for i in range(num_samples):
        t_start = t_flux[i]
        t_end = t_start + sampling_period
        indices = (t >= t_start) & (t < t_end)

        if np.any(indices):
            flux[i] = np.trapezoid(gaussian_curve[indices], t[indices])

    mflux = np.mean(flux)
    x = flux - mflux

    Fs = 1 / sampling_period
    N = len(x)
    X = np.fft.fft(x)

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.plot(t_flux, flux, "-k")
    plt.xlabel("Time (s)")
    plt.ylabel("Integrated flux")

    X_mag0 = np.abs(X) / N
    X_mag0 = X_mag0[:N // 2 + 1]
    f = Fs * np.arange(N // 2 + 1) / N

    plt.subplot(1, 2, 2)
    plt.plot(f, X_mag0, "-b")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("Frequency Spectrum")
    plt.grid(True)

    plt.savefig("noiseless.png")
    plt.close()

    if noise_std > 0:
        magX = np.abs(X)
        phaseX = np.angle(X)

        max_mag = np.max(magX)
        threshold = 0.1 * max_mag
        small_indices = magX < threshold

        noise_vector = noise_std * np.random.randn(np.sum(small_indices))
        magX_noisy = magX.copy()
        magX_noisy[small_indices] *= (1 + noise_vector)

        X_noisy = magX_noisy * np.exp(1j * phaseX)
    else:
        X_noisy = X

    flux_noisy = np.real(np.fft.ifft(X_noisy)) + mflux
    flux_noisy[flux_noisy < 0] = 0

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.plot(t_flux, flux_noisy, "-k")
    plt.xlabel("Time (s)")
    plt.ylabel("Integrated flux")

    X_mag = np.abs(X_noisy) / N
    X_mag = X_mag[:N // 2 + 1]

    plt.subplot(1, 2, 2)
    plt.plot(f, X_mag, "-b")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("Frequency Spectrum")
    plt.grid(True)

    plt.savefig("noisy.png")
    plt.close()

    return flux_noisy
