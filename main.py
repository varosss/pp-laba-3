from string import ascii_letters, digits
from bs4 import BeautifulSoup

class EmailRegex:
    def __init__(self):
        self.local_char_set = set()
        self.domain_char_set = set()

        local_chars = ascii_letters + digits + "!#$%&’r;+-.=?^^_`{}|~"
        domain_chars = ascii_letters + digits + ".-"

        self.__allow_chars(self.local_char_set, local_chars)
        self.__allow_chars(self.domain_char_set, domain_chars)

    def __allow_chars(self, char_set, chars):
        for char in chars:
            char_set.add(char)

    def get_emails_from_html_file(self, filename):
        file = open(filename, "r")
        data = file.read()

        return self.get_emails_from_html(data)

    def get_emails_from_html(self, data):
        soup = BeautifulSoup(data)
        string = soup.get_text("\n")

        return self.get_emails_from_str(string)

    def get_emails_from_str(self, string):
        email_addresses = []
        n = len(string)

        MAX_LOCAL_LEN = 64
        MAX_DOMAIN_LEN = 253
        MAX_ADDRESS_LEN = 256

        l = 0
        r = 0

        while l < n:
            address = {"local": "", "@": False, "domain": ""}

            key = "local"
            char_set = self.local_char_set

            while r < n:
                if string[r] == "@" and address["@"]:
                    break

                if string[r] == "@" and not address["@"]:
                    address["@"] = True
                    key = "domain"
                    char_set = self.domain_char_set

                if string[r] in char_set:
                    address[key] += string[r]
                elif string[r] != "@":
                    break

                if len(address["local"]) == MAX_LOCAL_LEN:
                    break

                if len(address["domain"]) == MAX_DOMAIN_LEN:
                    break

                if len(address["local"]) + len(address["domain"]) == MAX_ADDRESS_LEN:
                    break

                r += 1

            if len(address["local"]) > 0 and len(address["domain"]) > 0 and "" not in address["domain"].split(".") and address["domain"][-1] != "-":
                email_addresses.append(string[l: r])

            r += 1
            l = r

        return email_addresses