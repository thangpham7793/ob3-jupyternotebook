# ob3-jupyternotebook

### Make A Python Virtual Env

Make a new folder and open a terminal from the folder.

Type in: python -m venv ob3-notebook (or other name you prefer)

Change directory into the virtual env (important!): 

cd ob3-notebook

Activate your virtual env (important!): 

source scripts/activate

If you see (ob3-notebook) in the terminal then it's activated.

### Clone the Git Repo

From the terminal (make sure that you're inside the virtual env folder), type:

git clone https://github.com/thangpham7793/ob3-jupyternotebook.git

This will create a new folder name ob3-jupyternotebook. Cd into the folder:

cd ob3-jupyternotebook

In there you should see all the files from the repo. Now we'll use pip to install all require python packages into our virtual env. 
This is similar to 'npm install'.

pip3 install -r requirements.txt

Once the installation is finished, open the jupyternotebook inside the folder and run the SET UP cell. 
It should display a row of result unless there's an error. 
Next, please follow the 2 examples and afterward you can start working with Cassandra inside this Jupyternotebook!
