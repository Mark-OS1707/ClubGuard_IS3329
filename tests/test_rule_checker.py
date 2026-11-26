from club_profile.club_profile_service import get_profile
from rule_checker.checker import check_rules

# Message claims to be from Jonny but comes from an unknown number
def test_sender_unknown_is_found():
    profile = get_profile("westeros-rfc") # loading the club details so six officer names, numbers, etc
    findings = check_rules("Hello there, it's Jonny, can you buy some gift cards please?", profile, "089 555 1234")
    assert findings[0]["rule"] == "sender_mismatch" # Checks that the first finding is a sender_mismatch.

# Message claims to be from Jonny and comes from real Jonny's real number in the club profile
def test_real_officer_number_is_not_flagged():
    profile = get_profile("westeros-rfc") # loading the club details so six officer names, numbers, etc
    findings = check_rules("Hi it's Jonny, meeting is Thursday", profile, "082 252 4264")
    assert findings == []

# Link to a website that isn't Foireann which is the official payment site of the club
def test_unofficial_payment_link_is_found():
    profile = get_profile("westeros-rfc") # loading the club details so six officer names, numbers, etc
    findings = check_rules("Pay here: http://foireannn-fees.com/pay", profile) # Fake website name with a lookalike domain
    assert findings[0]["rule"] == "unofficial_link" # Checks that the first finding is an unofficial link.

# Link to the club's real Foireann page
def test_real_foireann_link_is_not_flagged():
    profile = get_profile("westeros-rfc") # loading the club details so six officer names, numbers, etc
    findings = check_rules("Pay on https://www.foireann.ie/club/westeros", profile) # real website
    assert findings == []

# Edge case when the sender box was left empty so the sender check is skipped
def test_no_sender_given_by_user_so_skips_sender_check():
    profile = get_profile("westeros-rfc") # loading the club details so six officer names, numbers, etc
    findings = check_rules("Hi it's Jonny, quick favour", profile)
    assert findings == []

# Message claims to be from Leah and comes from Leah's real email
def test_real_officer_email_is_not_flagged():
    profile = get_profile("westeros-rfc") # loading the club details so six officer names, numbers, etc
    findings = check_rules("This is Leah, the fees are due Friday", profile,
                           "leahnelsondoherty628274556@gmail.com")
    assert findings == []