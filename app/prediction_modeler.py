from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn import utils


class PredictionModeler:
    """Input doc2vec embeddings and create logistic regression model
    
    Returns:
        logistic_model -- trained logistic regression model
        accuracy -- accuracy score of model
    """
    def fit_predict_lr(self, x_train, y_train, x_test, y_test, random_state=42, C=1e5):
        """Input doc2vec embeddings and create logistic regression model
        
        Arguments:
            x_train {series} -- list of document vectors
            y_train {series} -- list of tags
            x_test {series} -- list of document vectors
            y_test {series} -- list of tags
        
        Keyword Arguments:
            random_state {int} -- set random state (default: {42})
            C {float} -- inverse of regular strength (default: {1e5})
        
        Returns:
            logistic_model -- trained logistic regression model
            accuracy -- accuracy score of model
        """
        print('Training Logistic Regression model...')
        logistic_model = LogisticRegression(C=C, random_state=random_state)
        logistic_model.fit(x_train, y_train)

        print('Making Prediction...')
        y_pred = logistic_model.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        accuracy_percent = round(accuracy*100, 2)
        print('Prediction Accuracy:' + str(accuracy_percent) + ' %')
        return logistic_model, accuracy
