import os
import argparse

from annotate import annotate
from audioparse import parse_audio
from fetch_yt import fetch_from_yt

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--url', '-u', type=str, nargs=1, help='source website URL')
parser.add_argument('--notes_out', '-on', type=str, nargs=1, help='note output path')
parser.add_argument('--transcript_out', '-ot', type=str, nargs=1, help='audio output path')
parser.add_argument('--audio_out', '-oa', type=str, nargs=1, help='audio output path')
parser.add_argument('--prompt', '-p', type=str, nargs=1, help='custom prompt to add to notetaker')

args = parser.parse_args()

src_url = ""
notes_out = "notes.txt"
transcript_out = "transcript.txt"
audio_out = "audio.webm"

save_transcript = False
save_audio = False

if args.url is None:
    print("ERROR: must provide URL (use --url or -u)")

src_url = args.url[0]

if args.notes_out is not None:
    notes_out = args.notes_out[0]

if args.transcript_out is not None:
    transcript_out = args.transcript_out[0]
    save_transcript = True

if args.audio_out is not None:
    audio_out = args.audio_out[0]
    save_audio = True

print(f"downloading audio from {src_url}")
fetch_from_yt(src_url, audio_out)

print("processing audio")
audio_transcript, t_audio, t_process_audio = parse_audio(audio_out, transcript_out)

print("generating notes")
_, t_process_notes, prompt_tokens, generation_tokens = annotate(audio_transcript, notes_out)

print("done")

