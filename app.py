from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import os
import pandas as pd
import random  

app = Flask(__name__)

# Load your trained models here
random_forest_model = pickle.load(open('./models/rf_reg_insurance.pkl','rb'))
gradient_boost_model = pickle.load(open('./models/gb_reg_insurance.pkl','rb'))
xgboost_model = pickle.load(open('./models/xgb_reg_insurance.pkl','rb'))

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/form')    
def form_page():
    return render_template('form.html')
 
@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        age = int(request.form["age"])
        surgeries_count = int(request.form["surgeries"])
        weight = int(request.form["weight"])
        chronic = 1 if request.form['chronic'].lower() == 'yes' else 0
        transplants = 1 if request.form['transplants'].lower() == 'yes' else 0
        cancer = 1 if request.form['cancer'].lower() == 'yes' else 0

        if age >= 27.6 and age < 37.2:
            age_label_mod_low = 1
            age_label_mod = 0
            age_label_mod_high = 0
            age_label_high = 0
        elif age >= 37.2 and age < 46.8 :
            age_label_mod_low = 0
            age_label_mod = 1
            age_label_mod_high = 0
            age_label_high = 0
        elif age >= 46.8 and age < 56.4 :
            age_label_mod_low = 0
            age_label_mod = 0
            age_label_mod_high = 1
            age_label_high = 0
        elif age >= 56.4 and age < 66:
            age_label_mod_low = 0
            age_label_mod = 0
            age_label_mod_high = 0
            age_label_high = 1
        else:
            age_label_mod_low = 0
            age_label_mod = 0
            age_label_mod_high = 0
            age_label_high = 0

        if age_label_mod_low == 1 :
            premiumLabel_mod_low = 1
            premiumLabel_mod = 0
            premiumLabel_mod_high = 0
            premiumLabel_high = 0
        elif age_label_mod == 1 or age_label_mod_high == 1 or age_label_high == 1:
            rand_int = random.randint(0,2)
            if rand_int == 0:
                premiumLabel_mod_low = 0
                premiumLabel_mod = 1
                premiumLabel_mod_high = 0
                premiumLabel_high = 0
            elif rand_int == 1:
                premiumLabel_mod_low = 0
                premiumLabel_mod = 0
                premiumLabel_mod_high = 1
                premiumLabel_high = 0
            else:
                premiumLabel_mod_low = 0
                premiumLabel_mod = 0
                premiumLabel_mod_high = 0
                premiumLabel_high = 1
        else:
            premiumLabel_mod_low = 0
            premiumLabel_mod = 0
            premiumLabel_mod_high = 0
            premiumLabel_high = 0



    # Example prediction using one of the models
        prediction1 = random_forest_model.predict([[age,premiumLabel_mod_low,premiumLabel_mod,surgeries_count,premiumLabel_mod_high,weight,age_label_high,age_label_mod,premiumLabel_high,age_label_mod_low,chronic,transplants,age_label_mod_high,cancer,age_label_mod_low]])
        prediction2 = gradient_boost_model.predict([[age,premiumLabel_mod_low,premiumLabel_mod,surgeries_count,premiumLabel_mod_high,weight,age_label_high,age_label_mod,premiumLabel_high,age_label_mod_low,chronic,transplants,age_label_mod_high,cancer,age_label_mod_low]])
        prediction3 = xgboost_model.predict([[age,premiumLabel_mod_low,premiumLabel_mod,surgeries_count,premiumLabel_mod_high,weight,age_label_high,age_label_mod,premiumLabel_high,age_label_mod_low,chronic,transplants,age_label_mod_high,cancer,age_label_mod_low]])
   
    
        mean_price=(prediction1[0]+prediction2[0]+prediction3[0])/3

        output=round(mean_price,2)

        return render_template('form.html',prediction_text="Your medical premium price is Rs. {}".format(output))
    
    return render_template("form.html")

if __name__ == '__main__':
    app.run(debug=True)
