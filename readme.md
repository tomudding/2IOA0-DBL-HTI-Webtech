## 2IOA0 DBL HTI + Webtech
This document enlists possible requirements for the web app.

### Installing everything in Anaconda
1. Open the _Anaconda Prompt_ as an administrator (solves permission issues).
2. Update _conda_ using ```conda update conda```.
3. Create a new conda environment using ```conda create --name [name]``` (make sure to use Python 3.6(.8)).
4. Activate the conda environment using ```conda activate [name]```.
5. Install _pyviz_ and additional packages using ```conda install [package]```.

### Deployments
There are multiple platforms on which the web app can be hosted. Each platform has its own benefits and drawbacks. Possible providers are AWS (Amazon), Azure (Microsoft), Google Cloud Platform, Heroku, or self-hosted.
