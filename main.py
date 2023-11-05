import base64
import json
import aioredis
import bcrypt
from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from fastapi import FastAPI
from firebase_admin import credentials, auth, firestore
from fastapi_limiter import FastAPILimiter
from fastapi import FastAPI
import firebase_admin
from fastapi_limiter.depends import RateLimiter
from models import UserLogin, UserProfile, UserRegistration
from passwordAuth import load_email_passwords, retrieve_hashed_password, store_hashed_password
app=FastAPI(
    description="This is simple user management system",
    title="user management system",
    docs_url="/"
)

try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

#Bonus functionality : Simple rate limiting functionality 
@app.post("/register",dependencies=[Depends(RateLimiter(times=2, seconds=5))] )
async def register(user_data: UserRegistration):
    try:
        # Create the user in Firebase Authentication
        user = auth.create_user(
            email=user_data.email,
            password=user_data.password
        )
        store_hashed_password(user_data.email,user_data.password)
        
        user_data_dict = user_data.model_dump(exclude={"password"})

        # Store user data in Firestore
        user_data_dict["created_at"] = firestore.SERVER_TIMESTAMP  # Set creation timestamp
        db.collection("users").document(user.uid).set(user_data_dict)

        return {"message": "User registered successfully"}
    except Exception as e:
        return {"error": str(e)}
    
    
    
@app.post("/login")
async def login_user(user_data: UserLogin):
    try:
        # Retrieve the stored hashed password for the email
        stored_hashed_password = retrieve_hashed_password(user_data.email)
        
        if stored_hashed_password:
            # Compare the stored hashed password with the user's provided password
            if bcrypt.checkpw(user_data.password.encode('utf-8'), base64.b64decode(stored_hashed_password)):
                user = auth.get_user_by_email(user_data.email)
                custom_claims = {
                    "is_admin": False,
                }

                # Create a Firebase Auth token for the user with custom claims
                custom_token = auth.create_custom_token(user.uid, custom_claims)

                # Return the custom token as a response
                return {"custom_token": custom_token.decode()}
            else:
                return {"error": "Invalid password"}
        else:
            return {"error": "Email not found"}

    except Exception as e:
        return {"error": str(e)}

            


@app.get("/user/{email}")
async def get_user_profile(email: str):
    try:
        # Find the user by email using Firebase Authentication
        user = auth.get_user_by_email(email)
        user_id = user.uid

        user_ref = db.collection("users").document(user_id)
        user_data = user_ref.get()

        if not user_data.exists:
            raise HTTPException(status_code=404, detail="User not found")

        user_profile = user_data.to_dict()
        return user_profile

    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        return {"error": str(e)}

@app.put("/user/{email}")
async def update_user_profile(email: str, updated_profile: UserProfile):
    try:
        # Find the user by email using Firebase Authentication
        user = auth.get_user_by_email(email)
        user_id = user.uid

        user_ref = db.collection("users").document(user_id)
        user_data = user_ref.get()

        if not user_data.exists:
            raise HTTPException(status_code=404, detail="User not found")

        # Update the user's profile information (excluding the password)
        user_ref.update({
            "username": updated_profile.username,
            "email": updated_profile.email,
            "full_name": updated_profile.full_name,
        })

        return {"message": "User profile updated successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        return {"error": str(e)}

@app.delete("/user/{email}")
async def delete_user(email: str):
    try:
        # Find the user by email using Firebase Authentication
        user = auth.get_user_by_email(email)
        user_id = user.uid

        user_ref = db.collection("users").document(user_id)
        user_data = user_ref.get()

        if not user_data.exists:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user's document in Firestore
        user_ref.delete()

        # Optionally, you can also delete the user from Firebase Authentication

        return {"message": "User deleted successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        return {"error": str(e)}
    
#Bonus functionality password reset function

email_passwords_file = "hashed_email_passwords.json"
@app.put("/reset-password/{email,password}")
def reset_password(email, new_password):
    try:
        # Load existing email-password pairs from the file
        existing_email_passwords = load_email_passwords()

        # Check if the email exists in the hashed email-password pairs
        if email in existing_email_passwords:
            # hash the user's password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            hashed_password_base64 = base64.b64encode(hashed_password).decode('utf-8')

            # Update the hashed password for the user's email
            existing_email_passwords[email] = hashed_password_base64

            # Save the updated email-password pairs to the file
            with open(email_passwords_file, "w") as file:
                json.dump(existing_email_passwords, file)

            return {"message": "Password reset successful"}
        else:
            return {"error": "Email not found"}
    except Exception as e:
        print(f"Error resetting password: {str(e)}")
        return {"error": str(e)}




if __name__=="__main__":
    uvicorn.run("main:app",reload=True)