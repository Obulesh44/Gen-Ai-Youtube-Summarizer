import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import torch
import gradio as gr
from transformers import pipeline

text_summary = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", torch_dtype=torch.bfloat16)

# model_path = ("../Models/models--sshleifer--distilbart-cnn-12-6/snapshots"
#               "/a4f8f3ea906ed274767e9906dbaede7531d660ff")
# text_summary = pipeline("summarization", model=model_path,
#                 torch_dtype=torch.bfloat16)

def summary (input):
    output = text_summary(input)
    return output[0]['summary_text']

def extract_video_id(url):
    # Regex to extract the video ID from various YouTube URL formats
    regex = r"(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None


def get_youtube_transcript(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return "Video ID could not be extracted."

    try:
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Format the transcript into plain text
        formatter = TextFormatter()
        text_transcript = formatter.format_transcript(transcript)
        summary_text = summary(text_transcript)

        return summary_text
    except Exception as e:
        return f"An error occurred: {e}"


# Example URL (Replace this with the actual URL when using the script)
# video_url = "https://youtu.be/5PibknhIsTc"
# print(get_youtube_transcript(video_url))

gr.close_all()

# demo = gr.Interface(fn=summary, inputs="text",outputs="text")
demo = gr.Interface(fn=get_youtube_transcript,
                    inputs=[gr.Textbox(label="Input YouTube Url to summarize",lines=1)],
                    outputs=[gr.Textbox(label="Summarized text",lines=4)],
                    title="Gen Ai Project 2: YouTube Script Summarizer",
                    description="THIS APPLICATION WILL BE USED TO SUMMARIZE THE YOUTUBE VIDEO SCRIPT.")
demo.launch()
