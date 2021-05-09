# trufla_task

### Clone the project

You just need to open terminal

```sh
$ git clone https://github.com/TEha1/trufla_task.git
$ cd trufla_task
```

### Create and activate python environment

You can check that out [Creation of virtual environments](https://docs.python.org/3/library/venv.html#module-venv).

```sh
$ python3 -m venv env
$ source env/bin/activate
```

### Install requirements

You can check that out [pip install](https://pip.pypa.io/en/stable/cli/pip_install/#pip-install).

```sh
$ pip install -r requirements
```

### Run the project

```sh
# csv files
$ python parser.py csv files/customers.csv files/vehicles.csv

# xml files
$ python parser.py xml files/customer1.xml
$ python parser.py xml files/customer2.xml
```

### Check the output results

```sh
$ cd json/
$ cat results.json
```
