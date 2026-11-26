from club_profile.club_profile_service import ClubNotFoundError, get_profile

def test_get_profile_return_the_officers_and_payment_conditions_used():
    profile = get_profile("westeros-rfc")
    assert profile["club_name"] == "Westeros RFC" # Ensure that the right club is loaded
    assert len(profile["officers"]) == 6 # Six club officers loaded
    assert "foireann.ie" in profile["official_payment_domains"] # the payment site used is foireann, not WhatsApp or random safari website
    assert "Officers never ask members to buy gift cards or vouchers." in profile["payment_rules"] # Gift-card rule

def test_unknown_club_id_raises_clear_error(): # Edge case, a club that doesnt exist gives an error not crashing
    try:
        get_profile("no-such-club") # A club that doesnt exist
        assert False, "Expected ClubNotFoundError but no error was raised"
    except ClubNotFoundError:
        pass # The correct error took place so the test passes