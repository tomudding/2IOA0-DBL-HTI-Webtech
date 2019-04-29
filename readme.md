## 2IOA0 DBL HTI + Webtech
This document enlists possible requirements for the web app.

### Anaconda
#### Installation
1. Open the _Anaconda Prompt_ as an administrator (solves permission issues).
2. Update _conda_ using ```conda update conda```.
3. Go to the Git repository folder using ```cd [git folder location]```.
4. Create a new conda environment using ```conda env create -f environment.yml```.

#### Usage
1. Open the _Anaconda Prompt_ as an administrator (solves permission issues).
2. Enter the environment through ```conda activate 2ioa0```.
3. Make sure you go to the actual Git repository folder using ```cd [git folder location]```.
4. Now you can work on the web app.

### Required Packages
- Flask ```conda install -c anaconda flask```

### Deployments
There are multiple platforms on which the web app can be hosted. Each platform has its own benefits and drawbacks. Possible providers are AWS (Amazon), Azure (Microsoft), Google Cloud Platform, Heroku, or self-hosted.

To run the Flask service locally execute the following commands: 
1. ```export FLASK_APP=server.py```
2. ```flask run```
_The Flask service should now be running on 127.0.0.1:5000, it can be accessed through [localhost:5000](localhost:5000)._

To deploy the Flask service on an actual webserver execute the following commands:
1. ```export FLASK_APP=server.py```
2. ```flask run --host=0.0.0.0```
