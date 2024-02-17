#arun code
from flask import Flask, request, jsonify
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from bson import ObjectId
from urllib.parse import quote_plus
import certifi

uri = "mongodb+srv://arvind19rajan:Venu2002@test1.zs9ohef.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri,tlsCAFile=certifi.where())


try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Select your database
db = client["EHR"]

# Select your collection
patient_collection = db["Patient_demographics"]
allergy_collection=db["Allergies"]
insurance_collection=db["Insurance"]
admin_collection=db['Administrative_data'] 
immune_collection=db["Immunisation_details"]
medication_collection=db["Medications"]
diagnosis_collection=db["Diagnosis"]
history_collection=db["Medical_Histories"]
vitals_collection=db["Vitals"]
hospital_collection=db["Hospital"]
doctors_collection=db["Doctors"]
login_collection=db['Login']
sos_collection=db['SOS']
lab_collection=db['Lab_Tests']

app = Flask(__name__)

# GET method to retrieve all patients
@app.route('/patients', methods=['GET'])
def get_patients():
    items = list(patient_collection.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return jsonify({'items': items})

# GET method to retrieve patient details by patient_id
@app.route('/patients/<patient_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    patient = patient_collection.find_one({'Patient_id': patient_id})
    if patient:
        patient['_id'] = str(patient['_id'])
        return jsonify({'patient': patient})
    else:
        return jsonify({'message': 'Patient not found'})

# POST method to add a new patient
@app.route('/patients', methods=['POST'])
def add_item():
    data = request.json
    emergency_contact_info = data.get('Emergency_Contact_info', {})
    emergency_contact_name = emergency_contact_info.get('Name')
    emergency_contact_phone = emergency_contact_info.get('Phone_Number')

    new_item = {
        'patient_id': data['patient_id'],
        'Name': data['Name'],
        'DOB': data['DOB'],
        'Phone_number': data['Phone_number'],
        'Gender': data['Gender'],
        'Ethinicity': data['Ethinicity'],
        'Language': data['Language'],
        'Marital_Status': data['Marital_Status'],
        'Emergency_Contact_info': {
            'Name': emergency_contact_name,
            'Phone_Number': emergency_contact_phone
        }
    }
    result = patient_collection.insert_one(new_item)
    return jsonify({'message': 'Item added successfully', 'id': str(result.inserted_id)})

# PUT method to update an existing patient
@app.route('/patients/<patient_id>', methods=['PUT'])
def update_item(patient_id):
    data = request.json
    emergency_contact_info = data.get('Emergency_Contact_info', {})
    emergency_contact_name = emergency_contact_info.get('Name')
    emergency_contact_phone = emergency_contact_info.get('Phone_Number')

    updated_item = {
        'patient_id': data['patient_id'],
        'Name': data['Name'],
        'DOB': data['DOB'],
        'Phone_number': data['Phone_number'],
        'Gender': data['Gender'],
        'Ethinicity': data['Ethinicity'],
        'Language': data['Language'],
        'Marital_Status': data['Marital_Status'],
        'Emergency_Contact_info': {
            'Name': emergency_contact_name,
            'Phone_Number': emergency_contact_phone
        }
    }
    patient_collection.update_one({'patient_id': patient_id}, {'$set': updated_item})
    return jsonify({'message': 'Item updated successfully'})

# DELETE method to remove a patient
@app.route('/patients/<patient_id>', methods=['DELETE'])
def delete_item(patient_id):
    patient_collection.delete_one({'Patient_id': patient_id})
    return jsonify({'message': 'Item deleted successfully'})

#GET method to retrieve allergy of a patient using patient_id
@app.route('/allergies/<patient_id>',methods=['GET'])
def get_allergies(patient_id):
    allergies = list(allergy_collection.find({'Patient_id': patient_id}))
    for allergy in allergies:
        allergy['_id'] = str(allergy['_id'])
    return jsonify({'allergies': allergies})

#Add an allergy entry
@app.route('/allergies',methods=['POST'])
def add_allergy():
    data = request.json
    new_item ={
        'patient_id':data['patient_id'],
        'allergen':data['allergen'],
        'Reaction':data['Reaction'],
        'Severity':data['Severity'],
        'Date_of_diagnosis':data['Date_of_diagnosis']
        }
    result = allergy_collection.insert_one(new_item)
    return jsonify({'message': 'Item added successfully', 'id': str(result.inserted_id)})

#GET method to retrieve Insurance details of a patient using patient_id
@app.route('/insurance/<patient_id>',methods=['GET'])
def get_insurance(patient_id):
    insurance = insurance_collection.find({'Patient_id': patient_id})
    for i in insurance:
        i['_id'] = str(i['_id'])
    return jsonify({'insurance': insurance})

#GET method to retrieve administrative data of a patient using patient_id
@app.route('/admin/<patient_id>',methods=['GET'])
def get_admin(patient_id):
    admin = list(admin_collection.find({'Patient_id':patient_id}))
    for ad in admin:
        ad['_id'] = str(ad['_id'])
    return jsonify({'admin': admin})

#Add an administrative data entry
@app.route('/admin',methods=['POST'])
def add_admin():
    data = request.json
    new_item ={
        'patient_id':data['patient_id'],
        'Date':data['Date'],
        'Reason':data['Reason'],
        'Type':data['Type'],
        'Amount_paid':data['Amount_paid']
        }
    result = admin_collection.insert_one(new_item)
    return jsonify({'message': 'Item added successfully', 'id': str(result.inserted_id)})

#GET method to retrieve immunization data of a patient using patient_id
@app.route('/immune/<patient_id>',methods=['GET'])
def get_immune(patient_id):
    immune = list(immune_collection.find({'Patient_id': patient_id}))
    for im in immune:
        im['_id'] = str(im['_id'])
    return jsonify({'immune': immune})

#Add an immunization data entry
@app.route('/immune',methods=['POST'])
def add_immune():
    data = request.json
    new_item ={
        'patient_id':data['patient_id'],
        'Vaccine_name':data['Vaccine_name'],
        'Administration_date':data['Administration_date'],
        }
    result = immune_collection.insert_one(new_item)
    return jsonify({'message': 'Item added successfully', 'id': str(result.inserted_id)})

#GET method to retrieve Medication data of a patient using patient_id
@app.route('/medic/<patient_id>',methods=['GET'])
def get_medic(patient_id):
    medic = list(medication_collection.find({'Patient_id': patient_id}))
    for m in medic:
        m['_id'] = str(m['_id'])
    return jsonify({'medic': medic})

#Add a Medication data entry
@app.route('/medic',methods=['POST'])
def add_medic():
    data = request.json
    new_item ={
        'patient_id':data['patient_id'],
        'M_Name':data['M_Name'],
        'Dosage':data['Dosage'],
        'Route':data['Route'],
        'M_Reason':data['M_Reason']
        }
    result = medication_collection.insert_one(new_item)
    return jsonify({'message': 'Item added successfully', 'id': str(result.inserted_id)})


#GET method to retrieve Diagnosis data of a patient using patient_id
@app.route('/diagnosis/<patient_id>',methods=['GET'])
def get_diagnosis(patient_id):
    diagnosis = list(diagnosis_collection.find({'Patient_id': patient_id}))
    for d in diagnosis:
        d['_id'] = str(d['_id'])
    return jsonify({'diagnosis': diagnosis})

#Add a Diagnosis data entry
@app.route('/diagnosis',methods=['POST'])
def add_diagnosis():
    data = request.json
    new_item ={
        'patient_id':data['patient_id'],
        'Date_of_Diagnosis':data['Date_of_Diagnosis'],
        'Primary_Diagnosis':data['Primary_Diagnosis'],
        }
    result = diagnosis_collection.insert_one(new_item)
    return jsonify({'message': 'Item added successfully', 'id': str(result.inserted_id)})

#GET method to retrieve Vital Signs data of a patient using patient_id
@app.route('/Vitals/<patient_id>',methods=['GET'])
def get_vitals(patient_id):
    vitals = vitals_collection.find({'Patient_id': patient_id})
    if vitals:
        vitals['_id'] = str(vitals['_id'])
        return jsonify({'vitals': vitals})
    else:
        return jsonify({'message': 'Patient not found'})

#Add a Vital Signs data entry
@app.route('/vitals',methods=['POST'])
def add_vitals():
    data = request.json
    new_item ={
        "Patient_id":data['Patient_id'],
        "Temperature":data['Temperature'],
        "Heart_Rate":data['Heart_Rate'],
        "Respiration_Rate":data['Respiration_Rate'],
        "Blood_Pressure":data['Blood_Pressure'],
        "SPO2":data['SPO2'],
        "Blood_Glucose":data['Blood_Glucose']
        }
    result = vitals_collection.insert_one(new_item)
    return jsonify({'message': 'Item added successfully', 'id': str(result.inserted_id)})

# GET method to retrieve all hospitals
@app.route('/hospitals', methods=['GET'])
def get_hospitals():
    hospitals = list(hospital_collection.find())
    for hospital in hospitals:
        hospital['_id'] = str(hospital['_id'])
    return jsonify({'hospitals': hospitals})

#Add a Hospital data entry
@app.route('/hospitals',methods=['POST'])
def add_hospitals():
    data = request.json
    new_item ={
        "Hospital_id":data['Hospital_id'],
        "Hospital_name":data['Hospital_name'],
        }
    result = hospital_collection.insert_one(new_item)
    return jsonify({'message': 'Item added successfully', 'id': str(result.inserted_id)})

#GET method to retrieve data of a doctor using Doctor_id
@app.route('/doctors/<Doctor_id>',methods=['GET'])
def get_doctor(Doctor_id):
    Doctors = doctors_collection.find({'Doctor_id': Doctor_id})
    if Doctors:
        Doctors['_id'] = str(Doctors['_id'])
        return jsonify({'Doctors': Doctors})
    else:
        return jsonify({'message': 'Patient not found'})

#Add a Doctors data entry
@app.route('/doctors',methods=['POST'])
def add_doctor():
    data = request.json
    new_item ={
        "Doctor_id":data['Doctor_id'],
        "Hospital_id":data['Hospital_id'],
        "Doctor_Name":data['Doctor_Name'],
        "Specialization":data['Specialization'],
        }
    result = doctors_collection.insert_one(new_item)
    return jsonify({'message': 'Item added successfully', 'id': str(result.inserted_id)})

#GET method to retrieve medical history of a patient using Patient_id
@app.route('/history/<Doctor_id>',methods=['GET'])
def get_history(Doctor_id):
    history = list(history_collection.find({'Doctor_id': Doctor_id}))
    for h in history:
        h['_id'] = str(h['_id'])
    return jsonify({'history': history})


#Add a medical history data entry
@app.route('/history',methods=['POST'])
def add_history():
    data = request.json
    new_item ={
        "Patient_id":data['Patient_id'],
        "Hospital_id":data['Hospital_id'],
        "Doctor_Name":data['Doctor_Name'],
        "Specialization":data['Specialization'],
        }
    result = history_collection.insert_one(new_item)
    return jsonify({'message': 'Item added successfully', 'id': str(result.inserted_id)})

###################################################
#Code not sent to Gautham
###################################################

#Login code
@app.route('/login_verify', methods=['POST'])
def login_verify():
        data = request.json  # Assuming you're sending JSON data from React Native
        u_name = data['Email']  # Assuming the key for email is 'email'
        u_pass = data['Password']  # Assuming the key for password is 'password'

        query = {
            "Email": u_name,
            "Password": u_pass
        }
        result = login_collection.find_one(query)
        
        if result:
            result['_id'] = str(result['_id'])
            return jsonify({'result': 'True'})
        else:
            return jsonify({'result': 'False'})

#API to retrieve all possible data for a ignle patient

@app.route('/patient_all/<patient_id>',methods=['GET'])
def get_all_data(patient_id):
    patient = list(patient_collection.find({'Patient_id': patient_id}))

    allergies = list(allergy_collection.find({'Patient_id': patient_id}))

    insurance = list(insurance_collection.find({'Patient_id': patient_id}))

    admin = list(admin_collection.find({'Patient_id': patient_id}))

    immune = list(immune_collection.find({'Patient_id': patient_id}))

    medic = list(medication_collection.find({'Patient_id': patient_id}))

    diagnosis = list(diagnosis_collection.find({'Patient_id': patient_id}))

    vitals = list(vitals_collection.find({'Patient_id': patient_id}))

    history = list(history_collection.find({'Patient_id': patient_id}))

    combined_list=[]
    combined_dict={}
    keys=['patient_demographics','allergies','insurance_details','administrative_data','immunization_history','medication_history','diagnosis_history','vitals','medical_history']

    lists_to_combine=[patient,allergies,insurance,admin,immune,medic,diagnosis,vitals,history]
    
    for i in lists_to_combine:
        combined_list.extend(i)

    for item in combined_list:
        if isinstance(item, dict) and '_id' in item:
            item['_id'] = str(item['_id'])

    for key,result_list in zip(keys,lists_to_combine):
        combined_dict[key] = result_list

    for item in combined_dict:
        if isinstance(item, dict) and '_id' in item:
            item['_id'] = str(item['_id'])

    return jsonify({'result':combined_dict})


@app.route('/sos',methods=['GET'])
def sos():
    SOS = list(sos_collection.find())
    for s in SOS:
        s['_id'] = str(s['_id'])
    return jsonify({'SOS': SOS})

@app.route('/lab',methods=['GET'])
def lab():
    Lab = list(lab_collection.find())
    for l in Lab:
        l['_id'] = str(l['_id'])
    return jsonify({'Lab': Lab})



if __name__ == '__main__':
    app.run(debug=True)