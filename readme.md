<div align="center">

  <h3 align="center">Monit-App</h3>

  <p align="center">
    A python app that monitors your system
    <br />
    <a href="https://gitlab.com/ogb4n/tp-réseau-b2"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <!-- <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a> -->
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

This is a school project that aims to monitor a system. It is written in python and uses the psutil library. I also use a mongodb database to store the reports data and a web interface to display the data using Flask and pyMongo.

This app will receive updates in the future since it is a projetct i'd loved to work on.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- Python and most of native libraries, psutil, pyMongo, Flask
- mongodb

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

Clone the repository on your machine

Be sure having python and ip installed on your machine

### Prerequisites

You will need python and pip installed on your machine. You will also need to install the required libraries.

### Installation

2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```

<br>

3. Go into the app directory and run the command `pip install -r requirements.txt` to install the required libraries
   ```sh
   pip install -r requirements.txt
   ```

<br>

4. Go into the /app folder and edit the `config.json.example` file <br>
   it should look like this:

   ```js
   {
    "ports":[list of ports],
    "log_dir" : "/var/log/monit/",
    "rapport_dir" : "/var/monit/reports/",
    "local_api_mode": true
    }
   ```

   You can change the ports to monitor, the log directory and the report directory. You can also change the local_api_mode to false if you want to use the web interface on another machine, or to turn it off.

   _More values will be added in the future_

<br>

5. Still in the /app folder, run the ./install.sh script as admin to install the app

   ```sh
   sudo ./install.sh
   ```

   This will install the app as a service and will start it.

<br>

### You enabled the local_api_mode

6. go back to the /api folder and run the command `pip install -r requirements.txt` to install the required libraries

   ```sh
   pip install -r requirements.txt
   ```

<br>

7. Still into the /api folder, run the command 'monit-api.py' to start the api

   ```sh
   python monit-api.py
   ```

   The api will be available at 'http://localhost:8085/'

 <br>

If you enabled the local_api_mode, you can now go to http://localhost:8085/ to see the web interface.

### You disabled the local_api_mode

Otherwise, you can run the app with the command

```sh
monit
```

and use `monit -h` to see the available commands.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

This app is meant to be used as a service. It will monitor the system and store the data in a mongodb database. You can then use the web interface to see the data.

You can also use the command line to see the data, especially if you do not want to export your datas but prefer storing it on the system. Use `monit -h` to see the available commands.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Add logs
- [x] Add local_api_mode
- [x] Add web interface
- [ ] Add multiple machines monitoring
- [ ] Add Additional Templates & routes

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Project Link: [https://gitlab.com/ogb4n/b2-linux/-/tree/main/TP3-DEV](https://gitlab.com/ogb4n/b2-linux/-/tree/main/TP3-DEV)

Github: [ogb4n](https://github.com/ogb4n)

Discord : uptoban

mail : <a href="mailto:contact@doniban.fr">contact@doniban.fr</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>
