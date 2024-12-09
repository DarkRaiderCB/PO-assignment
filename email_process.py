from classifier import *
from summarizer import *
from parser import *

def process_email(email):

    #Classification
    label = classify_email(email['subject'], email['body'], email['attachments'])

    #Summarization
    summary = summarizer(email['subject'], email['body'], email['attachments'])
    # Combine everything for display
    parsed_data = {
        "label": label,
        "summary": summary
    }
    return parsed_data
