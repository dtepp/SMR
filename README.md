# SMR

## SECTION 5 : Installation and User Guide

### [ 1 ] System Environment Requirement

1. Install [PostgreSQL](https://www.postgresql.org/download/) on the computer

2. Install [python >=3.9](https://www.python.org/downloads/)

3. Google Chrome (latest version)

4. Install latest git version

### [ 2 ] Prepare basic project enviorment and create an virtual enviorment of python

1. Create a folder in computer to storage the project file and open a terminal in this folder:

 >git clone https://github.com/dtepp/SMR.git

 >cd SMR

 >python -m venv venv

 >venv\Scripts\activate(windows) OR: source venv/bin/activate(mac)

 >pip install -r requirements.txt

2. Open pgAdmin program on your computer and create a Databases call SchoolMajor

3. Use the db file to restore the SchoolMajor database
![image](https://user-images.githubusercontent.com/38468080/221103673-6f3b7283-c045-4835-b29f-c659a4c2627c.png)


### [ 3 ] Deploy the School Major Recommend system locally with virtual enviorment just created

1. In project folder terminal using virtual environment: 

 >flask db migrate
 
 >flask db upgrade
 
 >flask run


### [ 4 ] Run the systems on browser
Go to URL using web browser**http://127.0.0.1:5000
Or: Directly click the link on the frontend terminal
