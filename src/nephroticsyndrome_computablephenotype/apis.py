import csv
from datetime import datetime
from io import StringIO
import json
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import RedirectResponse
from .datatypes import Patient, Encounter, Diagnosis, AdditionalInfo,Result
from typing import List

app = FastAPI()

@app.get(
    "/",
    include_in_schema=False,
)
async def root(request: Request):
    response = RedirectResponse(url="/docs")
    return response

   
Exclude_Encounter=['583.89','582.89','583','V08','42','42.1','42.2','42.8','42.9','70.2','70.21','70.22','70.23','70.3','70.31','70.32','70.33','70.41','70.44','70.51','70.54',
                   '70.7','70.71','287','580','580.4','593.73','741.9','741','596.54','277.87','593.73','593.7','N05.1','N06.1','N07.1','N03.8','N05.9','Z21','B20','B16.2',
                   'B191.1','B160','B18.1','B180','B16.9','B191.0','B161','B18.1','B18.0','B17.11','B18.2','B17.10','B18.2','B19.20','B192.1','D69.0','N00.3','N01.3','N13.729',
                   'Q05.8','Q05.4','N31.9','E884.0','E884.1','E884.2','E884.9','H49819','N13.729','N13.70']
Amyloidosis_Encounter=['277.39','277.3','277.3','E85.1','E853','E858']
Diabetes1_Encounter=['E102.9','250.41','250.43']
Diabetes2_Encounter=['250.4','250.43','E08.21','E08.22','E112.9']
Lupus_Encounter=['M32.10','710','710']
Neph5820_Encounter=['582','N03.2']
Neph5829_Encounter=['N03.9','582.9']
Neph5832_Encounter=['583.2','N05.5']
NSNOS_Encounter=['N04.9','581.9']
PrimaryNS_Encounter=['581.1','581.3','582.1','583.1','N02.2','N04.0','N03.3','N05.2']
All_encounters = Exclude_Encounter + Amyloidosis_Encounter + Diabetes1_Encounter + Diabetes2_Encounter + Lupus_Encounter + Neph5820_Encounter + Neph5829_Encounter + Neph5832_Encounter + NSNOS_Encounter + PrimaryNS_Encounter

@app.post("/classification")
async def upload_file(file: UploadFile):
    """
    
    **Classify patients and return inclusion encounters:**

    This endpoint receives patient data in either JSON or CSV format, applies computable phenotype,
    and returns a list of inclusion encounters.

    **Parameters:**
    :param file: Patient data in JSON or CSV format.
    
    **Sample input data:**
    Sample input data (CSV and JSON) can be found in the GitHub repository under the 'input_test_data' folder:
    [Link to GitHub Repository](https://github.com/kgrid-lab/nephroticsyndrome-computablephenotype/tree/main/input_test_data)

    **Implementation:** 
    The implementation of this app is available on GitHub:
    [Link to GitHub Repository](https://github.com/kgrid-lab/nephroticsyndrome-computablephenotype)

    **Returns:**
    List of inclusion encounters that meet the criteria.
    """
    content = await file.read()
    
    if is_csv(content):
        patientList=prepare_data_from_csv(content)
        return process_patient_list(patientList)
    elif is_json(content):
        data = json.loads(content)        
        patientList = [Patient(**item) for item in data]        
        return process_patient_list(patientList)
    else:
        return "Input data must be json or csv"
        

def is_json(content):
    try:
        json.loads(content)
        return True
    except json.JSONDecodeError:
        return False

def is_csv(content):
    try:
        # Convert the content to a file-like object (StringIO)
        csv_text = content.decode('utf-8')
    
    # Process the CSV data and append rows to the JSON variable
        csv_reader = csv.reader(csv_text.splitlines())
        header = next(csv_reader)
        # Assuming it's CSV if it has at least two columns in the first row
        if len(header) >= 2:
            return True
    except (csv.Error, StopIteration):
        pass
    return False
     
def prepare_data_from_csv(csv_content)-> list[Patient]:
    data =  []
    patientList=[]
    numInput=0
    numDiagnosis=0

    # Convert the CSV content to a text string
    csv_text = csv_content.decode('utf-8')
    
    # Process the CSV data and append rows to the JSON variable
    for row in csv.reader(csv_text.splitlines()):
        numInput+=1
        if row[4] in All_encounters:    
            numDiagnosis+=1
            data.append(row)

    print("num input: ",numInput)
    print("num diagnosis: ",numDiagnosis)
    
    # Sort the data list based on the "id" key
    data = sorted(data, key=lambda x: x[0])
    
    #format data as [patients{[encounters{[duagnosis]}]}]
    for row in data: 
        patient:Patient
        encounter:Encounter
        
        #if patient does not exist add it otherwise find it
        if len([obj for obj in patientList if obj.patId == row[0]])==0:
            patient= Patient(patId=row[0],age=row[1],encounterList=[])            
            patientList.append(patient)              
        else:            
            patient = [obj for obj in patientList if obj.patId == row[0]][0]
        
        #if encounter does not exist in patient add it otherwise find it    
        if len([obj for obj in patient.encounterList if obj.encounterId == row[2]])==0:
            encounter= Encounter(encounterId=row[2],admitDate=row[3],dischargeDate=row[3],diagnosisList=[], additionalInfo=AdditionalInfo())            
            patient.encounterList.append(encounter)
        else:
            encounter = [obj for obj in patient.encounterList if obj.encounterId == row[2]][0]

        #add diagnosis to the right patient and encounter
        diagnosis= Diagnosis(diagnosisId="",dx=row[4])            
        encounter.diagnosisList.append(diagnosis)
            
    return patientList

def process_patient_list(patientList) -> {}:
    final_result=[]
    for patient in patientList: #for each patient in the list
        
        #sort patient encounters in place (date format must be like 3/27/2005)
        patient.encounterList.sort(key=lambda x: datetime.strptime(x.dischargeDate, '%m/%d/%Y')) 
        
        #for each encounter calculate the running total for the target diagnosis codes in chronological order
        previousEncounterAdditionalInfoRunningTotal=AdditionalInfo()        
        for encounter in patient.encounterList:
            encounter.additionalInfo=previousEncounterAdditionalInfoRunningTotal.copy()
            for diagnosis in encounter.diagnosisList:
                if(diagnosis.dx in Exclude_Encounter): 
                    encounter.additionalInfo.Exclude_Code_Total += 1
                    
                if(diagnosis.dx in Amyloidosis_Encounter): 
                    encounter.additionalInfo.Amyloidosis_Total += 1
                    
                if(diagnosis.dx in Diabetes1_Encounter): 
                    encounter.additionalInfo.Diabetes1_Total += 1
                    
                if(diagnosis.dx in Diabetes2_Encounter): 
                    encounter.additionalInfo.Diabetes2_Total += 1
                                        
                if(diagnosis.dx in Lupus_Encounter): 
                    encounter.additionalInfo.Lupus_Total += 1
                                        
                if(diagnosis.dx in Neph5820_Encounter): 
                    encounter.additionalInfo.NEPH5820_Total += 1
                                        
                if(diagnosis.dx in Neph5829_Encounter): 
                    encounter.additionalInfo.NEPH5829_Total += 1
                                        
                if(diagnosis.dx in Neph5832_Encounter): 
                    encounter.additionalInfo.NEPH5832_Total += 1
                    
                    
                if(diagnosis.dx in NSNOS_Encounter): 
                    encounter.additionalInfo.NSNOS_Total += 1
                    
                if(diagnosis.dx in PrimaryNS_Encounter): 
                    encounter.additionalInfo.PrimaryNS_Total += 1
            
            
            #check the running total for current encounter and if it is an inclusion but not an inclusion stop processing next encounters of this patient and append that encounter to final inclusions        
            previousEncounterAdditionalInfoRunningTotal=encounter.additionalInfo.copy()
            if  encounter.additionalInfo.PrimaryNS_Total>1 or (encounter.additionalInfo.PrimaryNS_Total+encounter.additionalInfo.NSNOS_Total>1 and patient.age<20) and not (encounter.additionalInfo.NEPH5829_Total>1 or encounter.additionalInfo.NEPH5832_Total>1 or encounter.additionalInfo.NEPH5820_Total>1 or encounter.additionalInfo.Amyloidosis_Total>1 or encounter.additionalInfo.Diabetes1_Total>1 or encounter.additionalInfo.Diabetes2_Total>1 or encounter.additionalInfo.Lupus_Total>1 or encounter.additionalInfo.Exclude_Code_Total>0):
                result=Result()
                result.patId=patient.patId
                result.age=patient.age
                result.Anchor_Admit_Date=encounter.admitDate
                result.Anchor_Discharge_Date=encounter.dischargeDate
                result.Anchor_EncounterID=encounter.encounterId
            
                final_result.append(result)
                break
          
    return {"num of inclusion patients":len(final_result),"inclusion patients":final_result}

#only runs virtual server when running this .py file directly for debugging
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)