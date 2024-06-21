from pydantic import BaseModel
from typing import List

class Diagnosis(BaseModel):
    diagnosisId: str 
    dx: str
    #edxType: str
    #dxSource: str


class AdditionalInfo(BaseModel):

    
    NEPH5829_Total: int=0
    NEPH5832_Total: int=0
    NEPH5820_Total: int=0
    Amyloidosis_Total: int=0
    Diabetes2_Total: int=0
    Diabetes1_Total: int=0
    Lupus_Total: int=0
    PrimaryNS_Total: int=0
    NSNOS_Total: int=0
    Exclude_Code_Total: int=0


class Encounter(BaseModel):
    encounterId: str 
    admitDate: str
    #encType: str
    #rawEncType: str
    dischargeDate:str
    diagnosisList:List[Diagnosis]
    additionalInfo:AdditionalInfo

class Patient(BaseModel):
    patId: str
    age: int
    encounterList:List[Encounter]
    
class Result:
    patId: str
    Cohort_Entry_Date: str
    Anchor_EncounterID: str
    Anchor_Admit_Date: str
    Anchor_Discharge_Date: str
    age: int
    
    def to_dict(self):
        return {
            'patId': self.patId,
            'age': self.age,
            'Anchor_Admit_Date': self.Anchor_Admit_Date,
            "Anchor_Discharge_Date": self.Anchor_Discharge_Date,
            "Anchor_EncounterID": self.Anchor_EncounterID
            
        }




