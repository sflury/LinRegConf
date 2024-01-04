# import functions
from numpy import array, any, diag, ones, cov, square, sum, sqrt, linspace
from numpy.linalg import inv,pinv,det
from scipy.stats import t as tdist
from matplotlib import pyplot as plt
'''
Name
    LinRegConf

Purpose
    Linear least squares fit to given data for polynomial of arbitrary order.
    Includes uncertainty in ordinate for inverse-variance weights if provided.
    Calculates $1\sigma$ uncertainties in parameters as well as best-fit
    confidence intervals for a desired p-value. Optional plotting.
    Least squares fit is accomplished using the generalized linear algebra
    approach with method for computing the inversion of the covariance matrix
    based on a test for singularity (SVD if singular, LUD otherwise).

Arguments
    :x_data (*np.ndarray*): data for the abscissa in nx1 array
    :y_data (*np.ndarray*): data for the ordinate in nx1 array

Keyword Arguments
    :x_err  (*np.ndarray*): abscissa uncertainty as nx1 array; default of None
    :y_err  (*np.ndarray*): ordinate uncertainty as nx1 array; default of None
    :n_poly (*int*)       : polynomial order; default of 1
    :p      (*float*)     : percentile for confidence intervals; default of 0.05

Returns
    :LinRegConf (*object*): an instantiation of the LinRegConf object class with
                all associated attributes and methods, including linear least
                squares fit results and confidences

Attributes
    :params (*np.ndarray*): n_poly+1 x 1 array of best-fit parameters
    :uncrts (*np.ndarray*): n_poly+1 x 1 array of parameter uncertainties
    :Z      (*np.ndarray*): n_poly+1 x n array of the design matrix
    :ssr    (*float*)     : summed squared residuals
    :model  (*function*)  : callable function which, given arbitrary abscissa
                values, returns the best-fit model prediction for the ordinate
    :CI     (*function*)  : callable function which, given arbitrary abscissa
                values, returns the *p* confidence on the predicted ordinate

Methods
    :__fit__ : performs linear least squares for polynomial of order *n_poly*
    :__conf__: computes confidence intervals on best-fit polynomial at the
                *p* percentile
    :pprint  : prints best-fit parameters with $1\sigma$ uncertainties
    :plot    : plots best fit with confidence intervals and data (with
                uncertainties if provided)
'''
class LinRegConf(object):
    def __init__(self,x_data,y_data,n_poly=1,p=0.05,x_err=None,y_err=None):
        # relevant numbers
        self.n_poly = n_poly
        self.n   = len(x_data)  # data size
        self.dof = self.n - self.n_poly # degrees of freedom
        self.p   = p
        # store data
        self.x = x_data
        self.y = y_data
        self.yerr = y_err
        self.xerr = x_err
        # design matrix
        self.design = lambda x: array([x**i for i in range(self.n_poly+1)]).T
        # fit using linear least squares
        self.__fit__()
        # confidence intervals on confidence intervals
        self.__conf__()
    # function to fit using linear least squares
    def __fit__(self):
        # design matrix
        Z = self.design(self.x)
        # response matrix
        Y = self.y
        # weight matrix
        if any(self.yerr == None):
            W = diag(ones(self.n))
        else:
            W = diag(self.yerr**-2)
        # linear least squares for singular matrix
        if det(Z.T @ Z) == 0:
            S = pinv(Z.T @ W @ Z)
            B = S @ (Z.T @ W @ Y)
        # linear least squares for non-singular matrix
        else:
            S = inv(Z.T @ W @ Z)
            B = S @ (Z.T @ W @ Y)
        # store for later
        self.Z  = Z
        self.Y  = Y
        self.W  = W
        self.invcov = S
        self.params = B
        # function returning Y given X
        self.model = lambda x: B @ self.design(x).T
        # summed squared residuals
        self.res = (Y-B@Z.T)
        self.ssr = (self.res.T @ W @ self.res)
        # 1sigma uncertainty in parameters
        self.uncrts = sqrt(diag(S)*self.ssr/self.dof) * tdist.ppf(0.8413,self.dof)
    # set up confidence intervals
    def __conf__(self):
        # normalization
        xbar = self.Z.mean(axis=0)
        norm = sum( (self.Z-xbar).T @ (self.Z-xbar) )
        # function returning confidence in Y given X
        x  = linspace(self.x.min()//1,self.x.max()//1+1,11)
        self.CI = lambda x,p=self.p: tdist.ppf(1-p,self.dof) * \
                    sqrt( self.ssr/self.dof * (1/sum(diag(self.W))+\
                    (diag(self.invcov) @ (self.design(x)-xbar).T**2)/ norm ) )
    # print out results
    def pprint(self):
        for i in range(self.n_poly+1):
            print(f'a_{i:d} x^{i:d}  :  {self.params[i]:.3f} +/- {self.errors[i]:.3f}')
    # plot up data
    def plot(self,xlabel='x',ylabel='y'):
        # arbitrary plotting arrays
        x_plot = linspace(self.x.min()//1,self.x.max()//1+1,101)
        y_plot = self.model(x_plot)
        c_plot = self.CI(x_plot)
        # plot with confidence intervals
        plt.fill_between(x_plot,y_plot-c_plot,y_plot+c_plot, \
                        color='xkcd:cerulean',alpha=0.3,edgecolor='none')
        plt.plot(x_plot,y_plot-c_plot,'--',color='xkcd:cerulean',alpha=0.5)
        plt.plot(x_plot,y_plot+c_plot,'--',color='xkcd:cerulean',alpha=0.5)
        if any(self.xerr != None) and any(self.yerr != None):
            plt.errorbar(self.x,self.y,zorder=3,ls='none',color='black',lw=1,\
                        xerr=self.xerr,yerr=self.yerr)
        elif any(self.yerr != None):
            plt.errorbar(self.x,self.y,zorder=3,ls='none',color='black',lw=1,yerr=self.yerr)
        plt.scatter(self.x,self.y,c='xkcd:peach',edgecolor='black',zorder=4)
        plt.plot(x_plot,y_plot,color='xkcd:cerulean',zorder=3)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xlim(x_plot[0],x_plot[-1])
        plt.ylim((y_plot-c_plot).min(),(y_plot+c_plot).max())
        plt.subplots_adjust(bottom=0.15,left=0.18,right=0.95,top=0.95)
        plt.show()
