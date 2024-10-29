import os

from openai import OpenAI

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key= OPENAI_API_KEY)

def generate_text(prompt, max_tokens=4000):
    response = client.chat.completions.create(
        model="gpt-4o",  # Du kan ändra till den modell du vill använda, t.ex. "gpt-4" om tillgängligt.
        messages=[
            {"role": "system", "content": "You are a helpful assistant, talk with the user in down to earth plain english."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        n=1,
        temperature=0.7,
    )
    return response.choices[0].message.content

def generate_summary(transcript):
    prompt = f"Sammanfatta följande podcastavsnitt kort på svenska. Avsnittet är från podcasten Datastudion och följer Data Daos personlighet: commited, daring, active, down to earth samt reliable.\n\nTranskription:\n{transcript}\n\nSammanfattning:"
    return generate_text(prompt)

def generate_slack_post(transcript):
    prompt = f"Write a short Slack message in English to promote this podcast episode internally. The podcast is from Datastudion and follows Data Dao's personality: commited, daring, active, down to earth, and reliable. End the message with a call to action asking to give the podcast a 5-star rating.\n\nTranscript:\n{transcript}\n\nSlack Post:"
    return generate_text(prompt) 

def generate_linkedin_post(transcript, version="1"):
    if version == "1":
        hook = "Get ready for a mind-blowing discussion!"
    elif version == "2":
        hook = "Missed our latest episode? Here's why you need to listen!"
    else:
        hook = "One last chance to catch our insightful episode!"
    
    prompt = f"Write a LinkedIn post in English with the hook: '{hook}'. Follow the hook with an insight from the following podcast transcript. The post should follow Data Dao's personality: commited, daring, active, down to earth, and reliable. Mention that the link is in the comments.\n\nTranscript:\n{transcript}\n\nLinkedIn Post:"
    return generate_text(prompt)

def process_transcription(transcript):
    summary = generate_summary(transcript)
    slack_post = generate_slack_post(transcript)
    linkedin_post_1 = generate_linkedin_post(transcript, version="1")
    linkedin_post_2 = generate_linkedin_post(transcript, version="2")
    linkedin_post_3 = generate_linkedin_post(transcript, version="3")

    return summary, slack_post, linkedin_post_1, linkedin_post_2, linkedin_post_3

def read_transcript_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            transcript = file.read()
        return transcript
    except FileNotFoundError:
        print(f"Filen {file_path} hittades inte.")
        return None

# Exempel på hur du kan använda funktionen
if __name__ == "__main__":
    # Sätt filvägen till din lokala transkriptionsfil
    file_path = "transcript.txt"
    transcript = read_transcript_from_file(file_path)
    
    if transcript:
        summary, slack_post, linkedin_post_1, linkedin_post_2, linkedin_post_3 = process_transcription(transcript)
        
        print("Sammanfattning på svenska:")
        print(summary)
        print("\nSlack post:")
        print(slack_post)
        print("\nLinkedIn Post 1:")
        print(linkedin_post_1)
        print("\nLinkedIn Post 2:")
        print(linkedin_post_2)
        print("\nLinkedIn Post 3:")
        print(linkedin_post_3)