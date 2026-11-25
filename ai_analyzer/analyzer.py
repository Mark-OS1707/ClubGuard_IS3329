import json
from pathlib import Path
from ai_analyzer.llm_client import load_config, create_llm_client

analyser_folder = Path(__file__).parent  # The ai_analyzer folder this is where prompt.txt is

class Bad_response_from_the_AI(Exception):  # CReates an error when the AI answer is in the incorrect format
    pass

def build_prompt(message, profile, findings, config):  # Fills in the blanks in prompt.txt file
    with open(analyser_folder / config["prompt_file"], encoding="utf-8") as f: # Opening it
        prompt = f.read() # reads all the text from prompt.txt into prompt

    officers = "" # Empty currently before the for loop
    for officer in profile["officers"]: # Looping through each officer in the club
        officers += f"- {officer['name']}, {officer['role']}, {officer['phone']}, {officer['email']}\n" # Adds for the officer

    payment_rules = "" # Empty currently before the for loop
    for rule in profile["payment_rules"]: # Looping through each payment rule in the club
        payment_rules += f"- {rule}\n" # Adding

    findings_text = "" # Empty currently before the for loop
    for finding in findings: # Looking at the details of the rule check
        findings_text += f"- {finding['detail']}\n"
    if not findings:
        findings_text = "None" # Rule checker found nothing

    prompt = prompt.replace("{club_name}", profile["club_name"]) # replacing the club name in the template with Westeros
    prompt = prompt.replace("{officers}", officers) # Swapping officers
    prompt = prompt.replace("{payment_rules}", payment_rules) # Swapping payment rules
    prompt = prompt.replace("{payment_domains}", ", ".join(profile["official_payment_domains"])) # Swapping payment domains
    prompt = prompt.replace("{findings}", findings_text) # Swapping findings
    prompt = prompt.replace("{message}", message) # Swapping message. It is done last so text in the message can't fill the other blanks
    return prompt # Now the prompt is ready to send to AI with the right details

def parse_reply(reply):  # Checks that the AI's reply is in the right format
    try:
        data = json.loads(reply)
    except json.JSONDecodeError:
        raise Bad_response_from_the_AI("The AI reply was not valid JSON.") # Incorrect format

    if not isinstance(data, dict):
        raise Bad_response_from_the_AI("The AI reply was not in the expected format.") # Incorrect format

    risk = str(data.get("risk", "")).upper() # risks
    if risk not in ["LOW", "MEDIUM", "HIGH"]: # If the risk isn't in one of the three levels of risk its rejected
        raise Bad_response_from_the_AI(f"The AI gave an unknown risk level: '{data.get('risk')}'.")

    reasons = data.get("reasons") # reasons
    if not isinstance(reasons, list) or len(reasons) == 0:
        raise Bad_response_from_the_AI("The AI gave no reasons.") # No reason is not valid

    return {"risk": risk, "reasons": reasons} # Everything correct return it correctly

def analyse(message, profile, findings, llm=None):
    config = load_config() # Reads from the config file
    if llm is None:
        llm = create_llm_client(config)
    prompt = build_prompt(message, profile, findings, config) # Fills in the prompt template
    reply = llm.ask(prompt) # AI question
    return parse_reply(reply) # Gives back the risk level and reasons behind it