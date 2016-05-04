from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

# Try adding your own number to this list!
callers = {
    "+14124179805": "George",
    "+19542269211": "Philip",
}

finals = {
    "AANL 10103 1": ["LEC", "Elementary Hittite (3)", "Goedegebuure", "8:00 AM", "10:00 AM", "W", "6/8/2016", "OR 315"],
    "AKKD 10103 1": ["LEC", "Elementary Akkadian (3)", "Reculeau", "10:30 AM", "12:30 PM", "M", "6/6/2016", "OR 210"],
    "ANTH 21420 1": ["SEM", "Ethnographic Methods", "Jenkins", "1:30 PM", "3:30 PM", "R", "6/9/2016", "HM 104"],
    "ARAB 10103 1": ["LEC", "Elementary Arabic (3)", "abu-Eledam", "10:30 AM", "12:30 PM", "F", "6/10/2016", "HM 145"],
    "ARAB 10103 2": ["LEC", "Elementary Arabic (3)", "abu-Eledam", "10:30 AM", "12:30 PM", "M", "6/6/2016," "HM 145"],
    "ARAB 10103 3": ["LEC", "Elementary Arabic (3)", "Choudar", "1:30 PM", "3:30 PM", "F", "6/10/2016", "C 201A-B"],
    "ARAB 10251 1": ["LEC", "Colloquial Egyptian Arabic (1)", "Abdel Mobdy", "1:30 PM", "3:30 PM", "R", "6/9/2016", "C 210"],
    "ARAB 20103 2": ["LEC", "Intermediate Arabic (3)", "Heikkinen", "1:30 PM", "3:30 PM", "F", "6/10/2016", "C 104"],
    "ARAB 20103 3": ["LEC", "Intermediate Arabic (3)", "Abdel Mobdy", "4:00 PM", "6:00 PM", "R", "6/9/2016", "WB 230"],
    "ARAB 29001 1": ["LEC", "Arabic Through Film", "Forster", "1:30 PM", "3:30 PM", "T", "6/7/2016", "C 403"],
    "ARAB 30203 1": ["LEC", "High Intermediate Modern Standard Arabic (3)", "Forster", "10:30 AM", "12:30 PM", "W", "6/8/2016", "HM 104"],
    "ARAB 30303 1": ["LEC", "High Intermediate Classical Arabic (3)", "Heikkinen", "10:30 AM", "12:30 PM", "W", "6/8/2016", "C 104"],
    "ARAB 30352 1": ["LEC", "Arabic Through Maghribi Literature", "Choudar", "4:00 PM", "6:00 PM", "W", "6/8/2016", "C 430"],
    "ARAB 40102 1": ["LEC", "Advanced Arabic Syntax (2)", "Qutbuddin", "10:30 AM", "12:30 PM", "T", "6/7/2016", "P 218"],
    "ARAB 40392 1": ["SEM", "Readings: The Sira Literature", "Donner", "1:30 PM", "3:30 PM", "F", "6/10/2016", "OR 210"],
    "ARAM 10403 1": ["LEC", "Elementary Syriac (3)", "Creason", "10:30 AM", "12:30 PM", "R", "6/9/2016", "OR 208"],
    "ARTH 15707 1": ["CRS", "American Art since the Great War", "English", "1:30 PM", "3:30 PM", "T", "6/7/2016", "CWAC 157"],
    "ARTV 10100 1": ["CRS", "Visual Language: On Images", "Beck", "1:30 PM", "3:30 PM", "F", "6/10/2016", "LC 601"],
    "ARTV 10100 2": ["CRS", "Visual Language: On Images", "Mauser", "6:00 PM", "8:00 PM", "T", "6/7/2016", "LC 401"],
    "ARTV 10100 3": ["CRS", "Visual Language: On Images", "Adams", "10:30 AM", "12:30 PM", "T", "6/7/2016", "LC 401"],
    "ARTV 10100 4": ["CRS", "Visual Language: On Images", "Lloyd", "1:30 PM", "3:30 PM", "T", "6/7/2016", "LC 601"],
    "ARTV 10100 5": ["CRS", "Visual Language: On Images", "Williamson", "4:00 PM", "6:00 PM", "T", "6/7/2016", "LC 601"],
    "ARTV 10200 1": ["CRS", "Visual Language: On Objects", "Jackson", "10:30 AM", "12:30 PM", "M", "6/6/2016", "LC 110"],
    "ARTV 10200 2": ["CRS", "Visual Language: On Objects", "Rouse", "10:30 AM", "12:30 PM", "M", "6/6/2016", "a classroom that is not yet listed"],
    "ARTV 21501 1": ["CRS", "Introduction to Printmaking", "Desjardins", "1:30 PM", "3:30 PM", "T", "6/7/2016", "LC 109"],
    "ARTV 22310 1": ["CRS", "Art of Engagement", "Ginsburg", "10:30 AM", "12:30 PM", "T", "6/7/2016", "LC 108"],
    "ARTV 22500 1": ["CRS", "Digital Imaging", "Salavon", "10:30 AM", "12:30 PM", "M", "6/6/2016", "LC 028"],
    "ARTV 22502 1": ["CRS", "Data and Algorithm in Art", "Salavon", "1:30 PM", "3:30 PM", "F", "6/10/2016", "LC 028"],
    "ARTV 23804 1": ["CRS", "Experimental Animation", "Wolniak", "10:30 AM", "12:30 PM", "T", "6/7/2016", "LC 014"],
    "ARTV 23805 1": ["CRS", "Minimalist Experiment in Film and Video", "Rodowick", "1:30 PM", "3:30 PM", "T", "6/7/2016", "LC 014"],
    "ARTV 24121 1": ["CRS", "Adopted Strategies", "Jackson", "1:30 PM", "3:30 PM", "F", "6/10/2016", "LC 110"],
    "ARTV 24201 1": ["CRS", "Collage", "Wolniak", "1:30 PM", "3:30 PM", "T", "6/7/2016", "LC 401"],
    "ARTV 24401 1": ["CRS", "Photography (1)", "Letinsky", "1:30 PM", "3:30 PM", "F", "6/10/2016", "ED B 045 D"],
    "ARTV 24402 1": ["CRS", "Photography (2)", "Letinsky", "1:30 PM", "3:30 PM", "F", "6/10/2016", "a classroom not yet listed"],
    "ARTV 27210 1": ["CRS", "Intermediate/Advanced Painting", "Desjardins", "8:00 AM", "10:00 AM", "T", "6/7/2016", "LC 203"],
    "ARTV 29600 1": ["CRS", "Junior Seminar", "Ginsburg", "1:30 PM", "3:30 PM", "T", "6/7/2016", "LC 802"],
    "ARTV 39901 1": ["CRS", "21st Century Art", "Jackson", "8:00 AM", "10:00 AM", "W", "6/8/2016", "LC 802"],
    "ARTV 44319 1": ["CRS", "Writing Images/Picturing Words", "Stockholder", "1:30 PM", "3:30 PM", "F", "6/10/2016" "LC 109"],
    "ASLG 10300 1": ["CRS", "American Sign Language (3)", "Ronchen", "10:30 AM", "12:30 PM", "W", "6/8/2016", "C 115"],
    "ASLG 10300 2": ["CRS", "American Sign Language (3)", "Ronchen", "4:00 PM", "6:00 PM", "R", "6/9/2016", "C 115"],
    "ASLG 10600 1": ["CRS", "Intermediate ASL (3)", "Ronchen", "10:30 AM", "12:30 PM", "R", "6/9/2016", "C 115"],
    "BANG 10300 1": ["CRS", "First-Year Bangla (3)", "Bhaduri", "8:00 AM", "10:00 AM", "W", "6/8/2016", "C 210"],
    "BANG 20300 1": ["CRS", "Second-Year Bangla (3)", "Bhaduri", "10:30 AM", "12:30 PM", "F", "6/10/2016", "C 228"],
    "BASQ 12200 1": ["CRS", "Elementary Basque (3)", "Palenzuela Rodrigo", "10:30 AM", "12:30 PM", "R", "6/9/2016", "C 430"],
    "BCSN 10303 1": ["CRS", "First-Year Bosnian/Croatian/Serbian (3)", "Petkovic", "1:30 PM", "3:30 PM", "F", "6/10/2016", "C 205"],
    "BCSN 20303 1": ["CRS", "Second-Year Bosnian/Croatian/Serbian (3)", "Petkovic", "10:30 AM", "12:30 PM", "M", "6/6/2016", "F 408"],
    "BCSN 21300 1": ["CRS", "(Re)Branding the Balkan City: Comtemp Belgrade/Sarajevo/Zagreb", "Petkovic", "10:30 AM", "12:30 PM", "R", "6/9/2016", "F 408"]
}


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""

    message_body = request.values.get('Body', None)
    if message_body in finals:
        classname = finals[message_body][1] + ""
        classprofessor = finals[message_body][2] + ""
        classweekday = finals[message_body][5] + ""
        classdate = finals[message_body][6] + ""
        finalbegin = finals[message_body][3] + ""
        finalend = finals[message_body][4] + ""
        finalroom = finals[message_body][7] + ""
        yourfinal = "Class Name: " + classname + "\nProfessor: " + classprofessor + "\nDate: " + classweekday + ", " + classdate + "\n" + "Location: " + finalroom + "\nTime: " + finalbegin + " - " + finalend + ""
        message = yourfinal
    else:
        message = "Please make sure you have the correct format ([Dept. Code] [Class Number] [Section Number])! For example, send 'CMSC 11000 1'. You can find the section number for your classes at http://classes.uchicago.edu. If you are sure you are texting your class correctly, your department may not be listed on the final exam schedule yet."

    resp = twilio.twiml.Response()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
