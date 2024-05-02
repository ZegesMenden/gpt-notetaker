from faster_whisper import WhisperModel
from openai import OpenAI
import time
import sys
import os

stt_out = ""
latest_audio_time = 0.0
print("progran init")

if len(sys.argv) == 1:
    print("ERROR: must provide file name!")
    exit

fname = sys.argv[1]
oname = sys.argv[2]

if not os.path.isfile(fname):
    print(f"ERROR: {fname} does not exist!")
    exit

if os.path.isfile(oname):
    f = open(oname, "r")
    for line in f.readlines():
        if len(line) > 1000:
            stt_out = line
            break

print("done")

print("audio process init...", end="")

audio_process_t_start = time.perf_counter_ns()

if stt_out == "":

    model_size = "base.en"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(fname, beam_size=3, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=250), word_timestamps=True)

    latest_audio_time = 0

    for segment in segments:
        stt_out += segment.text
        latest_audio_time = segment.end
else:
    print("[OK]\ndetected pre-existing transcript in output file, skipping audio processing...", end="")

audio_process_t_end = time.perf_counter_ns()

print("[OK]")

client = OpenAI()

print("summarization init...", end="")

summarization_t_start = time.perf_counter_ns()

response = client.chat.completions.create(
    # model="gpt-3.5-turbo-0125",
    model="gpt-4-turbo",
    messages=[
    {
        "role": "system",
        "content": """Create extensive advanced bullet-point notes summarizing the following reading.
Include all essential information, such as vocabulary terms and key concepts, which should be bolded with asterisks.
Base your notes on the provided information, and expand on every subject with any relevant information.
For any processes or instructions in the text, provide extensive and descriptive step-by-step examples.
Do not use latex formatting for any equations and provide units in parenthesis for every equation"""
    },
    {
        "role": "user",
        "content": stt_out
    }
    ],
    temperature=1,
    max_tokens=4096,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

summarization_t_end = time.perf_counter_ns()

print("[OK]")

print("saving...")

f = open(oname, "w")
f.write("transcript:\n\n")
f.write(stt_out)
f.write("\n\nnotes:\n\n")
for chr in response.choices[0].message.content:
    try:
        f.write(chr)
    except:
        print("writing error!")
        f.flush()
f.close()

print("done")

t_audio = round(float(audio_process_t_end-audio_process_t_start)/(10**9), 3)
t_summarization = round(float(summarization_t_end-summarization_t_start)/(10**9), 3)

print("time statistics:")
print(f"\trecording time: {latest_audio_time} s")
print(f"\taudio process time: {t_audio} s")
print(f"\tsummarization process time: {t_summarization} s")
print(f"\ttotal time: {t_audio + t_summarization} s")
print("")
print(f"\trecording to translation ratio: {round((latest_audio_time/max(t_audio, 10**-9)), 2)}x speed")
print(f"\trecording to summarization ratio: {round((latest_audio_time/max(t_summarization, 10**-9)), 2)}x speed")
print(f"\trecording to total time ratio: {round((latest_audio_time/max((t_audio + t_summarization), 10**-9)), 2)}x speed")
print("")
print("tokens used:")
print(f"\tprompt: {response.usage.prompt_tokens}")
print(f"\tgeneration: {response.usage.completion_tokens}")
print(f"\ttotal: {response.usage.total_tokens}")
print(f"\testimated cost: ${round((float(response.usage.prompt_tokens)*0.01*0.001 + float(response.usage.completion_tokens)*0.03*0.001), 7)}")