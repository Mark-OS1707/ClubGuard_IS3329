from message_check.message_check_service import check_message
from ai_analyzer.llm_client import Mock

# The rule checker's findings and the AI's result are combined into one result
def test_findings_and_ai_result_are_combined():
    ai = Mock(reply='{"risk": "HIGH", "reasons": ["Jonny would not ask members for gift cards"]}') # Mock AI says high with a reason behind the high result
    result = check_message("Hi it's Jonny, can you buy some gift cards please?", "089 555 1234", "westeros-rfc", llm=ai) # Message claims to be from Jonny however it is from an unknown number
    assert result["risk"] == "HIGH" # Checks AI's risk level is in the result
    assert result["reasons"] == ["Jonny would not ask members for gift cards"] # Checks AI's reason is in the result
    assert result["findings"][0]["rule"] == "sender_mismatch" # Checks the rule checker's finding is in the result

# A genuine message from the real officer has no findings and keeps the AI's result
def test_genuine_message_has_no_findings():
    ai = Mock(reply='{"risk": "LOW", "reasons": ["This is Jonnys real number and nothing is been asked for"]}') # Mock AI says low with a reason behind the low result
    result = check_message("Hi there, it's Jonny. I am letting you know the meeting is Thursday", "082 252 4264", "westeros-rfc", llm=ai) # Message from Jonny's real number in the club profile
    assert result["risk"] == "LOW" # Checks the AI's risk level is in the result
    assert result["findings"] == [] # Checks there are no warnings from the rule checker