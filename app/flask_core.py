
"""
Start Date: 22 January 2019
Project: AWS NLP Pipeline
"""

from flask import Flask, request, jsonify
import joblib
from processor import clean_features
from versioning import model_version
import pandas as pd
from gensim.models import Doc2Vec


app = Flask(__name__)
embedding_model = joblib.load(model_version('embedding'))
prediction_model = joblib.load(model_version('prediction'))
label_encoder = joblib.load(model_version('encoder'))


@app.route('/predict-ui', methods=['GET', 'POST'])
def pred_ui():
    """Predict label for new string in flask app

    Returns:
      webpage -- webpage to input new string and return predicted label
    """
    if request.method == 'POST':
        req_text = request.form.get('text')
        # Use processing file to process a single document
        req_text = [req_text]
        req_df = pd.DataFrame(req_text, columns=['features'])
        proc_text = clean_features(req_df)
        proc_text = proc_text.features[0]
        # Infer vector intakes a list of strings (words)
        vec_text = embedding_model.infer_vector(proc_text)
        vec_text = vec_text.reshape(1, -1)
        num_pred = prediction_model.predict(vec_text)
        word_pred = label_encoder.inverse_transform(num_pred)

        return '''<p><font face="arial"> <h2>The predicted topic was "{}."</h2> <p> After processing, the text looked like this:<p> {}<p> Those "tokens" are what helped inform the prediction. </font>'''.\
            format(word_pred, proc_text)

    return '''<form method="POST">
                <h2><font face="arial">
                  Input Text Here <input type="text" name="text"><br>
                  <input type="submit" value="Submit"><br>
                </font>
              </form></h2>'''


if __name__ == '__main__':
    app.run(debug=True)
