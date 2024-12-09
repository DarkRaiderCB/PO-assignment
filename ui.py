import streamlit as st
import imaplib
import email
import os
from email.header import decode_header
from email_process import process_email  # Assuming you have the `process_email` function


def connect_email(username, password, imap_url='imap.gmail.com'):
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        return mail
    except Exception as e:
        st.error(f"Failed to connect: {e}")
        return None

def fetch_emails(mail, folder='INBOX'):
    try:
        mail.select(folder)
        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()
        
        fetched_emails = []

        for email_id in email_ids:
            res, msg = mail.fetch(email_id, "(RFC822)")
            for response_part in msg:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # Extract subject
                    subject = msg["Subject"]

                    # Extract email body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    # Extract attachments
                    attachments = []
                    for part in msg.walk():
                        if part.get_content_disposition() == "attachment":
                            filename = part.get_filename()
                            if filename:
                                attachments.append({"filename": filename, "content": part.get_payload(decode=True)})

                    fetched_emails.append({
                        "subject": subject,
                        "body": body,
                        "attachments": attachments
                    })
        return fetched_emails
    except Exception as e:
        st.error(f"Failed to fetch emails: {e}")
        return []

def save_attachments(email_data, folder="attachments"):
    os.makedirs(folder, exist_ok=True)
    saved_files = []
    for attachment in email_data.get("attachments", []):  # Ensure it checks only current email
        file_path = os.path.join(folder, attachment["filename"])
        with open(file_path, "wb") as f:
            f.write(attachment["content"])
        saved_files.append(file_path)
    return saved_files


# Streamlit UI
st.title("Email Summarizer")

# Email login inputs
email_user = st.text_input("Email Address")
email_pass = st.text_input("App Password", type="password")

if st.button("Fetch Emails"):
    if email_user and email_pass:
        mail = connect_email(email_user, email_pass)
        if mail:
            with st.spinner("Fetching unread emails..."):
                emails = fetch_emails(mail)
                mail.logout()

            if emails:
                for idx, email_data in enumerate(emails, start=1):
                    st.subheader(f"Email {idx}")
                    st.write(f"**Subject:** {email_data['subject']}")
                    st.write(f"**Body:** {email_data['body']}")

                    # Save attachments for the current email
                    saved_files = save_attachments(email_data)  # Reset for each email

                    if saved_files:
                        st.write("**Attachments:**")
                        for file in saved_files:
                            st.write(f"- {file}")
                    else:
                        st.write("No attachments found.")

                    # Process the email (using the imported `process_email` function)
                    result = process_email({
                        "subject": email_data['subject'],
                        "body": email_data['body'],
                        "attachments": saved_files,  # Use attachments specific to this email
                    })

                    st.write(f"**Label:** {result['label']}")
                    st.write(f"**Summary:** {result['summary']}")
                    st.write("-" * 50)



            else:
                st.info("No unread emails found.")
    else:
        st.error("Please enter both email and password.")
