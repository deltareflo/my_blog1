from flask import Flask, render_template, request, redirect, url_for, abort, flash
from werkzeug.urls import url_parse
from config import DeveloperConfig
from models import Usuarios, db, Blog
from forms import SignupForm, LoginForm, BlogForm
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import datetime
import locale

app = Flask(__name__)

app.config.from_object(DeveloperConfig)
login_manager = LoginManager(app)
login_manager.login_view = "login"
db.app = app
db.init_app(app)
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
# df1 = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSQ5NCVPoep7GUF5rFwqZ6jcaP84OVob42xcJjaBwo6YmWJM3MT89QmQaavTSo3Eqoi8cgsM1dOPv0S/pub?output=csv")

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.get_by_id(int(user_id))


@app.route('/')
#@login_required
def inicio():
    blogs = Blog.query.all()
    users = Usuarios.query.all()
    return render_template('index.html', blogs=blogs, users=users)


@app.route('/post/<int:bg_id>', methods=['GET'])
def post(bg_id):
    blog = Blog.query.filter_by(id=bg_id).first()
    user = Usuarios.query.filter_by(id=blog.id_user).first()
    return render_template('post_base.html', blog=blog, user=user)


@app.route('/about/', methods=['GET'])
def about():

    return render_template('about.html')


@app.route("/add-blog/", methods=['GET', 'POST'])
@login_required
def add_blog():

    if request.method == 'POST':
        titulo= request.form['titulo']
        subtitulo = request.form['subtitulo']
        contenido = request.form['contenido']
        fecha = datetime.datetime.now()
        new_blog = Blog(title=titulo, subtitle=subtitulo, id_user=current_user.id,
                        date=fecha, contenido=contenido)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('inicio'))
    return render_template('add.html')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('inicio'))


@app.route('/login/', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuarios.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('inicio')
            return redirect(next_page)
    return render_template('auth-signin.html', form=form)


@app.route('/signup/',  methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        edad = form.edad.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = Usuarios.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = Usuarios(nombre=name, email=email, edad=edad)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('inicio')
            return redirect(next_page)
    return render_template('signup.html', form=form, error=error)


if __name__ == '__main__':

    #print jdata
    db.create_all()
    app.run(debug=True)




