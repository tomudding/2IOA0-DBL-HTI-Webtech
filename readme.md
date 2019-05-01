# 2IOA0 DBL HTI + Webtech
## DOCUMENTATION
### 1. Installation
To install the development environment:
1. Open the _Anaconda Prompt_ as an administrator (solves permission issues).
2. Update _conda_ using ```conda update conda```.
3. Clone Git repository to current location with ```git clone insert_url``` where insert_url is the url given by the clone button on the top right. Or download the zip file.
4. Go to the Git repository folder using ```cd [git folder location]```.
5. Create a new conda environment using ```conda env create -f environment.yml```.

### 2. Development
To access the development environment:
1. Open the _Anaconda Prompt_ as an administrator (solves permission issues).
2. Enter the environment through ```conda activate 2ioa0```.
3. Make sure you go to the actual Git repository folder using ```cd [git folder location]```.
4. Now you can work on the web app.
5. After you finished a certain task, you can upload it to Github by doing the following commands in a git command prompt (or similar actions in Github desktop):
   1. ```git pull origin master``` to get the latest repository from Github.
   2. ```git add .``` to add all your file changes to a commit.
   3. ```git commit -m "Put commit message here``` to make the commit.
   4. ```git push origin master``` to push your commit to Github.  
   <sup><em><strong>If you decide to implement a whole new feature which requires a lot of modifications please do it on <a href="https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging">a seperate branch and create a pull request to merge</a> it into the master branch.</strong></em></sup>

### 3. Deployment
To run the Flask app service locally execute the following commands (in the repository folder):
1. ```pip install -e .```
2. ```set FLASK_APP=graphion``` (or ```export FLASK_APP=graphion``` on UNIX-like systems)
3. ```flask run```
_The Flask service should now be running on localhost:5000._
