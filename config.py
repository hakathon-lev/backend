
hebrew_keywords = [
    "מס משימה",
    "מס ניידת",
    "תאריך",
    "סוג תעודה",
    "גיל",
    "שם האב",
    "מייל",
    "מין",
    "תאריך לידה",
    "קופת חולים",
    "כתובת",
    "שם מלא",
    "טלפון",
    "ישוב",
    "מקום האירוע",
    "עיר",
    "המקרה שנמצא",
    "תלונה עיקרית",
    "סטטוס המטופל",
    "רקע רפואי",
    "רגישויות",
    "תרופות קבועות"
]

CHATGPT_REQUIREMENTS = f"""
You are a text processor.I will provide you with a Hebrew text and a list of hebrew keywords.
Your task is to extract the values corresponding to these keywords and return a valid JSON object.
hebrew keywords:
{hebrew_keywords}                                                                     
"""