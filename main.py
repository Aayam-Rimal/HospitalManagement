import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

conn=psycopg2.connect(
    dbname=os.getenv('dbname'),
    user=os.getenv('user'),
    password=os.getenv('password'),
    host=os.getenv('host')
)

cursor=conn.cursor()


def add_patient_details():
    try:
            print("Add patients details\n")
            name=input("Enter name of patient: ")
            age=int(input("Enter age of patient: "))
            phone= input("Enter phone of patient: ")
            user_input = input("Enter appointment date (YYYY-MM-DD): ")
            admission_date = datetime.strptime(user_input, "%Y-%m-%d").date()
            print("-"*50)

            print("Add doctors details\n")
            doc_name= input("Enter name of doctor: ")
            specialization= input("Enter doctors specialization: ")
            doc_num= input("Enter Doctors phone number: ")

            print("Enter Appointment Details\n")
            app_date= input("Enter appointment date in YYYY-MM-DD: ")
            appointment_date= datetime.strptime(app_date, "%Y-%m-%d").date()

            print("Enter prescription\n")
            Meds= input("Enter medicine: ")
            Dosage= input("Enter dosage: ")

            cursor.execute("INSERT INTO Patients(name,age,phone,admission_date) VALUES(%s,%s,%s,%s) RETURNING id",(name,age,phone,admission_date))
            patient_id=cursor.fetchone()[0]

            cursor.execute("INSERT INTO Doctors(name,specialization,phone) VALUES(%s,%s,%s) RETURNING id",(doc_name,specialization,doc_num))
            doctor_id=cursor.fetchone()[0]

            cursor.execute("INSERT INTO Appointments(patient_id,doctor_id,appointment_date) VALUES(%s,%s,%s,%s) RETURNING id",(patient_id,doctor_id,appointment_date))
            appointment_id= cursor.fetchone()[0]

            cursor.execute("INSERT INTO Prescriptions(appointment_id,Medicine,dosage) VALUES(%s,%s,%s)",(appointment_id,Meds,Dosage))
            
            conn.commit()

    except Exception as e:
            print("Error occured",e)
            return



def view_all_patients():
    cursor.execute("""SELECT id, name, age, phone, admission_date
                          FROM Patients;""")
    rows= cursor.fetchall()

    if not rows:
            print("No patient at all!")
    else:
        for id,name,age,phone,admission_date in rows:
            print(f"{id}|{name}|{age}|{phone}|{admission_date}")
    return

def view_doc_appts():
    try:
        doc_id= int(input("Enter valid doc id to search appointment history: "))
        cursor.execute("""
                    SELECT d.name AS doctor_name,       
                            p.name AS patient_name,
                            a.appointment_date,
                            a.status
                        FROM Appointments a
                        JOIN Doctors d ON a.doctor_id = d.id
                        JOIN Patients p ON a.patient_id = p.id
                        WHERE d.id=%s
                        ORDER BY d.name, a.appointment_date; """,(doc_id, ))
        rows=cursor.fetchall()

        if not rows:
            print("No history for this doctor")
        else:
            for dname,pname,appointmentdate,status in rows:
                print(f"{dname}|{pname}|{appointmentdate}|{status}")
        
    except ValueError:
        print("Invalid input!enter number!")
        return
        
        
def view_patients_history():
    try:
        p_id= int(input("Enter valid patient id to see appointment history:"))
        cursor.execute(""" 
                    SELECT p.name as patient_name,
                            d.name as doctor_name,
                            a.appointment_date
                    FROM Appointments a
                    JOIN Patients p on a.patient_id=p.id
                    JOIN Doctors d ON a.doctor_id=d.id
                    WHERE p.id=%s
                ORDER BY p.name, a.appointment_date; """,(p_id, ))
        
        rows=cursor.fetchall()

        if not rows:
            print("This patient does not exist!")
        else:
            for pname,dname,appdate in rows:
                print(f"{pname}|{dname}|{appdate}")
        

    except ValueError:
        print("Invalid input! enter a number")
        return
    
def view_prescriptions():
    try:
        appt_id= int(input("enter a valid appointment id to see prescription: "))
        cursor.execute(""" SELECT p.Medicine,p.dosage, a.appointment_date
                    FROM Prescriptions p
                    JOIN Appointments a on a.id=p.appointment_id
                    WHERE a.id=%s ; """, (appt_id, ))
        
        rows=cursor.fetchall()

        if not rows:
            print("No history for this appointment")
        else:
            for meds,dose,adate in rows:
                print(f"{meds}|{dose}|{adate}")
        

    except ValueError:
        print("Invalid id!!")
        return
    
def view_top_docs():
    cursor.execute("""SELECT d.name as doctor_name,
                                 COUNT(a.id) as total_appointment
                          FROM Appointments a
                          JOIN Doctors d ON a.doctor_id= d.id
                          GROUP BY d.name
                          ORDER BY total_appointment DESC ;""")
    rows=cursor.fetchall()

    if not rows:
        print("Cannot fetch the doctors!")
    else:
        for name,totalapp in rows:
            print(f"{name}|{totalapp}")
    return


while True:
    print("""Menu
                1. Add patient,Doctor,Appointment
                2. View all patients
                3. View doctors appointments
                4. View patients appointment history
                5. Prescriptions for an appointment
                6. Doctors with most appointments 
                7. Quit the menu """)
    try:
       choice=int(input("Enter task to perform: "))
    except ValueError:
        print("Invalid choice!! retry!")
        continue

    if choice==1:
        add_patient_details()
        
    elif choice==2:
        view_all_patients()
             
    elif choice==3:
        view_doc_appts()
             
    elif choice==4:
        view_patients_history()
       
    elif choice==5:
        view_prescriptions()
       
    elif choice==6:
        view_top_docs()

    elif choice==7:
        break
        
cursor.close()
conn.close()







        




            



