from flask import Flask, request, make_response, jsonify
import requests, json

app = Flask(__name__)

data = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print('Request:')
    print(json.dumps(req, indent=4))
    resp_text = ""
    # Extract parameters from the request
    intent_name = req["queryResult"]["intent"]["displayName"]
    if intent_name == 'University':
        school_name = req['queryResult']['parameters']['university']
        data['school_name'] = school_name
        resp_text = "What is your GPA?"
    if intent_name == 'GPA':
        gpa = req['queryResult']['parameters']['gpa']
        data['gpa'] = gpa
        resp_text = "What‘s your Language score? Please enter your IELTS or TOEFL directly."
    if intent_name == 'Language scores':
        toefl = req['queryResult']['parameters']['language']
        ielts = req['queryResult']['parameters']['ielts']
        if ielts is not None:
            data['IELTS'] = ielts
        if toefl is not None:
            data['TOEFL'] = toefl
        resp_text = "Which country you want to presume your postgraduate degree?"
    if intent_name == 'Country':
        country = req['queryResult']['parameters']['country']
        data['country'] = country
        resp_text = "Which filed you want to study? Please choose from these research areas: Computer Science, Engineering, Business, Economics, Law, Medicine, Arts, Education, Social Science, Agriculture, Environment. Please describe the details the courses you want to learn from the field you choose: For example, if you choose Computer Science, you can enter 'Computer Science: Machine Learning, Deep Learning, Computer Vision, Natural Language Processing, Data Mining, Data Science, Big Data, etc.'"
    if intent_name == 'Research area':
        research_area = req['queryResult']['queryText']
        result = research_area.split(":")
        data['research_area'] = result[0]
        data['courses'] = result[1]
        # 在这里，调取杜杜的方法，将json传到后端，去进行下一步操作
        resp_text = "Here are the universities you can apply for."

    # Save data to file in JSON format

    with open('data.json', 'w') as f:
        json.dump(data, f)

    return make_response(jsonify({'fulfillmentText': resp_text}))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
