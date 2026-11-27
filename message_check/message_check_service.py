from club_profile.club_profile_service import get_profile
from rule_checker.checker import check_rules
from ai_analyzer.analyzer import analyse

def check_message(message, sender, club_id, llm = None):
    profile = get_profile(club_id) # Getting the club details for Westeros
    findings = check_rules(message, profile, sender) # Runs the checkers of who the sender is and the link of the sending
    ai_result = analyse(message, profile, findings, llm = llm) # Ai analyse's providing the message, profile and the findings
    return {"risk": ai_result["risk"], # Returns the combined result of risk, reasons and findings
        "reasons": ai_result["reasons"],
        "findings": findings,}