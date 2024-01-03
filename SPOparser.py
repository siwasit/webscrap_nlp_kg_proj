import spacy
nlp = spacy.load('en_core_web_sm')

def extract_spo(sentence):
    # Process the sentence using SpaCy
    doc = nlp(sentence)

    # Initialize variables to store Subject, Predicate, and Object
    subject = ""
    predicate = ""
    obj = ""

    # Iterate through the tokens in the sentence
    for token in doc:
        # Check if the token is a subject (nsubj) or a passive subject (nsubjpass)
        if "subj" in token.dep_:
            subject = token.text

        # Check if the token is a predicate (ROOT)
        elif "ROOT" in token.dep_:
            predicate = token.text

        # Check if the token is an object (dobj)
        elif "obj" in token.dep_:
            obj = token.text

    # Return the extracted SPO triple
    return subject, predicate, obj