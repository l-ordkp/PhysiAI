from email_agent.get_unread_emails import get_unread_emails
from email_agent.summariser import summarise_email

def unread_email_summariser(state):
    """
    This function retrieves unread emails and summarizes them.
    It returns a list of dictionaries containing the email ID and its summary.
    """
    # Get unread emails
    unread_count, emails = get_unread_emails()
    email_summaries = []
    
    # Summarise each unread email
    for i, email_data in enumerate(emails, 1):
        print(f"Summarizing email {i} of {unread_count}...")
        summary = summarise_email(email_data)
        email_summaries.append(summary)

    state["result"] = str(email_summaries)
    return state