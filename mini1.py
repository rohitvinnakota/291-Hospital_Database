'''
CMPUT 291 mini project 1
Created by: Rohit Vinnakota, Kaiyi Song, Musaed Alsobaie
No additional sources used
'''

from __future__ import print_function
import sqlite3
import hashlib


# Does the doctor prescribe the drug in the time specified?
def is_no_prescription_during_time_period(dic, name_of_doctor ,lists):
    true_or_false = 0
    for rows in range(len(lists)):
	if dic[name_of_doctor] in lists[rows][0]:
	    true_or_false = 1
    return true_or_false

#Creates a patient object and adds it to the patients table in the database
def create_patient(hcno):
    name = raw_input("Enter the patient's name ")
    age_group = raw_input("Enter the age_group ")
    address = raw_input("Enter the address ")
    phone = raw_input("Enter the phone no ")
    emg_phone = raw_input("Enter the emergency phone no ")
    query = ("INSERT INTO patients VALUES ('" + hcno +"','"+name+"','"+age_group+"','"+address+"','"+phone+"','"+emg_phone+"');")
    c.execute(query)
    conn.commit()
    
#Sums up the drug amount and returns value for printing
def drug_sums(lists, staff_id_list, i,start_date, end_date):
    a = Staff()
    amt_sid_dname = ("SELECT SUM(m.amount), m.staff_id, m.drug_name FROM medications m WHERE date(m.mdate) >= '"+ str(start_date)+ "' AND date(m.mdate) < '"+ str(end_date) +"' AND m.staff_id = '"+ str(staff_id_list[i]) +"' GROUP BY m.drug_name;") 
    c.execute(amt_sid_dname)
    list_amt_sid_dname = list(c.fetchall())
    for row in range(len(list_amt_sid_dname)):
        if list_amt_sid_dname[row][2] == lists:
            return list_amt_sid_dname[row][0]
    
#  Creates a new chart and also checks if the patient exists              
def create_chart(hcno):
    patient_checker = ("SELECT * FROM patients WHERE hcno = '" + hcno + "'")
    c.execute(patient_checker)
    if len(c.fetchall()) == 0:
        print("The patient does not exist. Creating a new patient")
        create_patient(hcno)
            
    chart_id = raw_input("Enter a non-existent chart_id ")
    query = ("INSERT INTO charts VALUES('"+chart_id+"',"+"'"+hcno+"',"+"date('now'),NULL);")
    c.execute(query)
    conn.commit()

# shows all the data in the charts for a given HCNO
def charts():
    hcno = raw_input("Enter the patient's hcno ")
    query = ("SELECT * FROM charts WHERE hcno = "+(hcno)+" ORDER BY adate;")
    query2 = ("SELECT COUNT(*) FROM charts WHERE hcno = "+(hcno)+" " + " ORDER BY adate;")
    count_rows = c.execute(query2)
    count_row = count_rows.fetchone()[0]
    c.execute(query)
    list_charts = c.fetchall()
    for i in range(count_row):
        if list_charts[i][3] is None: #chart open
            c.execute("SELECT chart_id FROM charts WHERE"+ "'"+(list_charts[i][0])+"'" + "=chart_id"+ ";")
            print(c.fetchone()[0]+" is open")
        else: #chart closed
            c.execute("SELECT chart_id FROM charts WHERE "+ "'"+(list_charts[i][0])+"'"+ " = chart_id;")
            print(c.fetchone()[0]+" is closed")      
    select_chart = raw_input("Enter an open chart ID to view details: ") 
    c.execute("SELECT * FROM symptoms WHERE chart_id = '" + select_chart + "' ORDER BY obs_date ; ")
    print("Symptoms: \n" + str(c.fetchall()) )
    c.execute("SELECT * FROM diagnoses WHERE chart_id = '" + select_chart + "' ORDER BY ddate;")
    print("Diagnoses: \n"+  str(c.fetchall()) )
    c.execute("SELECT * FROM medications WHERE chart_id = '" + select_chart + "' ORDER BY mdate;")
    print("Medications: \n" + str(c.fetchall()) )    


# Closes a chart given the current day
def close_chart():
    chart_option = raw_input("List an open chart('now')) WHEREss chart_id = '" + chart_option + "';")
    c.execute(query)
    conn.commit()
    
#Inserts a new entry into the medication colums        
def execute_medication(hcno,chart_id,staff_id,amt,start_med,end_med,drug):
    query = ("INSERT INTO medications VALUES('"+hcno+"','"+chart_id+"','"+staff_id+"',"+"date('now')"+",'"+start_med+"','"+end_med+"',"+amt+",'"+drug+"');")
    c.execute(query)
    conn.commit()
    
#when a doctor logs in, calls the list of options function for the doctor to choose from        
class Doctor:
    def __init__(self):
        return
    def list_of_options(self,doc_id):
	while(1==1):
	    doc_option = raw_input("You have the following options \n Press 1 to access patient chart selection \n Press 2 to add an entry to a patient's symptoms \n Press 3 to add a diagnosis for a patient \n Press 4 to add a medication for the patient \n. Press anything else to logout ")
	    if(doc_option == "1"):
		charts()
    
	    elif(doc_option == "2"):
		print(doc_id)
		hcno = raw_input("Enter the patient's hcno: ")
		chart_id = raw_input("Enter the patient's open chart ID: ")
		#Maybe add a clause for a closed chart
		symptom = raw_input("Enter the symptom the patient is displaying")
		query = ("INSERT INTO symptoms VALUES("+hcno+",'"+chart_id+"','"+doc_id+"',"+"date('now')"+",'"+symptom+"');");
		c.execute(query)
		conn.commit()
	    elif(doc_option == "3"):
		hcno = raw_input("Enter the patient's hcno: ")
		chart_id = raw_input("Enter the patient's open chart ID: ")
	      #Maybe add a clause for a closed chart
		diagnosis = raw_input("Enter the diagnosis")
		query = ("INSERT INTO diagnoses VALUES('"+hcno+"','"+chart_id+"','"+doc_id+"',"+"date('now')"+",'"+diagnosis+"');");
		c.execute(query)
		conn.commit()
		#execute the query          
	    elif(doc_option == "4"):
		hcno = raw_input("Enter the patient's hcno: ")
		chart_id = raw_input("Enter the patient's open chart ID: ")
		drug = raw_input("Enter an entry for medications: ")
		amt = raw_input("Enter the dosage amount")
		start_med = raw_input("Enter medication start date")
		end_med = raw_input("Enter medication end date")
		age_group_query = ("SELECT age_group FROM patients WHERE hcno = '" + hcno +"';");
		c.execute(age_group_query)
		age_group = c.fetchone()[0]
		dosage_check_query = ("SELECT sug_amount FROM dosage WHERE age_group = " +"'"+str(age_group)+"'"+" AND drug_name = '" +str(drug) + "';")
		c.execute(dosage_check_query)
		sug_amt = c.fetchone()[0]
		if int(amt) > sug_amt:
		    warning = raw_input("The suggested amount for this patient's age group is " + str(sug_amt) + " Do you wish to continue?. Press N for No and anything else for yes: ")
		    if warning == "n":
			break
		query = ("SELECT r.drug_name,i.canbe_alg FROM inferredallergies i, reportedallergies r WHERE i.alg = r.drug_name AND r.hcno = '"+hcno+"';")
		c.execute(query)
		x = c.fetchall()
		for i in range(len(x)):
		    if (x[i][1] == drug):
		        warning = raw_input("The patient reported being allergic to " + x[i][0] + " and may be allergic to " + x[i][1] + " Do you wish to continue? Press n for no or anything else for yes: ")
		        if warning == "n":
		            break
		execute_medication(hcno,chart_id,doc_id,amt,start_med,end_med,drug)
		    
		    
		    
		
	    else:
		break
		
            # if dosage_check > amount, show warning;
            # if there is an allergy, show warning; 
	    
#when a nurse logs in, calls the list of options function for the nurse to choose from  
class Nurse:
    def __init__(self):
        return   
    def nlist_of_options(self,n_id):
	while(1==1):
	    nurse_option = raw_input("You have the following options: \n Press 1 to create a new chart \n Press 2 to close a chart \n Press 3 to access patient chart selection  \n  Press 4 to add an entry to a patient's symptoms. Press anything else to logout ")
	    if(nurse_option == "1"):
		hcno = raw_input("List the patient's hcno")
		open_checker = ("SELECT * FROM charts WHERE hcno = '"+hcno+"' AND edate IS NULL")
		c.execute(open_checker)
		if(len(c.fetchall())) != 0:
		    choice = raw_input("This patient has an open chart. Would you like to close it?. Press Y for yes and anyhting else for No")
		    if(choice == "Y"):
			close_chart()
			create_chart(hcno)
		else:
		    create_chart(hcno)
		
		
	    elif(nurse_option == "2"):
		close_chart()
    
		
	    elif(nurse_option == "3"):
		charts()
		
	    elif(nurse_option == "4"):
		hcno = raw_input("Enter the patient's hcno: ")
		chart_id = raw_input("Enter the patient's open chart ID: ")
		#Maybe add a clause for a closed chart
		symptom = raw_input("Enter the symptom the patient is displaying")
		query = ("INSERT INTO symptoms VALUES("+hcno+",'"+chart_id+"','"+doc_id+"',"+"date('now')"+",'"+symptom+"');");
		c.execute(query)
		conn.commit()		
	    else:
		break
	    

 
          
#when Staff logs in, calls the list of options function for the Staff to choose from        
class Staff:
    def __init__(self):
        return   
    def slist_of_options(self,s_id):
	while(1==1):
	    staff_option = raw_input("You have the following options: \n Press 1 to see a report of the each doctor and the amount of drug that the doctor prescribed  \n  Press 2 to see for each category, total amount prescribed for each drug in that category  \n  Press 3 to see a list of all possible medications for a given diagnosis  \n  Press 4 to see diagnoses that have been made for a given drug. Press any other key to logout ")
	    if(staff_option=="1"):
		start_date = raw_input("Enter start date of drug prescribed in the form YYYY-MM-DD: ")
		end_date = raw_input("Enter end date of drug prescribed in the form YYYY-MM-DD: ")
	     
		sid_drugs = ("SELECT DISTINCT m.staff_id, m.drug_name FROM medications m WHERE date(m.mdate) >= '" + str(start_date) + "' AND  date(m.mdate) < '" + str(end_date) + "'; ")
		c.execute(sid_drugs)
		list_sid_drugs = list(c.fetchall())
		
		select_doctor = ("SELECT staff_id,name FROM staff WHERE role='D'; ")
		list_doctor = c.execute(select_doctor)
		convert_list_doctor = list(c.fetchall())
		name_list = [x[1] for x in convert_list_doctor] #extracts doctor names from tuple in list
		staff_id_list = [x[0] for x in convert_list_doctor]	 
		
		dic = {}
		for i in range(len(name_list)):
		    dic[name_list[i]] = staff_id_list[i]
		    dic[staff_id_list[i]] = name_list[i]
		  
		    
		    
		for i in range(len(staff_id_list)):
		    did_doctor_prescribe = is_no_prescription_during_time_period(dic, str(dic[staff_id_list[i]]), list_sid_drugs)  #dic, current doctor, drug list
		    if did_doctor_prescribe == 1:
           		print(str(dic[staff_id_list[i]]) + " prescribed (drug name | drug amount) : ")     
		    for drug in range(len(list_sid_drugs)):
           		if str(staff_id_list[i]) == list_sid_drugs[drug][0]:
          			a = drug_sums(list_sid_drugs[drug][1], staff_id_list, i,start_date, end_date)
          			dname_amt = ("{} | {}").format(str(list_sid_drugs[drug][1]) , str(a))
          			print(dname_amt)
		    
	    elif (staff_option =="2"):
		start_date = raw_input("Enter start date of drug prescribed in the form YYYY-MM-DD: ")
		end_date = raw_input("Enter end date of drug prescribed in the form YYYY-MM-DD: ")     
     
		category_ctotal = ("SELECT d.category, SUM(m.amount) FROM drugs d, medications m WHERE d.drug_name = m.drug_name AND date(m.mdate) >= '"+ str(start_date) + "'AND date(m.mdate) < '" + str(end_date) + "'GROUP BY d.category;") 
		c.execute(category_ctotal)
		list_category_ctotal = list(c.fetchall())
     
     
		dname_dtotal = ("SELECT m.drug_name, SUM(m.amount) FROM medications m WHERE date(m.mdate) >= '"+ str(start_date) + "'AND date(m.mdate) < '" + str(end_date) + "'  GROUP BY m.drug_name;")
		c.execute(dname_dtotal)
		list_dname_dtotal = list(c.fetchall())
     
		print("Total amount prescribed in each category: " )
		for i in range(len(list_category_ctotal)):
		    format_category = ('{}: {}').format(list_category_ctotal[i][0], list_category_ctotal[i][1] )
		    print(format_category)
		    print()
     
		print("Total amount prescribed for each drug: ")
		for j in range(len(list_dname_dtotal)):
		    format_drugtotal = ('{}: {}').format(list_dname_dtotal[j][0], list_dname_dtotal[j][1] )
		    print(format_drugtotal)
		    print()
			
	    elif(staff_option == "3"):
		diagnosis = raw_input("\nEnter a diagnosis: ")
		diagnosis = "'" + diagnosis + "'"
		     
		List_of_medications_After_Diagnosis__Query = ('''
		SELECT m.drug_name 
		FROM medications m, diagnoses d 
		WHERE m.chart_id = d.chart_id
		AND m.mdate > d.ddate 
		AND diagnosis = ''' + diagnosis + '''
		GROUP BY m.drug_name
		ORDER BY count(*);
		''')
			 
			 
		c.execute(List_of_medications_After_Diagnosis__Query)
		list_of_medications = c.fetchall()
		
		for medicine in list_of_medications:
		    print(medicine[0])
		    
	    elif(staff_option == "4"):
		drug = raw_input("\nEnter a drug: ")
		drug = "'" + drug + "'"
	
		List_of_Diagnosis_Before_Prescribed_Drug_Query = ('''
		    SELECT d.diagnosis
		    FROM diagnoses d, medications m
		    WHERE d.chart_id = m.chart_id 
		    AND   d.ddate < m.mdate
		    AND drug_name = ''' + drug + '''
		    GROUP BY d.diagnosis
		    ORDER BY AVG(amount);
		''')
		
		c.execute(List_of_Diagnosis_Before_Prescribed_Drug_Query)
		list_of_diagnosis = c.fetchall()
		
		for diagnosis in list_of_diagnosis:
		    print(diagnosis[0])
	    else:
		break
		




#Authenticates username and password and creates a class object based on their designation
def user_checker(username,password):
    query1 = ("SELECT password FROM staff WHERE login = '" +username +"';")
    hash_password = (hashlib.sha224(password).hexdigest())
    query2 = ("SELECT role FROM staff WHERE login = '" +username +"';")
    doc_id = ("SELECT staff_id FROM staff WHERE login = '" +username +"';")
    c.execute(query1)
    pass1 = c.fetchone()
    if pass1 is None:
        print("No username found")
        return    
    pass2 = pass1[0]
    if(pass2!=hash_password):
        print("Wrong password, returning to welcome screen")
        return
    if(pass2 == hash_password):
        role1 = c.execute(query2)
        role2 = role1.fetchone()
        c.execute(doc_id)
        doc_id1 = c.fetchone()
        doc_id2 = doc_id1[0]
        if role2[0] == 'D':
            current = Doctor()
            Doctor.list_of_options(current,doc_id2)
        elif role2[0] == 'N':
            current = Nurse()
            Nurse.nlist_of_options(current,doc_id2)
        elif role2[0] == 'A':
            current = Staff()
            Staff.slist_of_options(current,doc_id2)
	    
#mechanism to add a new user to the system                     
def create(): 
    in_staff_id =raw_input("Enter staff id: ")
    id_exists_or = ("SELECT staff_id FROM staff WHERE staff_id = " + (in_staff_id)+";")
    c.execute(id_exists_or)
    if (c.fetchone() is not None): #insert into existing tuple
        print("User already exists") 
      
    else: #create new tuple
        in_name = raw_input("Enter name: ")
        in_role = raw_input("Enter role: ")
        in_user = raw_input("Enter username: ")
        in_password = raw_input("Enter password: ")
        chash_password = (hashlib.sha224(in_password).hexdigest())
        #final_query = ("INSERT INTO staff VALUES (" + (in_staff_id)+","+(in_role)+","+(in_name)+","+(in_user)+","+(str(chash_password))+ ");")
        c.execute("""INSERT INTO staff VALUES (?,?,?,?,?);""",(in_staff_id,in_name,in_role,in_user,chash_password))
        conn.commit()


db = raw_input("Enter the database filename: ")
conn = sqlite3.connect(db)
conn.text_factory = str
c=conn.cursor()       
       
while(True):
    choice = raw_input( "Welcome to the hospital. Press 1 to access the login screen. Press 2 to create a new user. Press 3 to exit. Press enter to confirm: ")
    if (choice == "1"):
	login = raw_input("Enter username: ")
        password = raw_input("Password: ")
        user_checker(login,password)
    elif (choice == "2"):
        create()
    else:
        break


      
      
