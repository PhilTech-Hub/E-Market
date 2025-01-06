import paypalrestsdk

paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": "AUBXs4963ONtWTAbguFOZza5StYOqzOjbcFYzf50wbKnLdQ7c-mvIrzY4ylPpUc-sRlVaCVp7kcswM4-",  # Replace with the client ID from your PayPal app
    "client_secret": "EH3PbhbGgZ3XnADIjVfnrK9kJb1ANDY8EzK1jNvcy6qwhBAgz-mOP-L-xOJwjUYZw_7OuAu4tdvAe3-e",  # Replace with the secret from your PayPal app
    "log": True  # Enables logging for troubleshooting
})
