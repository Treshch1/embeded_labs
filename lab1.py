from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

from random import random
import math

N = 256  # number of discrete
w = 2000  # cutoff frequency
x = np.arange(0, N, 1)


class DrawOption:
    def __init__(self, pl_title, pl_type="plot", x_range=x):
        self.pl_title = pl_title
        self.pl_type = pl_type
        self.x_range = x_range


def draw_plot(axes, data_plot, options_plot):
    axes.set_title(options_plot.pl_title)
    if options_plot.pl_type == "bar":
        axes.bar(options_plot.x_range, data_plot)
    elif options_plot.pl_type == "plot":
        axes.plot(options_plot.x_range, data_plot)


def draw(data, options, picture_name):
    data_length = len(data)
    if len(data) > 1:
        _, axes = plt.subplots(len(data), sharex=False, figsize=(10, 8))
        for i in range(data_length):
            draw_plot(axes[i], data[i], options[i])
    else:
        plt.figure(figsize=(10, 8))
        plt.plot(x, data[0], color='green')
    plt.savefig(picture_name)


def generate_signal(t):
    res = 0
    n = 14  # number of harmonic
    A = 5  # max amplitude
    wp = w / n

    for _ in range(n):
        a = A * random()
        fi = 2 * math.pi * random()
        res += a * math.sin(wp * t + fi)
        wp += w / n

    return res


def generate_array_of_signals(N):
    return np.array([generate_signal(i) for i in range(N)])


def generate_chart(signal, file_name):
    print(f'Математичне сподівання - {np.mean(signal)}')
    print(f'Дисперсія - {np.var(signal)}')
    options = [
       DrawOption("Signal", "plot"),
    ]
    draw([signal], options, file_name)
    return signal


def generate_spectrum(signal, file_name):
    x = np.fft.rfftfreq(N, 1./w)
    options = [
       DrawOption("Spectrum", "bar", x_range=x),
    ]
    draw([signal], options, file_name)
    return signal


def autocorr(i):
    corr = np.correlate(i, i, mode='full') / i.size
    corr = corr[corr.size // 2:]
    return corr


def intercorr(a, v):
    corr = np.correlate(a, v, mode='full') / a.size
    corr = corr[corr.size // 2:]
    return corr


def fft_function(signal):
    fft = np.fft.fft(signal)
    # fft_theo = np.abs(fft / N)
    return fft


def fft_function_2(signal):
    def factor(pk, n):
        angle = -2 * math.pi / n * pk
        return complex(math.cos(angle), math.sin(angle))

    def inner_fft(signal, p, level_factor):
        n = len(signal)
        next_n = n // 2
        next_p = p % next_n
        if n > 2:
            signal_odd = np.array([signal[i] for i in range(1, n) if i % 2 == 1])
            signal_pair = np.array([signal[i] for i in range(n) if i % 2 == 0])
            next_factor = factor(next_p, next_n)
            f_odd = inner_fft(signal_odd, next_p, next_factor)
            f_pair = inner_fft(signal_pair, next_p, next_factor)
            return f_pair + level_factor * f_odd

        w_odd = -1 if p % 2 else 1
        return signal[0] + signal[1] * w_odd

    length = len(signal)
    result = np.array([inner_fft(signal, p, factor(p, length)) for p in range(length)])
    real, image = np.array([i.real for i in result]), np.array([i.imag for i in result])
    return real, image


def calculate_timedelta_lab1():
    time_dict = {}
    for i in range(1, 6):
        start = datetime.now()
        generate_array_of_signals(i * 1000)
        end = datetime.now()
        delta = (end - start)
        time_dict[i * 1000] = delta.microseconds
    return time_dict


def calculate_timedelta_lab1():
    time_dict = {}
    for i in range(1, 6):
        start = datetime.now()
        generate_array_of_signals(i * 1000)
        end = datetime.now()
        delta = (end - start)
        time_dict[i * 1000] = delta.microseconds
    return time_dict


if __name__ == '__main__':
    print('LAB 1')
    lab_1_signal = generate_chart(generate_array_of_signals(N), "lab1.png")

    print('\n\nLAB 2\nAutocorrelated signal')
    autocorrelated_signal_lab_2 = generate_chart(autocorr(lab_1_signal), 'lab2_autocorr.png')
    
    print('\nIntercorrelated signal')
    intercorrelated_signal = generate_chart(intercorr(lab_1_signal, autocorrelated_signal_lab_2), 'lab2_intercorr.png')

    print('\nFourier transformation')
    fft = generate_spectrum(fft_function(lab_1_signal), 'lab3_spectr.png')
    real, imagine = fft_function_2(lab_1_signal)
    fft_2 = generate_spectrum(real, 'lab3_spectr_additional_task.png')
