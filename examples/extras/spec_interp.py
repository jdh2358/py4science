#!/usr/bin/env python
"""Simple spectral interpolation routines."""

import scipy as S
import pylab as P

def spec_interp(coef_spec,factor=1,x1=1.0):
    """Interpolate a function"""

    assert isinstance(factor,int) and factor > 0,\
           "factor must be a positive integer"

    npts = len(coef_spec)
    padded_fft = S.zeros(npts*factor,'D')
    padded_fft[:npts] = coef_spec
    return factor*S.ifft(padded_fft).real

def spec_interp2(coef_spec,factor=1):
    """Interpolate a function"""

    assert isinstance(factor,int) and factor > 0,\
           "factor must be a positive integer"

    npts = len(coef_spec)
    padded_fft = S.empty(npts*factor,'D')
    for i in range(factor):
        padded_fft[i*npts:(i+1)*npts] = coef_spec
    out = S.ifft(padded_fft)
    return out.real

def spec_interp(coef_spec,factor=1):
    """Interpolate a function"""

    assert isinstance(factor,int) and factor > 0,\
           "factor must be a positive integer"

    fhat = coef_spec
    M = factor
    N = len(fhat)
    alpha = 2j*S.pi/(M*N)
    out = S.empty(M*N,'D')
    for m in range(M):
        out[m::M] = S.ifft(fhat*S.exp(alpha*m*S.arange(N)))
    return out.real

def spec_interp2(x,coef_spec,x1=1.0):
    """Interpolate a function"""

    npts = len(coef_spec)
    a = S.sin((1*S.pi/(x1))*x*S.arange(npts))
    out = (1.0/npts)*S.dot(coef_spec.imag,a)
    return out

def interpolating_func(coef_spec,x1=1.0):
    """Interpolate a function"""

    npts = len(coef_spec)
    a = S.exp((2j*S.pi/(x1))*x*S.arange(npts))
    return (1.0/npts)*S.dot(coef_spec,a).real


if __name__=='__main__':

    P.close('all')
    x1   = 1.0
    npts = 8
    interp_factor = 7
    npts_interp = npts*interp_factor
    
    def parab(x,x1=1.0):
        return ((x1**2)/4.0)-(x-(x1/2.0))**2

    def sin2(x,x1=1.0):
        return S.sin(2*S.pi*x)

    xarr = P.frange(0,x1,npts=npts,closed=0)
    yarr = parab(xarr,x1)
    yarr = sin2(xarr,x1)
    yspec = S.fft(yarr)
    
    xinterp = P.frange(0,x1,npts=npts_interp,closed=0)
    yinterp = spec_interp(yspec,interp_factor)
    P.plot(xarr,yarr,'g+-',lw=2,label='data')
    P.plot(xinterp,yinterp,'r+-',lw=1,mew=2,label='inerpolated')

##    xinterp = P.frange(0,x1,npts=npts_interp+1,closed=0)
##    yinterp = S.array([spec_interp(x,yspec,x1) for x in xinterp])
##    P.plot(xinterp,yinterp,'b+-',lw=1,mew=2,label='inerpolated+1')

##    xinterp = P.frange(0,x1,npts=npts_interp+2,closed=0)
##    yinterp = S.array([spec_interp(x,yspec,x1) for x in xinterp])
##    P.plot(xinterp,yinterp,'c+-',lw=1,mew=2,label='inerpolated+2')

##    xinterp = P.frange(0,x1,npts=npts_interp*12,closed=1)
##    yinterp = S.array([spec_interp(x,yspec,x1) for x in xinterp])
##    P.plot(xinterp,yinterp,'m+-',lw=1,label='inerpolated-cont')

    P.legend()
    P.show()
