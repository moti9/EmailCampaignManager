# Email Campaign Manager

The Email Campaign Manager is a web application that allows you to create and manage email campaigns. It provides a simple interface for creating campaigns, managing subscribers, and sending emails.

## Features

---

- Create and manage email campaigns
- Add and manage subscribers
- Send emails to subscribers

## Setup in local-environment

---

### Clone the repository:

```bash
$ git clone https://github.com/moti9/EmailCampaignManager
```

---

### Create a virtual environment (Recommended pipenv)

- It is recommended to use a virtual environment to keep the project dependencies separate from other Python projects on your machine.
- To create a virtual environment, follow these steps:

- Navigate to the project directory:

```bash
$ cd <project-name>
```

- Install dependencies:

```bash
$ pip install -r requirements.txt

or

$ pipenv sync

```

- Activate the virtual environment:

  - On macOS/Linux: `$ source venv/bin/activate`

  - On Windows: `$ venv\Scripts\activate.bat`
    <br/>
    `$ .\<name-env>\Scripts\activate`

---

# Note:

## Make sure you have completed the setup of database, smtp configuration properly in `settings.py`
