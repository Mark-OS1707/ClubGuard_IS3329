import re

URL_PATTERN = re.compile(r"(https?://\S+|www\.\S+)", re.IGNORECASE) # Find links

def normalise_phone_number_so_it_is_the_same(number):
    return re.sub(r"\D", "", number or "") # Creating the form of phone numbers so that they are all in identical format

def find_officer_by_contact(sender, profile): # Function for comparing the sender to the club profile
    for officer_in_westeros in profile["officers"]: # A loop through all officers in westeros
        if sender.strip().lower() == officer_in_westeros["email"].lower(): # stripping to ensure no spaces where not needed and lowering to ensure in the same format
            return officer_in_westeros # If it is correct, can stop looking as we have found the officer
        if normalise_phone_number_so_it_is_the_same(sender) and normalise_phone_number_so_it_is_the_same(sender) == normalise_phone_number_so_it_is_the_same(officer_in_westeros["phone"]): # digits only
            return officer_in_westeros
    return None # the loop has finished it goes out of the if statement as no officer is found

def find_claimed_officer_from_profile(message, profile): # Text message and club profile
    text = message.lower()
    for officer_in_westeros in profile["officers"]: # A loop through all officers in westeros
        name = officer_in_westeros["first_name"].lower()  # lower the letters to lower case
        claims = [f"it's {name}", f"its {name}", f"this is {name}"]  # Phrases that would be used
        for claim in claims: # check the phrases
            if claim in text:
                return officer_in_westeros # the message claims to be from an officer
    return None # the message does not claim to be from an officer

def check_sender(message, sender, profile): # Rule 1: Is the message from the sender that it claims to be
    if not sender: # If there is no sender then nothing to check, the member left the box of the sender empty
        return []
    claimed = find_claimed_officer_from_profile(message, profile) # who the message says its from
    if claimed and find_officer_by_contact(sender, profile) is not claimed: # It claims to be from an officer however the sender is not them
        return [{ # Warning
            "rule": "sender_mismatch",
            "detail": f"The message claims to be from {claimed['name']} ({claimed['role']}), "
                      f"but '{sender}' is not their contact in the club profile.",
        }]
    return [] # No warning

def check_links(message, profile): # Do the links go to the club's official payment site.
    findings = [] # This is the list of warnings. It is empty to start and will fill up if warnings appear
    for link in URL_PATTERN.findall(message):
        domain = re.sub(r"^(https?://)?(www\.)?", "", link.lower()).split("/")[0] # Getting the link down to just the website name
        if not any(domain == d or domain.endswith("." + d) for d in profile["official_payment_domains"]): # not foireann which is the official payment site for the club
            findings.append({ # Warning
                "rule": "unofficial_link",
                "detail": f"The link '{link}' does not go to the club's official payment site.",
            })
    return findings # All link warnings that were found

def check_rules(message, profile, sender=None): # D1 interface which is the only function other parts of ClubGuard call.
    return check_sender(message, sender, profile) + check_links(message, profile)