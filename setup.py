import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn=psycopg2.connect(
    dbname=os.getenv('dbname'),
    user=os.getenv('user'),
    password=os.getenv('password'),
    host=os.getenv('host')
)

cursor=conn.cursor()

create_Patients= """
CREATE TABLE IF NOT EXISTS Patients(
id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
name VARCHAR(50),
age INT,
phone VARCHAR(50),
admission_date DATE

);

"""

create_Doctors= """
CREATE TABLE IF NOT EXISTS Doctors(
id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
name VARCHAR(50),
specialization VARCHAR(50),
phone VARCHAR(50)

);

"""

create_Appointments= """
CREATE TABLE IF NOT EXISTS Appointments(
id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
patient_id INT NOT NULL REFERENCES Patients(id) ON DELETE CASCADE,
doctor_id INT NOT NULL REFERENCES Doctors(id) ON DELETE CASCADE,
appointment_date DATE NOT NULL,
status TEXT DEFAULT 'scheduled',
UNIQUE(patient_id,doctor_id,appointment_date)

);


"""

create_Prescriptions= """
CREATE TABLE IF NOT EXISTS Prescriptions(
id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
appointment_id INT NOT NULL REFERENCES Appointments(id) ON DELETE CASCADE,
Medicine TEXT NOT NULL,
dosage TEXT

);

"""

cursor.execute(create_Patients)
cursor.execute(create_Doctors)
cursor.execute(create_Appointments)
cursor.execute(create_Prescriptions)

conn.commit()

cursor.close()
conn.close()
