# from flask import Flask, request, render_template, jsonify
# import pickle
# import pandas as pd
# from sklearn.preprocessing import LabelEncoder
# import traceback

# app = Flask(__name__)

# # Load the model from the specified path
# model_path = '/Users/harunorrashidsajib/Desktop/Pyhton/crop_prediction_model.pkl'
# with open(model_path, 'rb') as f:
#     model = pickle.load(f)

# # Load crop names and fit a label encoder
# data = pd.read_csv('V3_crop_environment_data_with_lih_and_advice_with_error.csv')
# crop_names = data['Crop Name'].unique().tolist()
# label_encoder = LabelEncoder()
# label_encoder.fit(crop_names)

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         try:
#             # Get input values from the form
#             temperature = float(request.form['temperature'])
#             humidity = float(request.form['humidity'])
#             soil_moisture = float(request.form['soil_moisture'])
#             light_intensity = float(request.form['light_intensity'])
#             crop_name = request.form['crop_name']
            
#             # Encode the crop name
#             crop_name_encoded = label_encoder.transform([crop_name])[0]
            
#             # Create a DataFrame for the input data
#             input_data = pd.DataFrame([[temperature, humidity, soil_moisture, light_intensity, crop_name_encoded]],
#                                       columns=['Temperature', 'Humidity', 'Soil Moisture', 'Light Intensity', 'Crop Name'])

#             # Make prediction
#             prediction = model.predict(input_data)
#             advice = prediction[0]  # Store the prediction result
#             return jsonify({'Advice': advice})
#         except Exception as e:
#             # Print error details to console
#             print("An error occurred:", e)
#             traceback.print_exc()
#             return jsonify({'error': 'An error occurred. Please try again.'}), 500

#     return render_template('index.html', crop_names=crop_names)

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import traceback
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Load the model from the specified path
# Load the model from the specified path
model_path = 'crop_prediction_model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Load crop names and fit a label encoder
data = pd.read_csv('V3_crop_environment_data_with_lih_and_advice_with_error.csv')
crop_names = data['Crop Name'].unique().tolist()
label_encoder = LabelEncoder()
label_encoder.fit(crop_names)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name('black-media-386619-0e541c4ee39e.json', scope)
client = gspread.authorize(creds)

# Open the spreadsheet by its URL
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1bOPtxYV2xsDtBWfj8EhQniRMEafk6mBUr_DoD9et5is/edit?gid=152194846'
spreadsheet = client.open_by_url(spreadsheet_url)
worksheet = spreadsheet.get_worksheet(0)  # Get the first worksheet

def get_last_row():
    """Fetches the last row from the Google Sheet"""
    data = worksheet.get_all_values()
    return data[-1]  # Return the last row

@app.route('/', methods=['GET', 'POST'])
def home():
    last_row = get_last_row()  # Fetch the last row from the sheet
    if request.method == 'POST':
        try:
            # Get input values from the form
            temperature = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            soil_moisture = float(request.form['soil_moisture'])
            light_intensity = float(request.form['light_intensity'])
            crop_name = request.form['crop_name']
            
            # Encode the crop name
            crop_name_encoded = label_encoder.transform([crop_name])[0]
            
            # Create a DataFrame for the input data
            input_data = pd.DataFrame([[temperature, humidity, soil_moisture, light_intensity, crop_name_encoded]],
                                      columns=['Temperature', 'Humidity', 'Soil Moisture', 'Light Intensity', 'Crop Name'])

            # Make prediction
            prediction = model.predict(input_data)
            advice = prediction[0]  # Store the prediction result
            return jsonify({'Advice': advice})
        except Exception as e:
            # Print error details to console
            print("An error occurred:", e)
            traceback.print_exc()
            return jsonify({'error': 'An error occurred. Please try again.'}), 500

    return render_template('index.html', crop_names=crop_names, last_row=last_row)



@app.route('/fetch_last_row', methods=['GET'])
def fetch_last_row():
    try:
        last_row = get_last_row()  # Fetch the last row from the sheet
        return jsonify({
            'temperature': last_row[2],  # Should be a float value for temperature
            'humidity': last_row[3],     # Should be a float value for humidity
            'soil_moisture': last_row[4], # Should be a float value for soil moisture
            # 'light_intensity': last_row[3] 
        })
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
        return jsonify({'error': 'An error occurred while fetching data.'}), 500



if __name__ == '__main__':
    app.run(debug=True)
