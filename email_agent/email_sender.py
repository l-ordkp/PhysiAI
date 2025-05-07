from email_agent.email_send_function import send_email
from email_agent.email_body_creator import email_body_creator
def email_sender(state):
    """
    This function sends an email based on the input provided.
    It first creates the email body using the email_body_creator function,
    and then sends the email using the send_email function.
    """
    # Create the email body
    email_body_creator(state)
    
    # Send the email
    send_email(state)
    
    return send_email(state)