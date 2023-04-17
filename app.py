import json

import pandas as pd
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import  login_user, LoginManager, current_user, logout_user
from forms import CreateMajorForm, RegisterForm, LoginForm,CreateLevelForm
from flask_gravatar import Gravatar
from functools import wraps
import os
from flask_migrate import Migrate
from models import db,User,SchoolMajor,SchoolLevel


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Absentminderteacherdahuanglikefindjob'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql://postgres:750811582@localhost:5432/SchoolMajor")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ckeditor = CKEditor(app)
Bootstrap(app)


db.init_app(app)
migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    # #CONNECT TO DB
  

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))




    @app.route('/')
    def get_all_majors():
        majors = SchoolMajor.query.all()
        return render_template("index.html", all_majors=majors, current_user=current_user)
    
    @app.route('/levels')
    def get_all_levels():
        levels = SchoolLevel.query.all()
        return render_template("Levels.html", all_levels=levels, current_user=current_user)


    @app.route('/register', methods=["GET", "POST"])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():

            # if user's email already exists
            if User.query.filter_by(email=form.email.data).first():
                # Send flash message
                flash("You've already signed up with that email, log in instead!")
                # redirect to /login route.
                return redirect(url_for('login'))

            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method="pbkdf2:sha256",
                salt_length=8
            )
            new_user = User(
                email=form.email.data,
                password=hash_and_salted_password,
                name=form.name.data
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('get_all_majors'))
        return render_template("register.html", form=form, current_user=current_user)


    @app.route('/login', methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            user = User.query.filter_by(email=email).first()

            if not user:
                flash("That email does not exist, please try again.")
                return redirect(url_for('login'))
            elif not check_password_hash(user.password, password):
                flash("Password incorrect, please try again.")
                return redirect(url_for('login'))
            else:
                login_user(user)
                return redirect(url_for('get_all_majors'))

        return render_template("login.html", form=form, current_user=current_user)


    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('get_all_majors'))


    @app.route("/major/<int:major_id>", methods=["GET", "POST"])
    def show_major(major_id):
        requested_major = SchoolMajor.query.get(major_id)
        gravatar = Gravatar(
            app,
            size=100,
            rating='g',
            default='retro',
            force_default='y',
            force_lower=False,
            use_ssl=False,
            base_url=None
        )
        return render_template("major.html", major=requested_major, current_user=current_user,  gravatar=gravatar)
    
    
    @app.route("/level/<int:level_id>", methods=["GET", "POST"])
    def show_level(level_id):
        requested_level = SchoolLevel.query.get(level_id)
        gravatar = Gravatar(
            app,
            size=100,
            rating='g',
            default='retro',
            force_default='y',
            force_lower=False,
            use_ssl=False,
            base_url=None
        )
        return render_template("level.html", level=requested_level, current_user=current_user,  gravatar=gravatar)



    def admin_only(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # If id is greater than 5 then return abort with error
            if current_user.id > 5:
                return abort(403)
            # Otherwise continue with the route function
            return f(*args, **kwargs)
        return decorated_function


    @app.route("/new-major", methods=["GET", "POST"])
    @admin_only
    def add_new_major():
        form = CreateMajorForm()
        if form.validate_on_submit():
            new_major = SchoolMajor(
                majorName=form.majorName.data,
                school=form.school.data,
                applyReq=form.applyReq.data,
                langReq=form.langReq.data,
                course=form.course.data,
                Fee=form.Fee.data,
                cluster=form.cluster.data,
                label=form.label.data,
                author=current_user,
                date=date.today().strftime("%B %d, %Y")
            )
            db.session.add(new_major)
            db.session.commit()
            return redirect(url_for("get_all_majors"))
        return render_template("make-major.html", form=form, current_user=current_user)


    @app.route("/edit-major/<int:major_id>", methods=["GET", "POST"])
    @admin_only
    def edit_major(major_id):
        major = SchoolMajor.query.get(major_id)
        edit_form = CreateMajorForm(
            majorName=major.majorName,
            school=major.school,
            applyReq=major.applyReq,
            author=major.author,
            langReq=major.langReq,
            Fee=major.Fee,
            course=major.course,
            cluster=major.cluster,
            label=major.label
        )
        if edit_form.validate_on_submit():
            major.majorName = edit_form.majorName.data
            major.school = edit_form.school.data
            major.applyReq = edit_form.applyReq.data
            major.langReq = edit_form.langReq.data
            major.Fee = edit_form.Fee.data
            major.course = edit_form.course.data
            major.cluster=edit_form.cluster.data
            major.label=edit_form.label.data
            db.session.commit()
            return redirect(url_for("show_major", major_id=major.id))

        return render_template("make-major.html", form=edit_form, current_user=current_user)


    @app.route("/deletemajor/<int:major_id>")
    @admin_only
    def delete_major(major_id):
        major_to_delete = SchoolMajor.query.get(major_id)
        db.session.delete(major_to_delete)
        db.session.commit()
        return redirect(url_for('get_all_majors'))

    @app.route("/new-level", methods=["GET", "POST"])
    @admin_only
    def add_new_level():
        form = CreateLevelForm()
        if form.validate_on_submit():
            new_level = SchoolLevel(
                countryName = form.countryName.data,
                schoolname=form.schoolname.data,
                isApply=form.isApply.data,
                isAddOn=form.isAddOn.data,
                schoolscore=form.schoolscore.data,
                addscore=form.addscore.data,
                level_author=current_user,
                date=date.today().strftime("%B %d, %Y")
            )
            db.session.add(new_level)
            db.session.commit()
            return redirect(url_for("get_all_levels"))
        return render_template("make-level.html", form=form, current_user=current_user)


    @app.route("/edit-level/<int:level_id>", methods=["GET", "POST"])
    @admin_only
    def edit_level(level_id):
        level = SchoolLevel.query.get(level_id)
        edit_form = CreateLevelForm(
            countryName=level.countryName,
            schoolname=level.schoolname,
            isApply=level.isApply,
            level_author=level.level_author,
            isAddOn=level.isAddOn,
            schoolscore=level.schoolscore,
            addscore=level.addscore,
        )
        if edit_form.validate_on_submit():
            level.countryName = edit_form.countryName.data
            level.schoolname = edit_form.schoolname.data
            level.isApply = edit_form.isApply.data
            level.isAddOn = edit_form.isAddOn.data
            level.schoolscore = edit_form.schoolscore.data
            level.addscore = edit_form.addscore.data
            db.session.commit()
            return redirect(url_for("show_level", level_id=level.id))

        return render_template("make-level.html", form=edit_form, current_user=current_user)


    @app.route("/deletelevel/<int:level_id>")
    @admin_only
    def delete_level(level_id):
        level_to_delete = SchoolLevel.query.get(level_id)
        db.session.delete(level_to_delete)
        db.session.commit()
        return redirect(url_for('get_all_levels'))


    @app.route('/import_excel', methods=["GET", "POST"])
    def import_excel():
        print("method run")
        df = pd.read_excel('testresult10.xlsx')
        data = df.values
        for i in range(0, len(data)):
            new_major = SchoolMajor(
                majorName=data[i][0],
                author_id=current_user,
                school=data[i][1],
                applyReq=data[i][2],
                langReq=data[i][3],
                course=data[i][5],
                Fee=data[i][4],
                IELTS=data[i][6],
                TOEFL=data[i][7],
                author=current_user,
                date=date.today().strftime("%B %d, %Y")
            )
            db.session.add(new_major)
     #  db.session.commit()

        return 'Excel file imported successfully!'


    @app.route('/import_schools', methods=["GET", "POST"])
    def import_chinaSchool():
        print("method run")
        df = pd.read_excel('chinaSchoolGrades.xlsx')
        data = df.values
        for i in range(0,len(data)):
            new_level = SchoolLevel(
                countryName="China",
                schoolname=data[i][0],
                isAddOn=True,
                addscore=data[i][1],
                level_author=current_user,
                date=date.today().strftime("%B %d, %Y")
            )
            db.session.add(new_level)
      #  db.session.commit()

        return  "you have imported the selected school"


    @app.route('/import_Appliedschools', methods=["GET", "POST"])
    def import_appliedSchool():
        print("method run")
        df = pd.read_excel('AppliedcountryAndGrades.xlsx')
        data = df.values
        for i in range(0, len(data)):
            new_level = SchoolLevel(
                countryName=data[i][1],
                schoolname=data[i][0],
                isApply=True,
                schoolscore=data[i][2],
                level_author=current_user,
                date=date.today().strftime("%B %d, %Y")
            )
            db.session.add(new_level)
       # db.session.commit()

        return "you have imported the selected school"

    def languageFilter(ielts,toefl):
        resultMajors = []
        if ielts == 0 :
            if toefl == 0:
                majors = SchoolMajor.query.filter((SchoolMajor.IELTS == 'NaN') & (SchoolMajor.TOEFL == 'NaN')).all()
                resultMajors = majors
            else:
                majors = SchoolMajor.query.filter((SchoolMajor.IELTS == 'NaN')& (SchoolMajor.TOEFL != 'NaN')).all()
                print(len(majors))
                for major in majors:
                    toeflScore = int(float(major.TOEFL))
                    if toefl >= toeflScore:
                        resultMajors.append(major)
        else:
            if toefl == 0:
                majors = SchoolMajor.query.filter((SchoolMajor.TOEFL == 'NaN')& (SchoolMajor.IELTS != 'NaN')).all()
                for major in majors:
                    ieltsScore = float(major.IELTS)
                    if ielts >= ieltsScore:
                        resultMajors.append(major)
            else:
                majors = SchoolMajor.query.filter((SchoolMajor.TOEFL != 'NaN')& (SchoolMajor.IELTS != 'NaN')).all()
                for major in majors:
                    ieltsScore = float(major.IELTS)
                    toeflScore = int(float(major.TOEFL))
                    if ielts>= ieltsScore and toefl >= toeflScore:
                        resultMajors.append(major)

        return resultMajors

    def countryFilter(majorList:SchoolMajor,country):
        schoolList =  SchoolLevel.query.all()
        resultSchoolList = []
        resultMajorList = []
        for school in schoolList:
            if school.countryName in country:
                resultSchoolList.append(school)

        for major in majorList:
            if major.school in resultSchoolList:
                resultMajorList.append(major)

        return  resultMajorList


    @app.route('/updates', methods=["GET", "POST"])
    def updateCluster():
        print("method run")
        df = pd.read_excel('NMFGroup.xlsx')
        data = df.values
        for i in range(0, len(data)):

            major = SchoolMajor.query.filter_by(school=data[i][1], majorName=data[i][0]).first()
            if major is None:
                print(i)
            else:
                major.cluster = data[i][8]
                major.label = data[i][9]
                db.session.add(major)
                db.session.commit()


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


    def handleRequest(request:json):
        school = request['school_name']
        gpa = request['gpa']
        ielts = request.get('IELTS', 0)
        toefl = request.get('TOEFL', 0)
        country = request['country']
        schoolInDb = SchoolLevel.query.filter(schoolname = school).first()
        finalGpa = int(gpa) + int(schoolInDb.addscore)

        allSchool =  SchoolLevel.query.filter( (SchoolLevel.country == country) & (SchoolLevel.isapply == True )).all() # country
        gpaGoodScool = []
        for school in allSchool:
            requireScore =  int (school.schoolscore)
            if requireScore<finalGpa:  #  gpa
                gpaGoodScool.append(school)


        languageResult = languageFilter(ielts, toefl)  # language
        finalResult = []
        for major in languageResult:
            if major.school in gpaGoodScool:
                finalResult.append(major)



        return finalResult

    if __name__ == "__main__":
        db.create_all()
        app.run(debug=True)
