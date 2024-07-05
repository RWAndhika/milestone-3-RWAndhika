# RevoU Project Milestone 3

Hello my name is Raden Wisnu Andhika Pranidhia. This is a project assignment from RevoU about making a secure and intuitive Flask API for a banking application. The API offer various features for account management, user authentication, and transactions.

For API documentation, you can click [here](https://documenter.getpostman.com/view/33841449/2sA3dyir9T)

If you have any question or anything else regarding the website, feel free to contact me at [linkedin](https://www.linkedin.com/in/raden-wisnu-andhika-pranidhia-b17a16196/), [email](mailto:radenwisnu21@gmail.com). I am open to any criticism and suggestion. Thank you!

## CREATE DATABASE

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

## Clone project

change newdirectory to the desired name:

```bash
mkdir newdirectory
```

```bash
cd newdirectory
```

```bash
git clone https://github.com/RevoU-FSSE-4/milestone-3-RWAndhika.git
```

## add .env file to connect to your local database

You can add new file named .env and then place it inside the root of the folder

```bash
DB_USERNAME=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_DATABASE=your_database_name

SECRET_KEY=your_secret_key
```

## Initialize your project

install package inside the pipenv file:

```bash
pipenv install
```

init pipenv virtual environment:

```bash
pipenv shell
```

run app:

```bash
flask --app index run
```

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/hMIDAFdr)
