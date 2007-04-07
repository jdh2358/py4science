from pylab import *
rc('lines', linewidth=2)
dx = 0.001
x = nx.arange(0.0, 1.0, 0.001)
#s = nx.where(x<0.5, 2*x, 2*(1.-x))
s = sin(2*4*pi*x*x)


F = fft(s)
nfreq = len(s)/2+1
freqs = linspace(0, 1/(2*dx), nfreq)  # the freq vector
F = F[:nfreq]  # extract positive frequencies

magnitude = nx.absolute(F)/len(s)
phase = nx.arctan2(F.imag,F.real)

# make the BODE plot
figure()
subplot(211)
plot(freqs, magnitude)
xlim(0,20)
grid()
ylabel('Amplitude')
title('Bode plot')
subplot(212)
plot(freqs, phase)
xlim(0,20)
grid()
ylabel('Phase')


# now do the reconstuction
def component(i):
    # scale by 2 because we are exluding negative freqs
    if i==0: scale = 1
    else: scale =2
    return scale*magnitude[i]*cos(2*pi*freqs[i]*x + phase[i])

tot = component(0)
for i in range(1,10): tot += component(i)

figure()
plot(x, tot, 'r--', x, s, 'b-', lw=2)
show()
