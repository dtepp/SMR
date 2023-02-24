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
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql://postgres:lily@localhost:5432/SchoolMajor")
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
                levelname=form.levelname.data,
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
            levelname=level.levelname,
            schoolname=level.schoolname,
            isApply=level.isApply,
            level_author=level.level_author,
            isAddOn=level.isAddOn,
            schoolscore=level.schoolscore,
            addscore=level.addscore,
        )
        if edit_form.validate_on_submit():
            level.levelname = edit_form.levelname.data
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


    if __name__ == "__main__":
        db.create_all()
        app.run(debug=True)
