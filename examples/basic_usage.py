from regexa import Regexa

def main():
    regex = Regexa()

    # Test email validation
    email = "test@example.com"
    print(f"Email validation: {regex.match_email(email)}")

    # Test password strength
    password = "MyStr0ng!Pass"
    result = regex.validate_password_strength(password)
    print(f"Password strength: {result['strength']}")

    # Test text extraction
    text = "Contact us at support@example.com or call +6281234567890"
    extracted = regex.extract_all(text)
    print(f"Extracted data: {extracted}")

if __name__ == "__main__":
    main()
