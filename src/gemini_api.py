import os
import google.generativeai as genai
import config
from dotenv import find_dotenv, load_dotenv
import json

env = find_dotenv()
load_dotenv(dotenv_path=env)


def get_gimini_response(text):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    response = chat_session.send_message(config.GEMINI_REQUIREMENTS + text)

    return response.text


def main():
    response = get_gimini_response("שלום לך איך קוראים לך יוסי כהן טוב יוסי תעודת הזהות שלך בבקשה 123456789 תודה מה קרה כאן יוסי רכב פגע בך כשחצית את הכביש הבנתי בן כמה אתה 39 זאת אומרת נולדת ב1 בינואר 1985 תודה אתה מבוטח בקופת חולים כללית נכון אוקיי תגיד לי איפה כואב לך עכשיו ברגל ימין ובחזה אני רואה שיש חבלה ברגל וכנראה שבר אני גם רואה סימני חבלה בצד ימין של החזה מה הכתובת שלך רחוב החרוב 12 תל אביב ומה מספר הטלפון שלך 0501234567 אל תדאג אנחנו עוצרים את הדימום עכשיו עם תחבושת לחץ ומקבעים את הרגל אני שם לך חמצן בסדר זה יעזור לך עם הנשימה תישאר רגוע אנחנו מסיימים כאן ומיד נפנה אותך לבית החולים להמשך טיפול")
    print(response)
    json_response = json.loads(response[8:-4])
    print(json_response)

#just for testing
if __name__ == "__main__":
    main()