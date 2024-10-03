

Exclude_Encounter = [
    "583.89",
    "582.89",
    "583",
    "V08",
    "42",
    "42.1",
    "42.2",
    "42.8",
    "42.9",
    "70.2",
    "70.21",
    "70.22",
    "70.23",
    "70.3",
    "70.31",
    "70.32",
    "70.33",
    "70.41",
    "70.44",
    "70.51",
    "70.54",
    "70.7",
    "70.71",
    "287",
    "580",
    "580.4",
    "593.73",
    "741.9",
    "741",
    "596.54",
    "277.87",
    "593.73",
    "593.7",
    "N05.1",
    "N06.1",
    "N07.1",
    "N03.8",
    "N05.9",
    "Z21",
    "B20",
    "B16.2",
    "B191.1",
    "B160",
    "B18.1",
    "B180",
    "B16.9",
    "B191.0",
    "B161",
    "B18.1",
    "B18.0",
    "B17.11",
    "B18.2",
    "B17.10",
    "B18.2",
    "B19.20",
    "B192.1",
    "D69.0",
    "N00.3",
    "N01.3",
    "N13.729",
    "Q05.8",
    "Q05.4",
    "N31.9",
    "E884.0",
    "E884.1",
    "E884.2",
    "E884.9",
    "H49819",
    "N13.729",
    "N13.70",
]
Amyloidosis_Encounter = ["277.39", "277.3", "277.3", "E85.1", "E853", "E858"]
Diabetes1_Encounter = ["E102.9", "250.41", "250.43"]
Diabetes2_Encounter = ["250.4", "250.43", "E08.21", "E08.22", "E112.9"]
Lupus_Encounter = ["M32.10", "710", "710"]
Neph5820_Encounter = ["582", "N03.2"]
Neph5829_Encounter = ["N03.9", "582.9"]
Neph5832_Encounter = ["583.2", "N05.5"]
NSNOS_Encounter = ["N04.9", "581.9"]
PrimaryNS_Encounter = [
    "581.1",
    "581.3",
    "582.1",
    "583.1",
    "N02.2",
    "N04.0",
    "N03.3",
    "N05.2",
]

All_encounters = (
    Exclude_Encounter
    + Amyloidosis_Encounter
    + Diabetes1_Encounter
    + Diabetes2_Encounter
    + Lupus_Encounter
    + Neph5820_Encounter
    + Neph5829_Encounter
    + Neph5832_Encounter
    + NSNOS_Encounter
    + PrimaryNS_Encounter
)