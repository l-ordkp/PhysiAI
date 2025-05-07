import imaplib
import email
from dotenv import load_dotenv
import os
load_dotenv()
from email.header import decode_header


def get_unread_emails():
    # Connect to Gmail's IMAP server
    username = os.getenv("EMAIL")
    app_password = os.getenv("APP_PASSWORD")

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, app_password)
    mail.select('inbox')
    
    # Search for unread emails
    result, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()
    
    unread_count = len(email_ids)
    print(f"Found {unread_count} unread emails")
    
    unread_emails = []
    
    for e_id in email_ids:
        # Fetch the email
        result, data = mail.fetch(e_id, '(RFC822)')
        
        for response_part in data:
            if isinstance(response_part, tuple):
                # Parse the email content - CORRECTED LINE
                msg = email.message_from_bytes(response_part[1])
                
                # Decode the email subject
                subject = "No Subject"
                if msg["Subject"]:
                    subject_header = decode_header(msg["Subject"])[0]
                    subject = subject_header[0]
                    encoding = subject_header[1]
                    if isinstance(subject, bytes) and encoding:
                        subject = subject.decode(encoding)
                    elif isinstance(subject, bytes):
                        subject = subject.decode('utf-8', errors='replace')
                
                # Get sender
                from_ = "Unknown Sender"
                if msg.get("From"):
                    from_header = decode_header(msg.get("From"))[0]
                    from_ = from_header[0]
                    encoding = from_header[1]
                    if isinstance(from_, bytes) and encoding:
                        from_ = from_.decode(encoding)
                    elif isinstance(from_, bytes):
                        from_ = from_.decode('utf-8', errors='replace')
                
                # Get date
                date = msg.get("Date", "No Date")
                
                # Get body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        
                        if "attachment" not in content_disposition:
                            if content_type == "text/plain":
                                try:
                                    payload = part.get_payload(decode=True)
                                    if payload:
                                        charset = part.get_content_charset() or 'utf-8'
                                        body = payload.decode(charset, errors='replace')
                                        break
                                except Exception as e:
                                    print(f"Error decoding email body: {e}")
                else:
                    try:
                        payload = msg.get_payload(decode=True)
                        if payload:
                            charset = msg.get_content_charset() or 'utf-8'
                            body = payload.decode(charset, errors='replace')
                    except Exception as e:
                        print(f"Error decoding email body: {e}")
                
                unread_emails.append({
                    'id': e_id.decode() if isinstance(e_id, bytes) else str(e_id),
                    'sender': from_,
                    'subject': subject,
                    'date': date,
                    'body': body
                })
    
    mail.close()
    mail.logout()
    
    return unread_count, unread_emails


