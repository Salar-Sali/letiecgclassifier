from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import tkinter as tk

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
    return render_template('index.html')

# Define a route for file upload
@app.route('/upload', methods=['POST'])
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
        
        # show the results-start:
        root = tk.Tk()
        window_width = 600
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_pos = int((screen_width - window_width) / 2)
        y_pos = int((screen_height - window_height) / 2)
        root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
        result_label = tk.Label(root, font=('Arial', 20), anchor='center')
        result_label.configure(text=f'The predicted class is {new_predicted_class}')
        result_label.pack(expand=True, fill='both')
        root.mainloop()
        # show the results-end

        # Return the result
        return f"The predicted class is {new_predicted_class}"

if __name__ == '__main__':
    app.run(debug=True)
