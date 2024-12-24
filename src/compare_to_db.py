from pymongo import MongoClient
import json
import config

def searchSimilar(patient_collection,current_case):

    try:
        query = {
            "פירוט המקרה.קוד אירוע": current_case["פירוט המקרה"]["קוד אירוע"]
        }

        # Search for similar cases
        similar_cases = patient_collection.find(query)

        cases_list = []
        for case in similar_cases:
            case['_id'] = str(case['_id'])  # Convert ObjectId to string
            cases_list.append(case)
        similar_cases=cases_list   

        #find treatments and sort by frequency
        treatment_recommendations = {}
        medication_reccomendations ={}
        for case in similar_cases:
            treatments = case.get("טיפולים", [])
            for treatment in treatments:
                for treatment_name in treatment.get("טיפול שניתן", []):
                    treatment_recommendations[treatment_name] = treatment_recommendations.get(treatment_name, 0) + 1
        ranked_treatments = sorted(treatment_recommendations.items(), key=lambda x: x[1], reverse=True)
        ranked_treatments_list=[x[0] for x in ranked_treatments]

        for case in similar_cases:
            medications=case.get("טיפול תרופתי", [])
            for medication in medications:
                for medication_name in medication.get("תרופה"):
                    medication_reccomendations[medication_name]=medication_reccomendations.get(medication_name, 0) +1
        ranked_medication=sorted(medication_reccomendations.items(), key=lambda x: x[1], reverse=True)
        ranked_medication_list=[x[0] for x in ranked_medication]

        test_reccomendations={}
        for case in similar_cases:
            tests = case.get("מדדים")
            for test in tests:
                for (key, val) in test.items():
                    if key=="זמן בדיקה":
                        continue
                    if val!="null":
                        test_reccomendations[key] = test_reccomendations.get(key, 0) +1
        ranked_tests=sorted(test_reccomendations.items(), key=lambda x: x[1], reverse=True)      
        ranked_tests_list=[x[0] for x in ranked_tests]  
        return( {"suggested tests": ranked_tests_list, "suggested treatments": ranked_treatments_list, "suggested medication": ranked_medication_list})
    except Exception as e:
        return f"error {str(e)}"

def missingTreatmentsByProtocol(medical_case):
    # with open("protocol.json", "r", encoding="utf-8") as file:
    #     protocols = json.load(file)
    protocols = json.loads(config.protocol)

    diagnosis_code = medical_case.get("פירוט המקרה").get("קוד אירוע")
    
    if diagnosis_code not in protocols:
        raise ValueError(f"Diagnosis code {diagnosis_code} not found in protocols.")
    
    protocol = protocols[diagnosis_code]
    
    # Extract protocol recommendations
    required_tests = set(protocol.get("בדיקות", []))
    required_treatments = set(protocol.get("טיפולים", []))
    required_medications = set(protocol.get("תרופות", []))
    
    given_tests = [list(item.keys()) for item in medical_case.get("מדדים", [])]
    given_tests=set([item for sublist in given_tests for item in sublist]) #flatten list
    print(given_tests)
    given_treatments = [item["טיפול שניתן"] for item in medical_case.get("טיפולים", [])]
    given_treatments=set([item for sublist in given_treatments for item in sublist]) #flatten list
    given_medications = [item["טיפול תרופתי"] for item in medical_case.get("תרופה", [])]
    given_medications=set([item for sublist in given_medications for item in sublist]) #flatten list
    
    # Determine missing items
    missing_tests = list(required_tests - given_tests)
    missing_treatments = list(required_treatments - given_treatments)
    missing_medications = list(required_medications - given_medications)
    
    return( {
        "suggested tests": missing_tests,
        "suggested treatments": missing_treatments,
        "suggested medication": missing_medications
    })


def findSuggestions(patient_collection,medical_case):
    suggestion1=searchSimilar(patient_collection,medical_case)
    suggestion2=missingTreatmentsByProtocol(medical_case)
    suggestions={}
    for key in suggestion1:
        if key in suggestion2:
            suggestions[key]=suggestion1[key]+suggestion2[key]
        else:
            suggestions[key]=suggestion1[key]
    for key in suggestion2:
        if key in suggestion1:
            suggestions[key]=suggestion1[key]+suggestion2[key]
        else:
            suggestions[key]=suggestion2[key]
    return(suggestions)


if __name__ == "__main__":
    findSuggestions()