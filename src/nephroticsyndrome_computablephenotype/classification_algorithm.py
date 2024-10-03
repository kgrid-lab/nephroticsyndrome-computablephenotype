from nephroticsyndrome_computablephenotype.icd_codes import Amyloidosis_Encounter, Diabetes1_Encounter, Diabetes2_Encounter, Exclude_Encounter, Lupus_Encounter, NSNOS_Encounter, Neph5820_Encounter, Neph5829_Encounter, Neph5832_Encounter, PrimaryNS_Encounter
from datetime import datetime

from nephroticsyndrome_computablephenotype.datatypes import AdditionalInfo, Result

def process_patient_list(patientList) -> {}:
    final_result = []
    for patient in patientList:  # for each patient in the list
        # sort patient encounters in place (date format must be like 3/27/2005)
        patient.encounterList.sort(
            key=lambda x: datetime.strptime(x.dischargeDate, "%m/%d/%Y")
        )

        # for each encounter calculate the running total for the target diagnosis codes in chronological order
        previousEncounterAdditionalInfoRunningTotal = AdditionalInfo()
        for encounter in patient.encounterList:
            encounter.additionalInfo = (
                previousEncounterAdditionalInfoRunningTotal.copy()
            )
            for diagnosis in encounter.diagnosisList:
                if diagnosis.dx in Exclude_Encounter:
                    encounter.additionalInfo.Exclude_Code_Total += 1

                if diagnosis.dx in Amyloidosis_Encounter:
                    encounter.additionalInfo.Amyloidosis_Total += 1

                if diagnosis.dx in Diabetes1_Encounter:
                    encounter.additionalInfo.Diabetes1_Total += 1

                if diagnosis.dx in Diabetes2_Encounter:
                    encounter.additionalInfo.Diabetes2_Total += 1

                if diagnosis.dx in Lupus_Encounter:
                    encounter.additionalInfo.Lupus_Total += 1

                if diagnosis.dx in Neph5820_Encounter:
                    encounter.additionalInfo.NEPH5820_Total += 1

                if diagnosis.dx in Neph5829_Encounter:
                    encounter.additionalInfo.NEPH5829_Total += 1

                if diagnosis.dx in Neph5832_Encounter:
                    encounter.additionalInfo.NEPH5832_Total += 1

                if diagnosis.dx in NSNOS_Encounter:
                    encounter.additionalInfo.NSNOS_Total += 1

                if diagnosis.dx in PrimaryNS_Encounter:
                    encounter.additionalInfo.PrimaryNS_Total += 1

            # check the running total for current encounter and if it is an inclusion but not an inclusion stop processing next encounters of this patient and append that encounter to final inclusions
            previousEncounterAdditionalInfoRunningTotal = (
                encounter.additionalInfo.copy()
            )
            if (
                encounter.additionalInfo.PrimaryNS_Total > 1
                or (
                    encounter.additionalInfo.PrimaryNS_Total
                    + encounter.additionalInfo.NSNOS_Total
                    > 1
                    and patient.age < 20
                )
                and not (
                    encounter.additionalInfo.NEPH5829_Total > 1
                    or encounter.additionalInfo.NEPH5832_Total > 1
                    or encounter.additionalInfo.NEPH5820_Total > 1
                    or encounter.additionalInfo.Amyloidosis_Total > 1
                    or encounter.additionalInfo.Diabetes1_Total > 1
                    or encounter.additionalInfo.Diabetes2_Total > 1
                    or encounter.additionalInfo.Lupus_Total > 1
                    or encounter.additionalInfo.Exclude_Code_Total > 0
                )
            ):
                result = Result()
                result.patId = patient.patId
                result.age = patient.age
                result.Anchor_Admit_Date = encounter.admitDate
                result.Anchor_Discharge_Date = encounter.dischargeDate
                result.Anchor_EncounterID = encounter.encounterId

                final_result.append(result.to_dict())
                break
    return {
        "num of inclusion patients": len(final_result),
        "inclusion patients": final_result,
    }
