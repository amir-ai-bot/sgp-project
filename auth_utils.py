import bcrypt

def hash_password(password):
    # Hash a password for the first time, with a randomly generated salt
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def check_password(password, hashed_password):
    # Check if the provided password matches the stored hash
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

# Example Usage
if __name__ == '__main__':
    # Simulate user registration
    user_password = "adminpass"
    hashed = hash_password(user_password)
    print(f"Original: {user_password}")
    print(f"Hashed: {hashed}")

    # Simulate login attempt
    login_password = "adminpass"
    if check_password(login_password, hashed):
        print("Login successful!")
    else:
        print("Login failed.")

    wrong_password = "wrongpass"
    if check_password(wrong_password, hashed):
        print("Login successful!")
    else:
        print("Login failed.")
