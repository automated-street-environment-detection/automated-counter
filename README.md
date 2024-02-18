### How to contribute

1. Clone the repository
    - Click the green "<> Code" Button
    - Copy the HTTP url for cloning
    - Open up your terminal
    - cd to your desired directory
    - Enter `git clone --recursive thelinkyoucopied`

2. Create a new feature branch
    - cd into the cloned repo
    - Enter `git checkout -b descriptivename`
    - Continue to work in this branch for development. Once tested and production ready, merge to main

3. Merge to main
    - Save your work
        - Enter `git add .`
        - Enter `git commit -m "Descriptive Message"`
        - Enter `git push origin branchname`
    - Checkout to main
        - Enter `git checkout main`
    - Fetch and Pull and Changes
        - Enter `git fetch`
        - Enter `git pull`
    - Attempt to merge
        - Enter `git merge desiredbranch -m "Descriptive Message"`

### How to run video
1. Copy the file path of the video
2. Open src/main.py
3. Change the VIDEO_PATH variable value with the path that was copied