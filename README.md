## Start Machine Learning project.

### Software and account Requirement.

1. [Github Account](https://github.com)
2. [Heroku Account](https://dashboard.heroku.com/login)
3. [VS Code IDE](https://code.visualstudio.com/download)
4. [GIT cli](https://git-scm.com/downloads)
5. [GIT Documentation](https://git-scm.com/docs/gittutorial)


creating conda environment
...
conda create -p venv python==3.7 -y
...
list environment
...
conda env list
...
activate env
...
conda activate venv/
...

...
pip install -r requirements.txt
....


TO add files to git
...
git add.  OR git add <file_name>
....

to commit file
...
git commit -m "comment"
...

To send version/changes to github
...
git push origin <branch_name>
...

To check remote url
...
git remote -v
...

-------------------------------------------------------
To setup CI/CD pipeline in heroku we need 3 information
-------------------------------------------------------

1. HEROKU_EMAIL = nishit.2571988@gmail.com
2. HEROKU_API_KEY = fedc8c69-8a78-4b5c-862c-0935d704440a
3. HEROKU_APP_NAME = ml-regression-first15


-----------------
Create Dockerfile
-----------------
create dockerignore file
------------------------
BUILD DOCKER IMAGE
------------------------
docker build -t <image_name>:<tagname> .
-------------------------
Note: Image name for docker must be lowecase


To list docker Image
--------------
docker images
--------------

Run docker image
-----------
docker run -p 5000:5000 -e PORT=5000 <IMAGE_ID>
-------------

To check running docker container
----------------
docker ps
----------------

To stop docker container
-------------
docker stop <container_id>
-------------