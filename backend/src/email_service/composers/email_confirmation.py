from email.message import EmailMessage


def confirmation_email(user_name: str, confirmation_link: str) -> EmailMessage:
    body = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Confirmation</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            color: #333;
            margin: 0;
            padding: 0;
        }}
        .email-container {{
            width: 100%;
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        h1 {{
            color: #1a73e8;
        }}
        .content {{
            font-size: 16px;
            line-height: 1.5;
            margin-bottom: 20px;
        }}
        .content a {{
            color: #1a73e8;
            text-decoration: none;
        }}
        .button {{
            display: inline-block;
            background-color: #4CAF50;
            color: #fff;
            padding: 12px 30px;
            text-align: center;
            border-radius: 5px;
            text-decoration: none;
            font-size: 16px;
            font-weight: bold;
            margin-top: 20;
        }}
        .button:hover {{
            background-color: #45a049;
        }}
        .footer {{
            text-align: center;
            font-size: 14px;
            color: #888;
        }}
        .footer a {{
            color: #888;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>Confirm Your Email Address</h1>
        </div>
        <div class="content">
            <p>Hello <strong>{user_name}</strong>,</p>
            <p>Thank you for signing up with us! To complete your registration and verify your email address, please click the button below:</p>
            <a href="{confirmation_link}" class="button">Confirm My Email</a>
            <p>If you did not request this, please ignore this email.</p>
        </div>
        <div class="footer">
            <p>Best regards,</p>
            <p>The LifeGrid</p>
        </div>
    </div>
</body>
</html>
    """
    msg = EmailMessage()
    msg.set_content(body, subtype='html')
    return msg
