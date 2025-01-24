# NCATrak-Mock-System

## Introduction

This software aims to give professors at the [University of Oklahoma Health Science Center](https://www.ouhsc.edu/) a mock database where they can simulate tests on data input to improve the data validity and quality for child advocacy centers.

NOTE: This is a continuation of the project that is being worked on for the Computer Science Capstone of the University of Oklahoma for Spring 2025.
We plan to continue to develop a mock NCAtrak data input/search system used at real Child Advocacy Centers in U.S., and be able to collect biometric data such as mouse movement data, keylogging data, and visually observed data, using many areas of interests (AOIs) defined within each form of the mock NCAtrak data input/search system. 
The mock system can be helpful for the potential National Institute of Health (NIH) project collaborations between DSA (ISE) and OUHSC.

## Requirements

-   [Anaconda](https://docs.anaconda.com/)
-   [PostgreSQL](https://www.postgresql.org/)
-   [Python](https://www.python.org/downloads/)

## Installation

### Anaconda Setup Instructions

This section will walk you thorough the installation and setup of Anaconda, which ensures that all of our code is cross-platform compatible.

#### Step 1: Install Anaconda

Follow Anaconda's [Installation Guide](https://docs.anaconda.com/anaconda/install/). Be sure to select the correct guide for your operating system.

#### Step 2 (Windows): Setup a Virtual Environment

Please follow the [guide provided by Anaconda](https://docs.anaconda.com/navigator/tutorials/manage-environments/#importing-an-environment)

#### Step 2 (Linux / Mac): Setup a Virtual Environment 

- On Linux or MacOS
- Navigate to the folder containing the current version of the NCA mock system using the command:

```shell
cd directory/of/mock/system/install
```

- Run the following command to create a virtual environment called NCA-Trak that installs all of the dependencies listed in the environment.yml file:

```shell
conda env create -n 'put_a_name' --file environment.yml
```

- Activate the virtual environment by running the command:

```shell
conda activate 'previously_put_name'
```

- Verify the virtual environment is running by entering the command 

```shell
conda info
```

and confirming that the 'active environment' is "NCA-Trak". Then, verify that all of the dependencies have been installed by running the command

```shell
conda list
```

and confirming that all of the packages listed in the environment.yml file are listed. *Note: there will be more packages listed than are included in the environment.yml file. This is fine - just be sure that all of the desired packages are included in the list.*


Once all packages have been installed, your Anaconda VNV should now be up and running!

### Database Setup Instructions

The purpose of this section is to walk you through setting up the initial database on your local machine so that you can run all of the programs we have developed so far. 

#### Step 1: Install PostgreSQL

Follow PostgreSQL's [Installation Guide](https://www.postgresqltutorial.com/postgresql-getting-started/). Depending on your operating system select the walkthrough guide provided by PostgreSQL to ensure correct installation.

*NOTE: For MacOS and/or Linux, you may skip the portion of the walkthrough titled “Load the sample database.” This section walks through creating a sample database that is not needed to run the code for this project.*

#### Step 2: Create Database

- First, open psql, the PostgreSQL terminal. To do this, open either Command Prompt (on Windows machines) or the terminal (on UNIX-like machines), and enter the command 

```shell
psql -U postgres
```

- When prompted, enter the password you chose during the installation in Step 1. The command prompt will change to look like this:

```shell
postgres=#
```

- Enter the command

```shell
CREATE DATABASE 'database_name';
```

- You can now exit psql by entering the command:

```shell
exit
```

### Configuring the Database

- Navigate to the folder where you installed the project

```shell
cd directory\of\mock\system\install
```

example:
```shell
cd D:\Dev\NCATrak-Mock-System
```

- Go into the app folder

```shell
cd app
```

- Run the wizard.py file

```shell
python wizard.py
```

- Input 1 and follow the steps, your input should look something like this to begin
```shell
Please Select From the following options:

[1] Complete Install
[2] Added New Generated Data

1
Enter the host
: localhost
Enter the database name
: test_setup_database
Enter user name
: postgres
Enter password
: password
Enter 
Custom Port (most likely not)? If so enter the port #### else hit enter
: (hit enter)
```

```Shell
How many data entries would you like to be generated?
50 ## We have generated up to 10,000 at one time before, so consider that the max tested limit.
Generating Data...
```

- After finishing the wizard, you should be able to run `app.py` in the current directory you are in. ie `D:\Dev\NCATrak-Mock-System\app`

```shell
python app.py
```

Shield: [![CC BY-NC 4.0][cc-by-nc-shield]][cc-by-nc]

This work is licensed under a
[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by-nc].

[![CC BY-NC 4.0][cc-by-nc-image]][cc-by-nc]

[cc-by-nc]: https://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg
