import scipy.stats
import numpy.linalg as la
import numpy


def regress(X,y):
    """
    Perform a multiple linear regression of y onto X.  X is a num
    observations by (num variables +1) array.  X should contain a
    column of ones to generate the intercept.  y is a num observations
    array of independent variables

    return value B, residuals, stats

    B: the regression coeffients;  Ypred = B.T * X.T
    residuals: array( y - Ypred.T)
    stats = Rsquared, F, p
    
    """

    # regression coeffs are given by (Xt*X)-1*Xt*y
    N = X.shape[0]
    origshape = y.shape
    y.shape = N, 1
    X = numpy.matrix(X)
    Y = numpy.matrix(y)
    Xt = X.T
    Xt_X_i = la.inv(Xt*X) 
    B = Xt_X_i*Xt*Y

    Ypred = B.T * Xt
    residuals = numpy.array(Y-Ypred.T)
    CF = N*numpy.mean(y)**2     # correction factor

    SStotal = float(Y.T*Y-CF)
    SSregress =  float(B.T * Xt * Y - CF)
    SSerror =  SStotal - SSregress

    Rsquared = SSregress/SStotal

    dfTotal = N-1
    dfRegress = len(B)-1
    dfError = dfTotal - dfRegress

    F = SSregress/dfRegress / (SSerror/dfError)
    prob = 1-scipy.stats.f.cdf(F, dfRegress, dfError)

    stats = Rsquared, F, prob
    y.shape = origshape
    B = numpy.asarray(B)
    #print 'B', B
    #print 'B[:,0]', B[:,0]
    #print 'B[0,:]', B[0,:]
    return B[:,0], residuals, stats


    

