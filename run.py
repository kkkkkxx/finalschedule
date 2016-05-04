from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

# Try adding your own number to this list!
callers = {
    "+14124179805": "George",
    "+19542269211": "Philip",
}

finals = {
    "AANL 10103 1":["Elementary Hittite (3)", "Wednesday", "June 8th", "OR 315", "8:00 AM", "10:00 AM"],
    "AKKD 10103 1":["Elementary Akkadian (3)", "Monday", "June 6th", "OR 210", "10:30 AM", "12:30 PM"],
    "ANTH 21420 1":["Ethnographic Methods", "Thursday", "June 9th", "HM 104", "1:30 PM", "3:30 PM"],
    "ARAB 10103 1":["Elementary Arabic (3)", "Friday", "June 10th", "HM 145", "10:30 AM", "12:30 PM"],
    "ARAB 10103 2":["Elementary Arabic (3)", "Monday", "June 6th", "HM 145", "10:30 AM", "12:30 PM"],
    "ARAB 10103 3":["Elementary Arabic (3)", "Friday", "June 10th", "HM 145", "1:30 PM", "3:30 PM"],
}


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""

    from_number = request.values.get('From', None)
    if from_number in callers:
        message = callers[from_number] + ", thanks for the message!"
    else:
        message = "Please make sure you have the correct format! Text [Dept. Code] [Class Number] [Section Number]. For example, 'CMSC 11000 1'. You can find your section number at http://classes.uchicago.edu"

    resp = twilio.twiml.Response()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
