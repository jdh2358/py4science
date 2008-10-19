from scipy import arange, sin, pi, randn, zeros
import pylab as p

a = 2       # 2 volt amplitude
f = 10      # 10 Hz frequency
sigma = 0.5 # 0.5 volt standard deviation noise

# create the t and v and store them a 2D array X 
t = arange(0.0, 2.0, 0.02)                # an evenly sampled time array
v = a*sin(2*f*pi*t) + sigma*randn(len(t)) # a noisy sine wave
X = zeros((len(t),2))                     # an empty output array
X[:,0] = t                                # add t to the first column 
X[:,1] = v                                # add s to the 2nd column
p.save('data/noisy_sine.dat', X)            # save the output file as ASCII

# plot the arrays t vs v and label the x-axis, y-axis and title
# save the output figure as noisy_sine.png
p.plot(t, v, 'b-')
p.xlabel('time (s)')
p.ylabel('volts (V)')
p.title('A noisy sine wave')
p.grid()
p.savefig('noisy_sine.png', dpi=150)
p.savefig('noisy_sine.eps')
p.show()
