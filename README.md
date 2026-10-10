Child Developmental Screening App is a machine-learning-supported application designed to assist parents, caregivers, and relevant professionals with early identification of possible developmental concerns in children. The system uses information related to developmental and functional areas to generate screening impressions and provide guidance on seeking appropriate professional assessment and therapy support.This application is a screening-support tool and is not intended to diagnose medical or developmental conditions.



Furaha Child Development Screening App

Overview

The Furaha Child Development Screening App is a machine-learning-supported application developed to assist with the early screening of possible developmental concerns in children.

The application provides a structured way of collecting information about a child's age, background, developmental abilities, functional activities, and other relevant observations. Based on the information provided, the system generates screening impressions and provides guidance on seeking appropriate professional assessment and therapy support.

The application was developed as part of my data science internship and project work at Furaha Therapy and Care Centre,Meru.

 Important: This application is a screening-support tool. It is not a diagnostic tool and should not be used to diagnose a child or replace assessment by qualified healthcare or therapy professionals.

---

 Project Objective

The main objective of the project is to develop a simple and accessible digital screening-support system that can:
Collect structured information about a child's development and functional abilities.
Support early identification of possible developmental concerns.
Use a trained machine-learning model to generate screening impressions.
Provide parent- and caregiver-friendly guidance.
Suggest appropriate therapy or health assessment pathways.
Provide referral information for therapy centres within the user's county of residence.



Key Features

1. Child Information

The application collects basic information such as:

* Child's date of birth
* Child's age
* County of residence
* Sub-county of residence

The location information is used mainly to provide relevant referral information.

2. Activities of Daily Living (ADLs)

The application collects information about the child's ability to perform selected daily activities.

Responses are represented as:
Not Achieved
Partly Achieved 
Achieved

These responses are converted into numerical values for use by the machine-learning model.

 3. Gross Motor Development

The application includes questions related to gross motor abilities and movement.

 4. Fine Motor Development

The application collects information related to fine motor skills and activities requiring controlled hand and finger movements.

 5. Sensory Development

The application includes structured observations related to sensory and functional development.

 6. Screening Impressions

The trained machine-learning model processes the information entered into the application and provides one or more screening impressions where applicable

Examples of conditions or developmental concerns represented in the underlying data include:

Cerebral Palsy
Autism Spectrum Disorder
Developmental Motor Skills Difficulty
Developmental delays
Delayed speech
ADHD
Hemiplegia
Down Syndrome
Other developmental or functional concerns represented in the dataset

The outputs are presented as screening impressions rather than diagnoses.

7. Problems Identified

Where relevant, the application can display functional or developmental problems identified from the available information.

The system is designed to present these in language that is easier for parents and caregivers to understand.

8. Therapy and Support Guidance

Based on the screening output, the application provides general information about possible professional support pathways.

These may include services such as:

* Occupational Therapy
* Physiotherapy
* Rehabilitative Therapy
* Neurodevelopmental Treatment (NDT)
* Sensory Integration Therapy
* Cognitive Behavioural Therapy (CBT)
* Oral Motor Stimulation

The application does not prescribe medication or provide medical treatment instructions.

9. Referral Information

The application can provide information about therapy centres and services within the user's county of residence.

This information is intended as referral guidance only and does not replace professional assessment.

---

 Machine Learning Component

The application uses a trained machine-learning model to support the screening process.

The model was developed using historical child-related assessment data and structured developmental and functional variables.

The machine-learning workflow involved:

1. Data collection
2. Data cleaning
3. Data preprocessing
4. Feature preparation
5. Encoding categorical variables
6. Preparing developmental and functional variables
7. Model training
8. Model evaluation
9. Saving the trained model
10. Integrating the model into a Streamlit application

The trained model is stored in:

```text
furaha_screening_model.joblib
---

The application loads the trained model and uses it to process information entered by the user.

---

## Data Preprocessing

The project involved preparing a dataset containing child assessment information.

The dataset included structured information from areas such as:

* Activities of Daily Living
* Gross motor development
* Fine motor development
* Sensory observations
* Medical and developmental information
* Screening impressions
* Problems identified
* Intervention information

For ADL-related variables, responses were encoded as:

```text
Not Achieved = 0
Partly Achieved = 1
Achieved = 2
```

Categorical variables were also processed during model preparation.

Missing-value indicators were included where required by the trained preprocessing pipeline.

---

Technologies Used
 
Programming Language

Python

Libraries and Frameworks
Pandas
NumPy
Scikit-learn
Joblib
Streamlit

Development Areas

Data preprocessing
Data analysis
Machine learning
Predictive modeling
Application development
User interface design
Model deployment

---

Application Architecture

The Streamlit interface is organized into small modules so that the entry point stays easy to navigate:

```text
Furaha-Child-Development-Screening/
│
├── app.py
├── furaha_screening_model.joblib
├── screening/
│   ├── app.py
│   ├── forms.py
│   ├── workflow.py
│   ├── model.py
│   ├── results_view.py
│   ├── theme.py
│   ├── contact.py
│   ├── clinical.py
│   ├── concerns.py
│   ├── questions_data.py
│   └── referrals.py
├── requirements.txt
├── runtime.txt
└── README.md
```

File Description

| File                            | Purpose                                                     |
| ------------------------------- | ----------------------------------------------------------- |
| `app.py` | Streamlit entry point and page configuration |
| `screening/app.py` | Composes the five-step interface and coordinates submission |
| `screening/forms.py` | Form fields, age-based questions, and answer definitions |
| `screening/workflow.py` | Validation, feature mapping, and screening-result adjustments |
| `screening/model.py` | Loads the model and runs predictions |
| `screening/results_view.py` | Displays impressions, guidance, and referral information |
| `screening/theme.py` | Responsive layout and Furaha visual styling |
| `screening/contact.py` | Optional follow-up consent and email handling |
| `screening/clinical.py` | Parent-friendly impression names and support information |
| `screening/concerns.py` | Caregiver concern list and concern scoring rules |
| `screening/questions_data.py` | Age thresholds, model question keys, and counties |
| `screening/referrals.py` | Therapy-centre referral information |
| `furaha_screening_model.joblib` | Trained model and preprocessing components |
| `requirements.txt` | Python packages required to run the application |
| `runtime.txt` | Runtime configuration |
| `README.md` | Project documentation |

---

User Workflow

The application follows a structured five-step screening workflow:

```text
Child details and residence → Daily skills → Movement → Senses → Review and screening summary
```

---

Running the Application Locally

1. Clone the repository

```bash
git clone https://github.com/koechtabitha/Furaha-Child-Development-Screening.git
```

 2. Move into the project directory

```bash
cd Furaha-Child-Development-Screening
```

3. Install the required packages

```bash
pip install -r requirements.txt
```

4. Run the Streamlit application

```bash
streamlit run app.py
```

The application will open in your web browser.

---

Deployment

The application was developed using Streamlit and prepared for deployment as a web-based screening-support application.

Live application:

https://furaha-child-development-screening-rzddnavm5xihknldhfs4pz.streamlit.app/

---

Ethical and Safety Considerations

This project involves information related to children and developmental health. Privacy and responsible use of data are therefore important considerations.

The application should not be used to:

Diagnose a child.
Replace professional assessment.
Prescribe medication.
Replace healthcare or therapy services.
Make decisions about a child's care without appropriate professional guidance.

Any real-world deployment should follow applicable data-protection, privacy, consent, and child-safeguarding requirements.

For portfolio purposes, sensitive or personally identifiable information should not be publicly uploaded to this repository.

---

Project Learning Outcomes

Through this project, I gained practical experience in:

Cleaning and preparing real-world datasets.
Working with missing and categorical data.
Preparing features for machine learning.
Building and working with predictive models.
Saving and loading trained machine-learning models.
Integrating a machine-learning model into a Streamlit application.
Designing a user-friendly data collection interface.
Deploying a Python-based application.
* Applying data science to a real-world child development context.
* Communicating technical results in a way that can be understood by non-technical users.

---

Future Improvements

Possible future improvements include:

Expanding the dataset with appropriately collected and anonymized data.
Improving model evaluation using additional performance metrics.
Conducting further validation with qualified professionals.
Improving accessibility for parents and caregivers.
Supporting additional languages.
Expanding referral information.
Improving monitoring and documentation of model performance.
Adding stronger privacy and security controls for any real-world implementation.

---

Project Context

This project was developed during my practical data science work at Furaha Centre, Meru as part of my training and internship experience.

The project combines my background in Biology and Science Education with newly developed skills in:

Data Analysis → Machine Learning → Application Development

---

Author

Tabitha Koech

Science Educator | Data Analyst | Data Science & Machine Learning

GitHub:
https://github.com/koechtabitha

---

Disclaimer

This application is intended for screening support and educational purposes on. It does not provide a medical or developmental diagnosis. Parents, caregivers, and users should seek assessment and guidance from qualified healthcare or therapy professionals when they have concerns about a child's development.

