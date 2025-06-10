# LinRegConf
Perform linear least squares regression, accounting for uncertainty, using linear algebra methods to minimize the objective function
(in this case, $\chi^2$).

When using this code, please cite this repository using the reference provided here by GitHub.

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

## BibTeX Reference
``` bibtex
@SOFTWARE{Flury_LinRegConf,
       author = {{Flury}, Sophia R.},
        title = "{LinRegConf}",
         year = 2024,
        month = jan,
      version = {1.0.0},
          url = {https://github.com/sflury/LinRegConf},
          doi = {10.5281/zenodo.15577097} }
```

[![DOI](https://zenodo.org/badge/738698393.svg)](https://doi.org/10.5281/zenodo.15577097)

## Licensing
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
