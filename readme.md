## 2IOA0 DBL HTI + Webtech
This document enlists possible requirements for the web app.

### Required Packages
In order to use the web app locally the following packages (and their dependencies) are required (```pip install [packages]``` should do the job):
- Python 3.7.*
- pyct (0.4.6, required to install pyviz)
- PROJ.4 (4.9.3, required to install Cartopy, see https://proj4.org/install.html or use ```conda install -c conda-forge proj4=4.9.3```)
- pyproj (2.1.3, required to interface with PROJ.4)
- Cartopy (0.17.0, required to install pyviz)
- pyviz (0.10.0)
- dash (0.42.0)
- bokeh (1.1.0)
- Flask (1.0.2, comes with dash)

### Optional Packages
Currently optional packages, might change as the web app is build:
- Datashader

### Deployments
There are multiple platforms on which the web app can be hosted. Each platform has its own benefits and drawbacks. Possible providers are AWS (Amazon), Azure (Microsoft), Google Cloud Platform, Heroku, or self-hosted.
