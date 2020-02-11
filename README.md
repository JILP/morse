# Morse Translator

Code challenge 4 MELI

## Table of contents

* [Getting Started](#getting-started)
* [Prerequisites](#prerequisites)
* [Installing](#installing)
* [Versioning](#versioning)
* [Authors](#authors)
* [License](#license)

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine.

### Prerequisites

To clone and run this application, you'll need Git, Python 3 installed on your
computer.

For Debian-based Linux distributions run the next commands with root access:

```bash

# Install python3
apt install python3.6

# Install git 
apt install git
```

### Installing

```bash
# Clone project
$ git clone https://github.com/JILP/morse.git

# Change current working directory
$ cd morse

# Create virtual environment
$ python3 -m venv venv

# Activate environment
$ source venv/bin/activate

# Install project
$ pip install -r requirements.txt


```

### Running the app

To run the app on Flask development web server - Werkzeug:

```bash
# Export FLASK_APP env variable to morse_app.py
$ export FLASK_APP=morse_app.py

# Run Flask
$ flask run

# The app will be running on http://127.0.0.1:5000/
```

To run the app on a production ready web server - Gunicorn:

```bash
# Run Flask on Gunicorn
$ gunicorn morse_app:app

# The app will be running on http://127.0.0.1:8000/
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available,
see the [tags on this repository](https://github.com/JILP/morse/tags). 

## Authors

* **Juan Ignacio López Pecora** - [JILP](https://github.com/JILP)

See also the list of [contributors] who participated in this project.
[contributors]: https://github.com/JILP/morse/contributors

## License

TODO: write license

