from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

def modify_the_label(label):
    if(label==0):
        return 'Bundle Branch Block'
    elif(label==1):
        return 'Cardiomyopathy'
    elif(label==2):
        return 'Dysrhythmia'
    elif(label==3):
        return 'Healthy Controls'
    elif(label==4):
        return 'Myocardial Infarction'
    elif(label==5):
        return 'Nan'
    else:
        return 'none'

app = Flask(__name__)

# Load saved model
# model = load_model('patchSize8')
model = load_model('Model8PatchSize')

# Define a route to the home page
@app.route('/')
def home():
    return render_template('../index.html')

# Define a route for file upload
@app.route('/letiecgclassifier/upload/', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        
        # Get uploaded file
        file = request.files['file']
        
        # Read data from file
        data = pd.read_csv(file, header=None)
        data = data.apply(pd.to_numeric, errors='coerce').values
        data = data.astype(float) # convert data to float
        data = data.reshape(1, -1)  # Reshape to match model input shape
        
        # Predict class of object
        class_probabilities = model.predict(data)
        predicted_class = np.argmax(class_probabilities)
        
        # modify the label:
        new_predicted_class = modify_the_label(predicted_class)
        

        # Return the result
        return f"The predicted class is {new_predicted_class}"
        return render_template('result.html', predicted_class=new_predicted_class)

if __name__ == '__main__':
    app.run(debug=True)
