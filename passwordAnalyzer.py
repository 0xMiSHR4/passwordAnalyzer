# Importing string module to access ASCII characters
import string

# Importing random module to generate random characters for strong password
import random

# Importing the getpass module to hide password input
import getpass  

def generate_strong_password(length):
    # Define characters for strong password generation
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate a strong password of specified length
    strong_password = ''.join(random.choice(characters) for _ in range(length))
    return strong_password

def analyze_password(password):
    # Defining criteria for a strong password
    length_criteria = 8  # Minimum length of the password
    uppercase_criteria = 1  # Minimum number of uppercase letters
    lowercase_criteria = 1  # Minimum number of lowercase letters
    digit_criteria = 1  # Minimum number of digits
    special_character_criteria = 1  # Minimum number of special characters

    suggestions = []  # Initializing list to store suggestions

    # Checking length of the password
    if len(password) < length_criteria:
        suggestions.append("Your password is too short. It may be easy to guess or crack.")

    # Checking uppercase letters
    if not any(char.isupper() for char in password):
        suggestions.append("Consider adding at least one uppercase letter to make your password stronger.")

    # Checking lowercase letters
    if not any(char.islower() for char in password):
        suggestions.append("Consider adding at least one lowercase letter to make your password stronger.")

    # Checking digits
    if not any(char.isdigit() for char in password):
        suggestions.append("Consider adding at least one digit to make your password stronger.")

    # Checking special characters
    if not any(char in string.punctuation for char in password):
        suggestions.append("Consider adding at least one special character to make your password stronger.")

    # Determining password strength
    if len(suggestions) == 0:
        return "Strong", suggestions
    elif len(suggestions) == 1:
        return "Weak", suggestions
    else:
        return "Very Weak", suggestions

password = getpass.getpass("Enter your password: ")  # Prompting user to input password securely
strength, suggestions = analyze_password(password)  # Analyzing password strength

print("Password strength:", strength)  # Printing password strength
if suggestions:
    print("Suggestions to improve your password:")  # Printing suggestions, if any
    for suggestion in suggestions:
        print("- " + suggestion)  # Printing each suggestion

# Prompt user for suggested strong password
prompt = input("Do you want a suggested strong password? (Y/N): ")
if prompt.lower() == 'y':
    print("Here's a suggested strong password:", generate_strong_password(12))  # Generate a strong password of length 12
elif prompt.lower() == 'n':
    print("Alright, keep your password secure!")
else:
    print("Invalid input. Remember to keep your password secure.")