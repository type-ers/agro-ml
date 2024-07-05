from config import *

__app__ = Flask(__name__)

# authentication

fetilizer_model = load(fertilizer_model_dir)
fertilizer_rqcolumns = ['Temperature', 'Humidity', 'Moisture', 'Soil Type', 'Crop Type', 'Nitrogen', 'Potassium', 'Phosphorous']

disease_model = {
    "apple" : load_model(d_model_apple_dir),
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

@__app__.route('/')
def home():
    return render_template("index.html")

@__app__.route('/disease')
def disease():
    return render_template("disease.html")

@__app__.route('/disease', methods=['POST'])
def process_disease_form():
    leaf_type = request.form.get('dropdown')
    file = request.files['image']
    try:
        image = Image.open(file)
        img_array = img_to_array(image.resize((224,224)))
        
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        predictions = (disease_model[leaf_type]).predict(img_array)
        predicted_label = np.argmax(predictions, axis=1)

        prediction = (disease_label[leaf_type])[predicted_label[0]]
        
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@__app__.route('/api/fertilizer', methods=['GET'])
def api_fertilizer():
    try:
        temperature = float(request.args.get('temperature'))
        humidity = float(request.args.get('humidity'))
        moisture = float(request.args.get('moisture'))
        soil_type = request.args.get('soil_type')
        crop_type = request.args.get('crop_type')
        nitrogen = float(request.args.get('nitrogen'))
        potassium = float(request.args.get('potassium'))
        phosphorous = float(request.args.get('phosphorous'))

        input_data = pd.DataFrame([[temperature, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorous]],
                                  columns=['Temperature', 'Humidity', 'Moisture', 'Soil Type', 'Crop Type', 'Nitrogen', 'Potassium', 'Phosphorous'])

        prediction = fetilizer_model.predict(input_data)

        return jsonify({"prediction": prediction[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@__app__.route('/api/market', methods=['GET'])
def api_market():
    commodity = request.args.get('commodity')
    date = request.args.get('date')

    try:
        date_ordinal = pd.to_datetime(date).toordinal()
        print(market_models[commodity])
        prediction = (market_models[commodity]).predict([[date_ordinal]])
        return jsonify({"prediction": float(prediction)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@__app__.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

if __name__ == '__main__':
    __app__.run(port=8000)