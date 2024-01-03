# LinRegConf
Perform linear least squares regression, accounting for uncertainty, using linear algebra methods.

## Example
``` python
import numpy as np
from LinRegConf import LinRegConf
# make fake data
np.random.seed(123)
n = 10
x_data = np.random.rand(n)
y_data = 2*x_data+1 + np.random.randn(n)*0.1
x_errs = np.max([abs(np.random.randn(n)*0.05),np.zeros(n)+0.05],axis=0)
y_errs = np.max([abs(np.random.randn(n)*0.1),np.zeros(n)+0.1],axis=0)
# fit plus confidence intervals (supports any polynomial order)
# automatically incorportates y errors if given
# for now, x errors are only for plotting
fit = LinRegConf(x_data,y_data,x_err=x_errs,y_err=y_errs,n_poly=1,p=0.05)
# print best-fit parameters
fit.pprint()
# plot fit plus data
fit.plot()
```
```
a_0 x^0  :  1.023 +/- 0.109
a_1 x^1  :  2.025 +/- 0.188
```
![image of a linear fit to data with 95% confidence intervals](LinRegConf.png "LinRegConf fit")
