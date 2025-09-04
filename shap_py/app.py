from joblib import load
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")   # Non-GUI backend (renders to PNG)
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from joblib import load
import shap
import base64
from io import BytesIO
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/shap')
@cross_origin()
def calculate_shap():
    x_test = pd.read_csv('./final.csv')
    df = pd.read_csv('./data_test_frequency.csv')
    df.drop(columns=['Unnamed: 0'], inplace=True)
    y_test = df.iloc[:,:1]
    model = load('./model.pkl')
    row = x_test.iloc[[10]] 
    y_res = y_test.iloc[[10]]
    explainer = shap.Explainer(model.decision_function, x_test)
    shap_values = explainer(row)
    
    # AFIB
    shap.plots.waterfall(shap_values[0,:,0], max_display=10, show=False)
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close()
    buffer.seek(0)
    AFIB_img = f"data:image/png;base64,{base64.b64encode(buffer.read()).decode('utf-8')}"

    # SB
    shap.plots.waterfall(shap_values[0,:,1], max_display=10, show=False)
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close()
    buffer.seek(0)
    SB_img = f"data:image/png;base64,{base64.b64encode(buffer.read()).decode('utf-8')}"
    
    # SR
    shap.plots.waterfall(shap_values[0,:,2], max_display=10, show=False)
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close()
    buffer.seek(0)
    SR_img = f"data:image/png;base64,{base64.b64encode(buffer.read()).decode('utf-8')}"
    
    # GSVT
    shap.plots.waterfall(shap_values[0,:,3], max_display=10, show=False)
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close()
    buffer.seek(0)
    GSVT_img = f"data:image/png;base64,{base64.b64encode(buffer.read()).decode('utf-8')}"
    
    return {
        "data":{
            "AFIB_img": AFIB_img,
            "SB_img": SB_img,
            "SR_Img": SR_img,
            "GSVT_Img": GSVT_img,
        },
        "result": True,
        "status": 200
    }
