from config import *

def predict_fertilizers(model, required_columns):
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
                                  columns=required_columns)


        prediction = model.predict(input_data)

        return prediction
    except Exception as e:
        return str(e), 400

def predict_disease(image, model, label):
    try:
        img_array = img_to_array(image.resize((224,224)))
        
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        predictions = model.predict(img_array)
        predicted_label = np.argmax(predictions, axis=1)

        prediction = label[predicted_label[0]]

        return prediction
    except Exception as e:
        return str(e), 400

def predict_market(model):
    try:
        date = request.args.get('date')
        date_ordinal = pd.to_datetime(date).toordinal()
        
        prediction = model.predict([[date_ordinal]])

        return jsonify({"prediction": float(prediction)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400