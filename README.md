# Hospital Management CLI

A simple **Command Line Interface (CLI) application** for managing patients, doctors, appointments, and prescriptions using **Python** and **PostgreSQL**.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Schema](#database-schema)
- [Setup & Installation](#setup--installation)


---

## Features

- Add new patients, doctors, appointments, and prescriptions.
- View all patients with full details.
- View appointment history for a specific doctor.
- View appointment history for a specific patient.
- View prescriptions for a specific appointment.
- List doctors with the most appointments.

---

## Tech Stack

- **Python 3.x**
- **PostgreSQL**
- **psycopg2** (PostgreSQL adapter for Python)
- **python-dotenv** (for environment variables)
- **datetime** (for handling dates)

---

## Database Schema

### Tables

#### Patients
| Column         | Type         |
|----------------|--------------|
| id             | SERIAL PRIMARY KEY |
| name           | VARCHAR      |
| age            | INTEGER      |
| phone          | VARCHAR      |
| admission_date | DATE         |

#### Doctors
| Column         | Type         |
|----------------|--------------|
| id             | SERIAL PRIMARY KEY |
| name           | VARCHAR      |
| specialization | VARCHAR      |
| phone          | VARCHAR      |

#### Appointments
| Column          | Type         |
|-----------------|--------------|
| id              | SERIAL PRIMARY KEY |
| patient_id      | INTEGER REFERENCES Patients(id) |
| doctor_id       | INTEGER REFERENCES Doctors(id)  |
| appointment_date| DATE         |
| status          | VARCHAR DEFAULT 'scheduled' |

#### Prescriptions
| Column         | Type         |
|----------------|--------------|
| id             | SERIAL PRIMARY KEY |
| appointment_id | INTEGER REFERENCES Appointments(id) |
| medicine       | VARCHAR      |
| dosage         | VARCHAR      |

---

## Setup & Installation

1. Clone the repository:

```bash
git clone git@github.com:Aayam-Rimal/HospitalManagement.git
cd hospital-management-cli

```

2. Create a virtual environment and activate it

```bash
python -m venv venv
source venv/bin/activate #linux/mac
venv/Scripts/Activate    # windows
```

3. Install dependencies 

```bash
pip install -r requirements.txt
```

4. Set up your .env file with your postgre credentials

- dbname=your_db_name
- user=your_db_user
- password=your_db_password
- host=your_db_host

5. Ensure your PostgreSQL database has the tables created (run the SQL scripts if provided)

---

6. License
- This project is open-source and available under the MIT License

---


Author: Aayam Rimal


