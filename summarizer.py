from together import Together
from parser import *
from dotenv import load_dotenv
import os

load_dotenv()

# Together API Summarizer
def summarizer(subject, body, attachment_path=[]):
    client = Together(api_key=os.getenv("API_KEY"))
    sys_prompt="""Summarize the following email and attachments. Provide a precise summary and NOTHING ELSE.
    If attachment present then consider it, else ignore it.
    Also answer the following questions, if data about them is present in that specific email/attachment, else leave blank.
        "Customer PO Number": "What is the Customer PO Number?",
        "Customer Name": "What is the Customer Name?",
        "Item Name": "What is the Item Name?",
        "Quantity": "What is the Quantity?",
        "Rate per unit": "What is the Rate per unit?",
        "Unit of measurement": "What is the Unit of measurement?",
        "Item wise Delivery Dates": "What are the Item wise Delivery Dates?",
        "Applicable Taxes": "What are the Applicable Taxes?",
        "Terms of Payment": "What are the Terms of Payment?"
    """
    attachment_content = ""
    for attachment in attachment_path:
        if attachment.endswith(('.pdf', '.xlsx', '.docx', '.jpeg', '.csv')):
            attachment_content = extract_attachment(attachment)
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"Subject:{subject}\nBody:{body}\nAttachment:{attachment_content}"}
        ],
        max_tokens=None,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>","<|eom_id|>"],
        stream=True
    )
    result = ""
    for token in response:
        if hasattr(token, "choices"):
            delta_content = token.choices[0].delta.content
            result += delta_content
    return result
