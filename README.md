# WinnerAlgorithm

WinnerAlgorithm is a Python-based web application built with Flask. It is designed to provide a dynamic user experience while keeping configuration secure and flexible through the use of environment variables. This README contains all the details you need to get started, including a complete file structure overview.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [File Structure](#file-structure)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
---

## Prerequisites

Before starting, ensure that you have the following installed:

- **Python 3.x**  
  [Download and install Python](https://www.python.org/downloads/).

- **Pip**  
  Python's package installer (usually comes with Python).

- **Virtual Environment (Recommended)**  
  To manage dependencies without affecting your global Python installation.

---
## File-structure
The project follows a specific structure to organize files properly. Ensure your project directory looks like this:

```
WinnerAlgorithm/
├── app.py                # Main application file containing the backend logic
├── requirements.txt      # List of required Python libraries for the application
├── .env                  # Environment variables configuration file (if applicable)
├── templates/
│   └── index.html        # Main HTML file that renders the web interface
└── static/
    └── css/
        └── style.css     # CSS file for styling the application
```

**Important**

The index.html file must be placed inside the templates folder.
The style.css file should reside in the static/css directory.


### Environment Variables
WinnerAlgorithm utilizes environment variables to handle configurations securely. These can be defined in your shell or via a .env file if you're using a package like python-dotenv

### Running the Application
If your setup supports direct execution, you can run using:

```
python app1.py
```
