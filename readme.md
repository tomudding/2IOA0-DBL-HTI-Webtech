## 2IOA0 DBL HTI + Webtech
This document enlists possible requirements for the web app.

### Anaconda
#### Installation
1. Open the _Anaconda Prompt_ as an administrator (solves permission issues).
2. Update _conda_ using ```conda update conda```.
3. Create a new conda environment using ```conda create -n 2ioa0 python=3.6``` (make sure to use Python 3.6(.8)).
4. Activate the conda environment using ```conda activate 2ioa0```.
5. Install _pyviz_ and additional packages using ```conda install -c pyviz/label/dev pyviz``` and ```conda install [package]```.

#### Usage
1. Open the _Anaconda Prompt_ as an administrator (solves permission issues).
2. Enter the environment through ```conda activate 2ioa0```.

### Deployments
There are multiple platforms on which the web app can be hosted. Each platform has its own benefits and drawbacks. Possible providers are AWS (Amazon), Azure (Microsoft), Google Cloud Platform, Heroku, or self-hosted.
