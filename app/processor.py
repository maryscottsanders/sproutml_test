import regex as re
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import remove_stopwords
import nltk
from nltk.stem import WordNetLemmatizer, SnowballStemmer
nltk.download('wordnet')
from sklearn.preprocessing import LabelEncoder


def lemmatize_stemming(doc):
    """Lemmatize and stem documents
    
    Arguments:
        doc {string} -- text document
    
    Returns:
        string-- string of lemmatized and stemmed words for each document
    """

    stemmer = SnowballStemmer("english")
    return stemmer.stem(WordNetLemmatizer().lemmatize(doc, pos='v'))


def reg_ex(doc):
    """Clean punctuation, url, series of x's(phone numbers), series of spaces, and anything else that is not a letter
    
    Arguments:
        doc {string} -- text document
    
    Returns:
        string -- processed text document
    """
    reg_punctuation = r'[\!"#$%&\*+,-./:;<=>?@^_`()|~=]'
    reg_url = r'https?://[A-Za-z0-9./]+'
    reg_x_series = r'x+'
    reg_nonletters = r'[^a-zA-Z]'
    reg_spaces = r'\s+'
    all_pats = r'|'.join((reg_punctuation,
                          reg_url,
                          reg_x_series,
                          reg_nonletters))
    stripped = re.sub(all_pats, ' ', doc)
    stripped_spaces = re.sub(reg_spaces, ' ', stripped)
    return stripped_spaces


def process_doc(doc, steps):
    """Apply process steps and convert documents to list of string
    
    Arguments:
        doc {string} -- text documents
        steps {functions} -- list of processing functions
    
    Returns:
        list -- list of strings
    """
    data = doc
    for step in steps:
        data = step(data)
    return data


PROCESS_STEPS = [lemmatize_stemming,
                 reg_ex,
                 remove_stopwords,
                 simple_preprocess]


def clean_features(df):
    """Applies process function to each document in dataframe
    
    Arguments:
        df {df} -- dataframe of text documents and labels
    
    Returns:
        df -- dataframe of processed documents
    """
    df['features'] = df.apply(lambda r: process_doc(
        r['features'], PROCESS_STEPS), axis=1)
    return df


def label_encode(df, column):
    """Create encoded labels from string labels
    
    Arguments:
        df {df} -- dataframe of documents and labels
        column {series} -- label column
    
    Returns:
        df -- dataframe with label encoded labels
        encoder -- encoding of labels
    """
    encoder = LabelEncoder()
    df[column] = encoder.fit_transform(df[column])
    return df, encoder
