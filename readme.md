# 2IOA0 DBL HTI + Webtech
## DOCUMENTATION
### 1. Anaconda
#### 1.1 Installation
1. Open the _Anaconda Prompt_ as an administrator (solves permission issues).
2. Update _conda_ using ```conda update conda```.
3. Go to the Git repository folder using ```cd [git folder location]```.
4. Create a new conda environment using ```conda env create -f environment.yml```.

#### 1.2 Usage
1. Open the _Anaconda Prompt_ as an administrator (solves permission issues).
2. Enter the environment through ```conda activate 2ioa0```.
3. Make sure you go to the actual Git repository folder using ```cd [git folder location]```.
4. Now you can work on the web app.

### 2. Deployment
To run the Flask service locally execute the following commands: 
1. ```pip install -e .```
2. ```set FLASK_APP=app``` (or ```export FLASK_APP=app``` on UNIX-like systems)
3. ```flask run```
_The Flask service should now be running on localhost:5000._
