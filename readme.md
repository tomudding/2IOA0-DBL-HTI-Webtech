# 2IOA0 DBL HTI + Webtech

The website can be accessed through [https://2ioa0.uddi.ng/](https://2ioa0.uddi.ng/).
Please follow the steps under **DOCUMENTATION** for more information on how to locally run graphion.

## DEADLINES
Given project deadlines:

| Task                   | Deadline date |
-------------------------|----------------
| ~~Interim video~~         | ~~24th of May~~  |
| ~~Interim report~~         | ~~24th of May~~  |
| Nearly final tool      | 12th of June |
| Final tool/report/video| 21st of June |

Our own deadlines:

| Task                              | Deadline date |
------------------------------------|----------------
| Filtering page v1                 | 31st of May   |
| Visualization page v1             | 31st of May   |
| Visualizations/interactions v1    | 31st of May   |
------------------------------------|----------------
| Filtering page v2                 | 7th of June   |
| Visualization page v2             | 7th of June   |
| Visualizations/interactions v2    | 7th of June   |
------------------------------------|----------------
| Filtering page v3                 | 14th of June  |
| Visualization page v3             | 14th of June  |
| Visualizations/interactions v3    | 14th of June  |
| Filming video                     | 14th of June  |
| Draft of final report             | 14th of June  |
------------------------------------|----------------
| Final touches on our tool         | 21st of June  |
| Editing video                     | 21st of June  |
| Checking and correcting report    | 21st of June  |

## REQUIREMENTS
Minimal requirements as described in VisProjectDescription.pdf and the kickoff slides.
- [ ] At least **2** visual metaphors
  - [x] Node-link diagram with at least **3** different layouts:
    - [x] Radial
    - [x] Force-directed
    - [x] Hierarchical
    - [ ] Spectral
    - [ ] Orthogonal
    - [ ] [Circular tree](https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_circular_tree.html)
    - [ ] Extra: others
  - [x] Adjacency matrix with at least **5** different reordering strategies
    - [x] Clustering
      - [x] Agglomerative hierarchichal clustering
        - Different ways of calculating the similarity between two clusters (aka. linkage criteria):
        - [x] Ward's method (minimizes the total within-cluster variance)
        - [x] single/minimum linkage clustering (dist(C1,C2) = min dist(Pi,Pj))
        - [x] complete/maximum linkage clustering (dist(C1, C2) = max dist(Pi, Pj))
        - [x] average linkage clustering (dist(C1, C2) = avg(dist(Pi, Pj)))
        - [x] weighted
        - [x] centroid
        - [x] median
        - Different distance metrics
        - [x] Euclidean
        - [x] Cityblock
        - [x] etc..
    - [ ] Greedy algorithms
      - [ ] Bipolarization
    - [ ] Optimal-leaf ordering
    - [ ] ...
  - Extra: others like (e.g. hybrid representations like NodeTrix or MatLink,)
    - Hybrid representations
      - [ ] NodeTrix
      - [ ] MatLink
    - [ ] [3D node-link diagram](https://plot.ly/python/3d-network-graph/)
    - [ ] [Arc diagram (combined with matrix reorderings maybe)](https://www.data-to-viz.com/graph/arc.html)

- [x] **Web-based** visualization tool for networks (weighted and directed graphs)
  - [x] Accessable via URL ([https://2ioa0.uddi.ng/](https://2ioa0.uddi.ng/))
  - [x] Upload graph data (in a specified data format)
  - [ ] Visual interactions from each of the 7 categories of interactions (Yi et al.)
  - [ ] Data and insights should be sharable with all other people using the web tool

Suggested further improvements but not required:
- [ ] Multiple coordinated view design
  - [ ] Different visualizations next to each other
  - [ ] Brushing and linking (highlighting / selecting is synchronized between graphs)
- [ ] Options for link representations in node-link diagrams (dotted, dashed, curved etc.)
- [ ] Edge bundling (though bold red text comes included: Only if you enjoy visualization and like to do more)

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
1. ```set FLASK_APP=graphion``` (or ```export FLASK_APP=graphion``` on UNIX-like systems)
2. ```flask run```
_The Flask service should now be running on localhost:5000._
