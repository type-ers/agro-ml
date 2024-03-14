from config import *

class LoginForm(FlaskForm):
    def assign_model(self, model):
        self.model = model

    username = StringField(
        validators=[InputRequired(), Length(min=4, max=26)],
        render_kw={"placeholder": "Username"}
    )


    email = EmailField(
        validators=[InputRequired(), Length(min=6, max=254), Email()],
        render_kw = {"placeholder": "Email"}
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw = {"placeholder": "Password"}
    )

    sumbit = SubmitField("Login")    


class RegisterForm(FlaskForm):
    def assign_model(self, model):
        self.model = model

    username = StringField(
        validators=[InputRequired(), Length(min=4, max=26)],
        render_kw={"placeholder": "Username"}
    )

    email = EmailField(
        validators=[InputRequired(), Length(min=6, max=254), Email()],
        render_kw = {"placeholder": "Email"}
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw = {"placeholder": "Password"}
    )

    sumbit = SubmitField("Register")

    def validate_username(self, username: str):
        existing_user_name = self.model.query.filter_by(username=username.data).first()

        if existing_user_name:
            raise ValidationError(
                f"{username.data} already exists, try logging in {url_for('login')}"
            )


def session_login(bcrypt: Bcrypt, db: SQLAlchemy, model):
    form = LoginForm()
    form.assign_model(model)

    if form.validate_on_submit():
        user = form.model.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for(f'user/{user.id}'))

    return render_template("login.html", form=form)

def register_account(bcrypt: Bcrypt, db: SQLAlchemy, model):
    form = RegisterForm()
    form.assign_model(model)
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)

        new_user = model(
            username = form.username.data,
            email = form.email.data,
            password = hashed_password
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html", form=form)

def fetch_account(user_id: int, model):
    user = model.query.get(user_id)
    if not user:
        abort(404)

    if user.image:
        image = b64encode(user.image).decode('utf-8')
        _bytes = user.image
    else:
        default_image_path = join('web', 'default.png')
        with open(default_image_path, 'rb') as f:
            image = b64encode(f.read()).decode('utf-8')
        _bytes = 0

    return render_template("user.html", 
        username = user.username,
        email = user.email,
        image = image,
        bytes = _bytes
    )

def logout():
    logout_user()
    return redirect(url_for('login'))