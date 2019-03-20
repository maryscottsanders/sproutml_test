from processor import clean_features, label_encode
from embedding_modeler import EmbeddingModeler
from prediction_modeler import PredictionModeler
from versioning import model_path
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

class TopicModeler:
    """Create model to predict labels for text data
    """
    def train_test_pipeline(self, input_data_file):
        """Create model to predict labels for text data

        Arguments:
            input_data_file {df} -- text with labels
        """
        # Loading data
        print('Reading csv')
        df = pd.read_csv(input_data_file, usecols=['features', 'response'])

        # Cleaning the text
        print('Cleaning text')
        df = clean_features(df)
        df, encoder = label_encode(df, 'response')
        joblib.dump(encoder, model_path('encoder'))

        # Test Train Splitting
        print('Train,test,split')
        train_df, test_df = train_test_split(df,
                                             test_size=.3,
                                             random_state=42)

        # Fitting embedding model to train_tagged_docs
        print('Doc2vec modeling')
        embedding = EmbeddingModeler()
        model, y_train, x_train, y_test, x_test = embedding.doc2vec_pipeline(train_df, test_df)
        joblib.dump(model, model_path('embedding'))

        # Fit and predict using logistic regression
        print('Fitting LR')
        lr = PredictionModeler()
        prediction_model = lr.fit_predict_lr(x_train=x_train,
                                                       y_train=y_train,
                                                       x_test=x_test,
                                                       y_test=y_test)
        joblib.dump(prediction_model, model_path('prediction'))

input_data_file = '../customer_complaints_topic_clean.csv'
modeler = TopicModeler()
modeler.train_test_pipeline(input_data_file)
