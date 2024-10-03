import csv
import json

from nephroticsyndrome_computablephenotype.icd_codes import All_encounters

from nephroticsyndrome_computablephenotype.datatypes import AdditionalInfo, Diagnosis, Encounter, Patient

def is_json(content):
    try:
        json.loads(content)
        return True
    except json.JSONDecodeError:
        return False


def is_csv(content):
    try:
        # Convert the content to a file-like object (StringIO)
        csv_text = content.decode("utf-8")

        # Process the CSV data and append rows to the JSON variable
        csv_reader = csv.reader(csv_text.splitlines())
        header = next(csv_reader)
        # Assuming it's CSV if it has at least two columns in the first row
        if len(header) >= 2:
            return True
    except (csv.Error, StopIteration):
        pass
    return False


def prepare_data_from_csv(csv_content) -> list[Patient]:
    data = []
    patientList = []
    numInput = 0
    numDiagnosis = 0

    # Convert the CSV content to a text string
    csv_text = csv_content.decode("utf-8")

    # Process the CSV data and append rows to the JSON variable
    for row in csv.reader(csv_text.splitlines()):
        numInput += 1
        if row[4] in All_encounters:
            numDiagnosis += 1
            data.append(row)

    print("num input: ", numInput)
    print("num diagnosis: ", numDiagnosis)

    # Sort the data list based on the "id" key
    data = sorted(data, key=lambda x: x[0])

    # format data as [patients{[encounters{[duagnosis]}]}]
    for row in data:
        patient: Patient
        encounter: Encounter

        # if patient does not exist add it otherwise find it
        if len([obj for obj in patientList if obj.patId == row[0]]) == 0:
            patient = Patient(patId=row[0], age=row[1], encounterList=[])
            patientList.append(patient)
        else:
            patient = [obj for obj in patientList if obj.patId == row[0]][0]

        # if encounter does not exist in patient add it otherwise find it
        if (
            len([obj for obj in patient.encounterList if obj.encounterId == row[2]])
            == 0
        ):
            encounter = Encounter(
                encounterId=row[2],
                admitDate=row[3],
                dischargeDate=row[3],
                diagnosisList=[],
                additionalInfo=AdditionalInfo(),
            )
            patient.encounterList.append(encounter)
        else:
            encounter = [
                obj for obj in patient.encounterList if obj.encounterId == row[2]
            ][0]

        # add diagnosis to the right patient and encounter
        diagnosis = Diagnosis(diagnosisId="", dx=row[4])
        encounter.diagnosisList.append(diagnosis)

    return patientList