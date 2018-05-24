# Log Anaylsis Project

A reporting tool that prints out reports (in plain text) based on the data in the database

## Installation

1. You will first need `virtualenv` on your system first

    ```bash
    pip install virtualenv
    ```

2. Then to install log_analysis

    ```bash
    git clone https://github.com/Scheercuzy/FSND-log-analysis-project.git
    cd log_analysis/
    virtualenv -p python3 env
    source env/bin/activate
    pip install .
    ```

## Usage

Below are the answers the python script will be answering:

1. What are the most popular three articles of all time?

2. Who are the most popular article authors of all time?

3. On which days did more than 1% of requests lead to errors?

Make sure you are in the virtual environment when you run the code:

```bash
source env/bin/activate
```

To get the answer to all the questions run:

```bash
logA -a all
```

if you want to get the answers one at the time (replace `question_number` with the question you want answered):

```bash
logA -a question_number
```

### Output the file

If you want to output the answers to a file, add `> filename.txt` at the end of your command, like below:

```bash
logA -a all > answer.txt
```

The answer file will be located in the directory you ran the command