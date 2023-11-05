import json
import bcrypt
import base64

# File path to store the hashed email-password pairs
email_passwords_file = "hashed_email_passwords.json"

def store_hashed_password(email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password_base64 = base64.b64encode(hashed_password).decode('utf-8')
    
    try:
        # Load existing email-password pairs from the file (if any)
        existing_email_passwords = load_email_passwords()

        # Update or add the new email-password pair
        existing_email_passwords[email] = hashed_password_base64

        # Save the updated email-password pairs to the file
        with open(email_passwords_file, "w") as file:
            json.dump(existing_email_passwords, file)

        return True
    except Exception as e:
        print(f"Error storing hashed password: {str(e)}")
        return False

def load_email_passwords():
    try:
        # Try to load existing email-password pairs from the file
        with open(email_passwords_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist yet, return an empty dictionary
        return {}
    except Exception as e:
        print(f"Error loading email-password pairs: {str(e)}")
        return {}

def retrieve_hashed_password(email):
    try:
        # Load existing email-password pairs from the file (if any)
        existing_email_passwords = load_email_passwords()

        # Retrieve the hashed password for the email
        return existing_email_passwords.get(email)
    except Exception as e:
        print(f"Error retrieving hashed password: {str(e)}")
        return None

def load_email_passwords():
    try:
        # Try to load existing email-password pairs from the file
        with open(email_passwords_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist yet, return an empty dictionary
        return {}
    except Exception as e:
        print(f"Error loading email-password pairs: {str(e)}")
        return {}

# # Example of using the store_hashed_password and retrieve_hashed_password functions
# user_email = "example@example.com"
# hashed_password = bcrypt.hashpw("example_password".encode('utf-8'), bcrypt.gensalt())

# # Store the hashed password for the user's email
# store_hashed_password(user_email, hashed_password)

# # Retrieve the hashed password for a user's email
# retrieved_hashed_password = retrieve_hashed_password(user_email)

# # Check if the retrieved hashed password matches the expected hashed password
# if retrieved_hashed_password == hashed_password:
#     print("Password match")
# else:
#     print("Password doesn't match")
