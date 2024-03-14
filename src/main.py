from models import *
from auth import *

__app__ = Flask(__name__, template_folder=abspath('web/'), static_folder=abspath('web/static'))
__app__.config['SECRET_KEY'] = "randomhashhere"

# database

__app__.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + abspath('db/meta.db')
__app__.config['SQLALCHEMY_BINDS'] = {"auth": {"url": "sqlite:///" + abspath('db/auth.db')}}

db = SQLAlchemy(__app__)

# authentication

class User(db.Model):
    __bind_key__ = "auth"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(26), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(72), nullable=False)
    image = db.Column(LargeBinary)

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.init_app(__app__)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return redirect(url_for(f'user/{user_id}'))


fetilizer_model = load(fertilizer_model_dir)
fertilizer_rqcolumns = ['Temperature', 'Humidity', 'Moisture', 'Soil Type', 'Crop Type', 'Nitrogen', 'Potassium', 'Phosphorous']


disease_model = {
    "apple" : load_model(d_model_apple_dir)
}

disease_label = {
    "apple": ["brown_spot", "healthy", "mosaic"] 
}

market_models = {}
for filename in listdir(market_dir):
    if filename.endswith('.pkl'):
        commodity = filename.split('_')[0]
        model_path = join(market_dir, filename)
        try:
            model = load(model_path)
            market_models[commodity] = model
        except Exception as e:
            print(f"Error loading model '{filename}': {str(e)}")


# home

@__app__.route('/')
def home():
    return render_template("index.html")

# authentication

@__app__.route('/login', methods=["GET", "POST"])
def login():
    return session_login(bcrypt, db, User)

@__app__.route('/register', methods=["GET", "POST"])
def signup():
    return register_account(bcrypt, db, User)

@__app__.route('/user/<user_id>')
def profile(user_id):
    return fetch_account(int(user_id), User)

# info

@__app__.route('/fertilizer')
def fertilizer():
    return render_template("fertilizer.html")

@__app__.route('/disease')
def disease():
    return render_template("disease.html")

@app.route('/disease', methods=['POST'])
def process_disease_form():
    leaf_type = request.form.get('dropdown')
    file = request.files['image']

    try:
        image = Image.open(BytesIO(file.read()))
        prediction = predict_disease(image, disease_model[leaf_type], disease_label[leaf_type])
        
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@__app__.route('/market')
def market():
    return render_template("market.html")

# playground
@__app__.route('/playground')
def playground():   
    return render_template("playground.html")

# docs

@__app__.route('/docs')
def docs():
    return render_template("docs/index.html")

# api

@__app__.route('/api/fertilizer', methods=['GET'])
def api_fertilizer():
    return predict_fertilizers(fetilizer_model, fertilizer_rqcolumns)

@__app__.route('/api/disease/<leaf_type>', methods=['GET'])
def api_disease(leaf_type):
    try:
        file = request.args.get('file')
        url = request.args.get('url').strip('"')

        if file:
            image = Image.open(BytesIO(file.read()))
        elif url:
            response = requests.get(url)
            if response.status_code != 200:
                return jsonify({"error": "Invalid URL or unable to fetch image"})
            image = Image.open(BytesIO(response.content))
        else:
            return jsonify({"error": "No file or URL provided"})

        img_array = img_to_array(image.resize((224,2)))
        
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        predictions = disease_model[leaf_type].predict(img_array)
        predicted_label = np.argmax(predictions, axis=1)

        prediction = (disease_label[leaf_type])[predicted_label[0]]

        return jsonify({"prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
        

@__app__.route('/api/market', methods=['GET'])
def api_market():
    commodity = request.args.get('commodity')

    if commodity in market_models:
        return predict_market(market_models[commodity])
    else:
        return jsonify({"error": f"Model for commodity '{commodity}' not found"}), 404


@__app__.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

with __app__.app_context():
    db.create_all() 

if __name__ == '__main__':
    __app__.run(debug=True, port=8888)