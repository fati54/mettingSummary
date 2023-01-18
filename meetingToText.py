import json
import requests
import re

def summarize_meeting():
    with open('input.txt', 'r') as file:
        transcript = file.read()
   
    # extract names of participants
    names = re.findall(r'[A-Z][a-z]+:', transcript)
    names = list(set([name.strip(':') for name in names]))
    
    with open("config.json") as config_file:
        config = json.load(config_file)
    api_key = config["openai_api_key"]

    model_engine = "text-davinci-002"
    prompt = (f"Please summarize this meeting transcript: {transcript}")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        "prompt": prompt,
        "model": model_engine,
        "max_tokens":1024
    }

    response = requests.post(
        'https://api.openai.com/v1/completions', json=data, headers=headers)

    summary = response.json()['choices'][0]['text']
    
    # Extract decisions from summary
    decisions = []
    for line in summary.splitlines():
        if "decided" in line or "agreed" in line or "approved" in line:
            decisions.append(line)
    
    # write results to output file
    with open('output.txt', 'w') as file:
        file.write('Participants: ' + ', '.join(names) + '\n\n')
        file.write('Summary: \n')
        file.write(summary + '\n\n')
        if decisions:
            file.write('Decisions: \n')
            for decision in decisions:
                file.write(decision + '\n')
        else:
            file.write('No decisions were made during this meeting.')
    print("Fin ")


def main():
    summarize_meeting()

if __name__ == '__main__':
    main()
