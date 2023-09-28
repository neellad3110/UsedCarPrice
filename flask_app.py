# import flask
from flask import Flask, render_template, request, redirect, url_for , jsonify
import joblib
import pickle
import pandas as pd

app = Flask(__name__)
loaded_model = joblib.load('model.pkl')

@app.route("/")

def root():
    return render_template("index.html")


brandlist=['Audi', 'BMW', 'Bentley', 'Chevrolet', 'Datsun', 'Fiat',
        'Force', 'Ford', 'Honda', 'Hyundai', 'Isuzu', 'Jaguar', 'Jeep',
        'Lamborghini', 'Land-Rover', 'Mahindra', 'Maruti', 'Mercedes-Benz', 'Mini',
        'Mitsubishi', 'Nissan', 'Porsche', 'Renault', 'Skoda', 'Tata', 'Toyota',
        'Volkswagen', 'Volvo','Ambassador']

locationlist=['Bangalore', 'Chennai', 'Coimbatore', 'Delhi', 'Hyderabad', 'Jaipur',
       'Kochi', 'Kolkata', 'Mumbai', 'Pune','Ahmedabad']


df1=pd.DataFrame({'list':brandlist})
df2=pd.DataFrame({'list':locationlist})

temp_df=['Year', 'Kilometers_Driven', 'Owner_Type', 'Seats',
       'Bangalore', 'Chennai', 'Coimbatore', 'Delhi', 'Hyderabad', 'Jaipur',
       'Kochi', 'Kolkata', 'Mumbai', 'Pune', 'Diesel', 'LPG', 'Petrol',
       'Manual', 'Audi', 'BMW', 'Bentley', 'Chevrolet', 'Datsun', 'Fiat',
       'Force', 'Ford', 'Honda', 'Hyundai', 'Isuzu', 'Jaguar', 'Jeep',
       'Lamborghini', 'Land-Rover', 'Mahindra', 'Maruti', 'Mercedes-Benz', 'Mini',
       'Mitsubishi', 'Nissan', 'Porsche', 'Renault', 'Skoda', 'Tata', 'Toyota',
       'Volkswagen', 'Volvo']

# Routes to serve JSON data
@app.route('/get_brands', methods=['GET'])
def get_brands():
    options = df1.to_dict(orient='records')
    return jsonify(options)

@app.route('/get_locations', methods=['GET'])
def get_locations():
    options = df2.to_dict(orient='records')
    return jsonify(options)

@app.route('/get_price', methods=['POST'])
def get_price():
    if request.method == 'POST':
        brand = request.form['selectbrand']
        year = request.form['selectyear']
        location = request.form['selectlocation']
        seats = request.form['selectseats']
        fueltype = request.form['selectfueltype']
        transmission = request.form['selecttransmission']
        km = request.form['km_driven']
        ownership = request.form['selectownership']

        input_data = [0] * len(temp_df)

        for i in range(len(temp_df)):
            if i == 0 :
                input_data[0]=year
            elif i == 1 :
                input_data[1]=km
            elif i == 2 :
                input_data[2]=ownership
            elif i == 3 :
                input_data[3]=seats
            elif i >= 4 and i<= 13 :
                if temp_df[i] == location :
                    input_data[i] = 1
            elif i >= 14 and i <= 16 :
                if temp_df[i] == fueltype :
                    input_data[i] = 1            
            elif i == 15 :
                if temp_df[i] == transmission :
                    input_data[i] = 1
            else :
                if temp_df[i] == brand :
                    input_data[i] = 1


        test_dict=dict(zip(temp_df,input_data))    

        model_input_df=pd.DataFrame([test_dict])
        effective_price= loaded_model.predict(model_input_df)
        price=pd.DataFrame({'finalprice':effective_price});
        price=price.to_dict(orient='records')
        return jsonify(price)
        
        

if __name__ == '__main__':
    app.run(debug=True)