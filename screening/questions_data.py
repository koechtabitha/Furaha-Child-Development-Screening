MODEL_MIN_AGE_MONTHS = 12

AGE_RULES = {

    # Activities of Daily Living
    "Feeding": 6,
    "Toileting": 24,
    "Dressing": 24,
    "Grooming": 24,

    # Gross motor
    "Head control": 0,
    "Rolling over": 3,
    "Trunk stability": 4,
    "Sitting": 4,
    "Crawling": 6,
    "Standing": 6,
    "Walking": 9,

    # Fine motor
    "Eye tracking": 0,
    "Eye-hand coordination": 3,
    "Bilateral hand use": 4,
    "Grasp": 3,
    "Manipulation": 6,
    "Release": 9,

    # Sensory
    "Auditory response": 0,
    "Visual response": 0,
    "Tactile response": 0,
    "Vestibular response": 3,
    "Proprioception": 6
}


QUESTION_MODEL_KEYS = {

    "Feeding": [
        "ML_ADL_FeedingEating"
    ],

    "Toileting": [
        "ML_ADL_Toileting"
    ],

    "Dressing": [
        "ML_ADL_GroomingDressingSkills"
    ],

    "Grooming": [
        "ML_ADL_Grooming"
    ],

    "Head control": [
        "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_HeadControl"
    ],

    "Rolling over": [
        "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_RollingOver"
    ],

    "Trunk stability": [
        "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_TrunkStablity"
    ],

    "Sitting": [
        "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Sitting"
    ],

    "Crawling": [
        "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Crawling"
    ],

    "Standing": [
        "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Standing"
    ],

    "Walking": [
        "OccupationalPerformanceAreas_DevelopmentalComponents_GrossMotor_Walking"
    ],

    "Eye tracking": [
        "OccupationalPerformanceAreas_FineMotor_EyeTracking"
    ],

    "Eye-hand coordination": [
        "OccupationalPerformanceAreas_FineMotor_EyeHandCordination"
    ],

    "Bilateral hand use": [
        "OccupationalPerformanceAreas_FineMotor_BilateralHandUse"
    ],

    "Grasp": [
        "OccupationalPerformanceAreas_FineMotor_Grasp"
    ],

    "Manipulation": [
        "OccupationalPerformanceAreas_FineMotor_Manipulation"
    ],

    "Release": [
        "OccupationalPerformanceAreas_FineMotor_Release"
    ],

    "Auditory response": [
        "OccupationalPerformanceAreas_FineMotor_Sensory_Auditory"
    ],

    "Visual response": [
        "OccupationalPerformanceAreas_FineMotor_Sensory_Visual"
    ],

    "Tactile response": [
        "OccupationalPerformanceAreas_FineMotor_Sensory_Tactile"
    ],

    "Vestibular response": [
        "OccupationalPerformanceAreas_FineMotor_Sensory_Vestibular"
    ],

    "Proprioception": [
        "OccupationalPerformanceAreas_FineMotor_Sensory_Proprioception",
        "Sensory_Proprioception",
        "Proprioception"
    ]
}
counties = [

    "Select County",

    "Baringo",
    "Bomet",
    "Bungoma",
    "Busia",
    "Elgeyo-Marakwet",
    "Embu",
    "Garissa",
    "Homa Bay",
    "Isiolo",
    "Kajiado",
    "Kakamega",
    "Kericho",
    "Kiambu",
    "Kilifi",
    "Kirinyaga",
    "Kisii",
    "Kisumu",
    "Kitui",
    "Kwale",
    "Laikipia",
    "Lamu",
    "Machakos",
    "Makueni",
    "Mandera",
    "Marsabit",
    "Meru",
    "Migori",
    "Mombasa",
    "Murang'a",
    "Nairobi",
    "Nakuru",
    "Nandi",
    "Narok",
    "Nyamira",
    "Nyandarua",
    "Nyeri",
    "Samburu",
    "Siaya",
    "Taita Taveta",
    "Tana River",
    "Tharaka-Nithi",
    "Trans Nzoia",
    "Turkana",
    "Uasin Gishu",
    "Vihiga",
    "Wajir",
    "West Pokot"
]
