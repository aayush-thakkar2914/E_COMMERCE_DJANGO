# E_comm/email_utils.py

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_order_status_email(order, previous_status=None):
    """
    Send email notification to user based on order status
    
    Args:
        order: The Order instance
        previous_status: The previous status (to avoid sending duplicate emails)
    """
    # Don't send email if status hasn't changed
    if previous_status and previous_status == order.status:
        return
    
    # Get user's email
    user_email = order.user.email
    
    # Define email subject and template based on order status
    status_email_map = {
        'PLACED': {
            'subject': 'Your Order Has Been Placed Successfully!',
            'template': 'E_comm/email/order_placed_email.html',
        },
        'ACCEPTED': {
            'subject': 'Good News! Your Order Has Been Accepted',
            'template': 'E_comm/email/order_accepted_email.html',
        },
        'SHIPPED': {
            'subject': 'Your Order Has Been Shipped',
            'template': 'E_comm/email/order_shipped_email.html',
        },
        'CITY': {
            'subject': 'Your Order Has Arrived in Your City',
            'template': 'E_comm/email/order_arrived_city_email.html',
        },
        'DELIVERED': {
            'subject': 'Your Order Has Been Successfully Delivered',
            'template': 'E_comm/email/order_delivered_email.html',
        }
    }
    
    # Get email details based on current status
    email_details = status_email_map.get(order.status)
    if not email_details:
        return
    
    subject = email_details['subject']
    template = email_details['template']
    
    # Context for the email template
    context = {
        'user': order.user,
        'order': order,
        'order_items': order.order_items.all(),
        'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else '',
    }
    
    # Render HTML content
    html_content = render_to_string(template, context)
    
    # Create plain text version
    text_content = strip_tags(html_content)
    
    # Create email message
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email]
    )
    
    # Attach HTML content
    email.attach_alternative(html_content, "text/html")
    
    # Send email
    email.send()
    
    return True