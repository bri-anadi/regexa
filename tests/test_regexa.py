import unittest
from regexa import Regexa

class TestRegexa(unittest.TestCase):
    def setUp(self):
        self.regexa = Regexa()

    def test_match_email(self):
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.id",
            "user123@subdomain.domain.com"
        ]
        invalid_emails = [
            "invalid.email",
            "@domain.com",
            "user@.com",
            "user@domain.",
            "user name@domain.com"
        ]

        for email in valid_emails:
            self.assertTrue(self.regexa.match_email(email))

        for email in invalid_emails:
            self.assertFalse(self.regexa.match_email(email))

    def test_match_phone_id(self):
        valid_phones = [
            "081234567890",
            "+6281234567890",
            "6281234567890"
        ]
        invalid_phones = [
            "12345",
            "+6581234567890",
            "abcdefghijk",
            "08123456"
        ]

        for phone in valid_phones:
            self.assertTrue(self.regexa.match_phone_id(phone))

        for phone in invalid_phones:
            self.assertFalse(self.regexa.match_phone_id(phone))

    def test_match_url(self):
        valid_urls = [
            "https://www.example.com",
            "http://subdomain.domain.co.id/path",
            "https://domain.com/path?param=value"
        ]
        invalid_urls = [
            "not-a-url",
            "ftp://domain.com",
            "http:/domain.com",
            "https://",
            "http://"
        ]

        for url in valid_urls:
            self.assertTrue(self.regexa.match_url(url))

        for url in invalid_urls:
            self.assertFalse(self.regexa.match_url(url))

    def test_validate_password_strength(self):
        passwords = {
            "weak123": {"expected_score": 2},
            "StrongP@ss123": {"expected_score": 5},
            "abc": {"expected_score": 1},
            "ABCDEF": {"expected_score": 1},
            "!@#$%^": {"expected_score": 1}
        }

        for password, expected in passwords.items():
            result = self.regexa.validate_password_strength(password)
            self.assertEqual(result['score'], expected['expected_score'])

    def test_extract_all(self):
        text = """
        Contact us at info@example.com or support@company.co.id
        Call +6281234567890 or 081234567891
        Visit https://www.example.com
        Follow us @username and #hashtag
        Room number 123
        """

        result = self.regexa.extract_all(text)

        self.assertEqual(len(result['emails']), 2)
        self.assertEqual(len(result['phones']), 2)
        self.assertEqual(len(result['urls']), 1)
        self.assertEqual(len(result['hashtags']), 1)
        self.assertEqual(len(result['mentions']), 1)

    def test_clean_text(self):
        text = "Hello! This is a test #123 @user"
        cleaned = self.regexa.clean_text(text)
        cleaned_no_spaces = self.regexa.clean_text(text, remove_spaces=True)

        self.assertFalse(any(char in cleaned for char in "!#@"))
        self.assertFalse(" " in cleaned_no_spaces)

    def test_extract_dates(self):
        text = """
        Dates:
        01/01/2024
        2024-01-01
        01-01-2024
        1 January 2024
        """

        results = self.regexa.extract_dates(text)
        self.assertEqual(len(results), 4)

    def test_extract_filename(self):
        paths = {
            "/path/to/file.txt": {
                "directory": "/path/to/",
                "filename": "file",
                "extension": "txt"
            },
            "document.pdf": {
                "directory": "",
                "filename": "document",
                "extension": "pdf"
            }
        }

        for path, expected in paths.items():
            result = self.regexa.extract_filename(path)
            self.assertEqual(result['directory'], expected['directory'])
            self.assertEqual(result['filename'], expected['filename'])
            self.assertEqual(result['extension'], expected['extension'])

    def test_validate_ip(self):
        ips = {
            "192.168.1.1": {"valid": True, "type": "IPv4", "private": True},
            "8.8.8.8": {"valid": True, "type": "IPv4", "private": False},
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334": {"valid": True, "type": "IPv6"},
            "invalid.ip": {"valid": False, "type": "Invalid"}
        }

        for ip, expected in ips.items():
            result = self.regexa.validate_ip(ip)
            self.assertEqual(result['is_valid'], expected['valid'])
            self.assertEqual(result['type'], expected['type'])

    def test_count_matches(self):
        text = "apple apple banana apple"
        pattern = r'apple'

        result = self.regexa.count_matches(text, pattern)
        self.assertEqual(result['count'], 3)
        self.assertEqual(len(result['positions']), 3)

    def test_validate_credit_card(self):
        cards = {
            "4111111111111111": {"valid": True, "type": "visa"},
            "5500000000000004": {"valid": True, "type": "mastercard"},
            "340000000000009": {"valid": True, "type": "amex"},
            "6011000000000004": {"valid": True, "type": "discover"},
            "1234567890": {"valid": False, "type": None}
        }

        for number, expected in cards.items():
            result = self.regexa.validate_credit_card(number)
            self.assertEqual(result['is_valid'], expected['valid'])
            self.assertEqual(result['card_type'], expected['type'])

if __name__ == '__main__':
    unittest.main()
