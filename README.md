# RevoU Project Milestone 3

Hello my name is Raden Wisnu Andhika Pranidhia. This is a project assignment from RevoU focused on creating a secure and intuitive Flask API for a banking application. The API offers various features for account management, user authentication, and transactions.

For API documentation, click [here](https://documenter.getpostman.com/view/33841449/2sA3dyir9T) (Note: Since the API is deployed using free services, it may take a few attempts to access it initially)

If you have any question or anything else regarding the project, feel free to contact me via [linkedin](https://www.linkedin.com/in/raden-wisnu-andhika-pranidhia-b17a16196/), [email](mailto:radenwisnu21@gmail.com). I am open to any criticism and suggestion. Thank you!

## UPDATE

For the Flask API has been deployed on [Render.com](https://render.com/) using a database hosted on [Filess.io](https://filess.io/) for easier access and testing.

The deployed back-end API can be accessed [here](https://banking-application-rwandhika.onrender.com).

## IMPORT API DOCUMENTATION TO POSTMAN

Using Postman makes it easier to test and consume the API. Click the link for API documentation above or [here](https://documenter.getpostman.com/view/33841449/2sA3dyir9T).

To import the API into Postman:

1. Inside the API documentation page, click the "Run in Postman" button in the top right.

2. Choose between using Postman in your web browser or the Postman client.

3. Select the workspace you want to import the documentation into.

4. Don't forget to change the environment variable to "Online" in the top right to use the correct API URL.

For a visual guide, follow the GIF below:

![Postman Import Gif](/import_postman_tutorial.gif)

## PREREQUISITES (FOR LOCAL SETUP)

Ensure the following are installed:

- MySQL Workbench (or any MySQL-compatible client)
- Python 3.x
- Flask
- Pipenv (for virtual environment management)

## CREATE DATABASE (FOR LOCAL)

For this project, I use MySQL Workbench to create a local database

```sql
CREATE DATABASE milestone_3;

USE milestone_3;

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

CREATE TABLE accounts(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER,
    account_type VARCHAR(255),
    account_number VARCHAR(255) UNIQUE,
    balance DECIMAL(10, 2),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE transactions(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    from_account_id INTEGER,
    to_account_id INTEGER,
    amount DECIMAL(10, 2),
    type VARCHAR(255),
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_account_id) REFERENCES accounts(id),
    FOREIGN KEY (to_account_id) REFERENCES accounts(id)
);
```

## CLONE PROJECT (FOR LOCAL)

To clone the project locally, follow these steps:

1. Create a new directory (replace `newdirectory` with your desired name):

    ```bash
    mkdir newdirectory
    cd newdirectory
    ```

2. Clone the repository:

    ```bash
    git clone https://github.com/RWAndhika/milestone-3-RWAndhika.git
    ```

## CONFIGURE DATABASE CONNECTION (FOR LOCAL)

1. Add an `.env` file to the root of your project directory to connect to your local database:

    ```bash
    DB_USERNAME=root
    DB_PASSWORD=
    DB_HOST=127.0.0.1
    DB_DATABASE=milestone_3

    SECRET_KEY=your_secret_key
    ```

2. Update the `/connectors/mysql_connector.py` file to connect to the local MySQL database:

    ```python
    from sqlalchemy import create_engine
    import os

    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_DATABASE")

    # Connect to Database
    print("Connecting to MySQL Database")
    engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}/{database}')

    connection = engine.connect()
    print("Successfully connected to MySQL Database")
    ```

This will change the back-end configuration to connect to your local MySQL database instead of the deployed one.

## INITIALIZE PROJECT (FOR LOCAL)

1. Install dependencies from the `Pipfile`:

    ```bash
    pipenv install
    ```

2. Activate the virtual environment:

    ```bash
    pipenv shell
    ```

3. Run the application:

    ```bash
    flask --app index run
    ```

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/hMIDAFdr)
