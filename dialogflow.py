from flask import Flask, request, make_response, jsonify
import requests, json
import telegram
import asyncio
import pandas as pd

app = Flask(__name__)

data = {}

my_list = [['Master of Science in Integrated Circuit Design（TUMA）', 'Nanyang Technological University', "Applicants must have obtained at least a Commonwealth (Second Class Honours) Bachelor of Science/Electrical/Electronic Engineering from a\
university;\nor European/German FH Diploma or equivalent;\nA bachelor's degree from a Chinese university with grades meeting certain requirements;\nOr equivalent;",
            'IELTS 6.5; or TOEFL 100; APS audit certificate is required', 'The tot\
al tuition fee is 43,316 SGD; the living expenses are about 80,000 RMB/year, and the total cost after 2 years of study is about 380,000 RMB.'],
           ['Master of Science in Power Engineering', 'Nanyang Technological University', "related maj\
ors;\nA bachelor's degree from a Chinese university with grades meeting certain requirements;\nOr equivalent;",
            'IELTS 6.5; or TOEFL 100', 'The total tuition fee is 43,200 SGD; the living expenses are about 80,000 RMB/year, and the tot\
al cost after one year of study is about 300,000 RMB.'],
           ['Master of Science in Computer Control & Automation', 'Nanyang Technological University', "related majors;\nA bachelor's degree from a Chinese university with grades meeting cer\
tain requirements;\nOr equivalent;\nRelevant work experience is an advantage;", 'IELTS 6.5; or TOEFL 100.', 'The total tuition fee is 43,200 SGD; the living expenses are about 80,000 RMB/year, and the total cost after one year of study\
 is about 300,000 RMB.'], ['Master of Science in Electronics', 'Nanyang Technological University',
                           "A bachelor's degree from a Chinese university with certain grades;\nOr equivalent;\nRelevant work experience is preferred;", 'IELTS 6.5\
; or TOEFL 100',
                           'The total tuition fee is 43,200 SGD; the living expenses are about 80,000 RMB/year, and the total cost after one year of study is about 300,000 RMB.'],
           ['Master of Technology in Intelligent Systems', 'National Univers\
ity of Singapore', "preferably a science or engineering major;\nA bachelor's degree from a Chinese university with certain grades;\nOr equivalent;\nAnd require a GPA of B;\nGRE or entrance exam;\n2 years of relevant work experience rec\
ommended (applicants with a highly relevant IT degree, good academic record, and good working knowledge of software development acquired through coursework, course projects or professional IT certifications may be exempt from the exper\
ience requirement)", 'TOEFL 85; or IELTS 6.0;',
            'The total tuition fee is 55,319-58,208 Singapore dollars; the living expenses are about 80,000 RMB/year, and the total cost after one year of study is about 360,000 RMB.'],
           ['Master of S\
cience in Green Electronics（TUMA）', 'Nanyang Technological University', "A Bachelor's degree in Electrical and Electronic Engineering or a closely related discipline;\nFundamentals of semiconductor physics, electromagnetism and organ\
ic chemistry (or electrochemistry);\nA bachelor's degree from a Chinese university with grades meeting certain requirements;\nOr equivalent;",
            'TOEFL 100 or IELTS 6.5; APS audit certificate is required;', 'The total tuition fee is 43,3\
16 SGD; the living expenses are about 80,000 RMB/year, and the total cost after 2 years of study is about 380,000 RMB.'],
           ['Master of Science in Materials Science and Engineering', 'Nanyang Technological University', "Engineering or re\
lated major;\nA bachelor's degree from a Chinese university with grades meeting certain requirements;\nOr equivalent;\nor Materials Science and Engineering;\nOr related majors with considerable years of relevant work experience;", 'IEL\
TS 6.5; or TOEFL 100',
            'The total tuition fee is 34,000 SGD; the living expenses are about 80,000 RMB per year; the total cost after one year of study is about 241,000 RMB'],
           ['Master of Science in Life Sciences（clean energy physics）\
', 'Nanyang Technological University', "A BSc Honors degree in a relevant course or equivalent, or\nA Bachelor of Science degree or equivalent in a relevant course, plus one year of professional work experience;\nA bachelor's degree fr\
om a Chinese university with grades meeting certain requirements;\nOr equivalent;", 'TOEFL 92; or IELTS 6.5', 'The total tuition fee is 44,679 Singapore dollars, and the living expenses are about 80,000 RMB per year; the total cost aft\
er one year of study is about 300,000 RMB.'],
           ['MSc in Precision Scientific Instrumentation', 'Nanyang Technological University', "Physics, engineering, optics, applied physics or related majors;\nA bachelor's degree from a Chinese uni\
versity with grades meeting certain requirements;\nOr equivalent;",
            'Good TOEFL or IELTS;\nGood GRE or GMAT scores are preferred;', 'The total tuition fee is 43,200 SGD; the living expenses are about 80,000 RMB/year, and the total cost\
 after one year of study is about 300,000 RMB.'],
           ['Master of Computing（Computer Science Specialisation）', 'National University of Singapore', 'Four-year undergraduate or Commonwealth Honors related degree, or have obtained a postgra\
duate certificate in computer foundation;\nAnd CAP reaches 3.0 or above: IT-related work experience is preferred;\nGRE320 (verbal and mathematics) and 3.5 (writing);\nor GMAT650;',
            'TOEFL 90; or IELTS 6.0',
            'The total tuition fee is 51\ ,000 SGD, the living expenses are about 80,000 RMB/year, and the total cost after 1.5 years of study is about 380,000 RMB']]


async def send_excel_file(chat_id, list):
    # 将列表转换为DataFrame对象
    df = pd.DataFrame(list,
                      columns=['University Name', 'Major Name', 'Language Requirments', 'Major Requirments', 'Fee'])

    # 将DataFrame写入Excel文件
    df.to_excel('result.xlsx', index=False)

    with open('result.xlsx', 'rb') as f:
        file_data = f.read()

    # 使用bot token初始化机器人
    bot = telegram.Bot(token='6029920369:AAH43WlnyDpQCx6zHi0o0N2mG_tW9zezrzc')

    # 发送文件到当前聊天
    await bot.send_document(chat_id=chat_id, document=file_data, filename='result.xlsx')


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
        resp_text = "Which filed you want to study? Please choose from these research areas: History, Law, Health, Environmental engineering direction, Education, Fintech, Music, Art, Computer science, Social studies. Please describe the details the courses you want to learn from the field you choose: For example, if you choose Computer science, you can enter 'Computer science: Machine Learning, Deep Learning, Computer Vision, Natural Language Processing, Data Mining, Data Science, Big Data, etc.'"
    if intent_name == 'Research area':
        research_area = req['queryResult']['queryText']
        result = research_area.split(":")
        data['research_area'] = result[0]
        data['courses'] = result[1]

        # 获取当前聊天的chat_id
        chat_id = req['originalDetectIntentRequest']['payload']['data']['chat']['id']
        # 调用async函数
        asyncio.run(send_excel_file(chat_id, my_list))

    # Save data to file in JSON format
    with open('data.json', 'w') as f:
        json.dump(data, f)

    return make_response(jsonify({'fulfillmentText': resp_text}))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
