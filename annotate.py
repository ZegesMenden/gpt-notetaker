from openai import OpenAI
import time

def annotate(txt_in, fname = ""):

    client = OpenAI()

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
            "content": txt_in
        }
        ],
        temperature=1,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    summarization_t_end = time.perf_counter_ns()

    notes_out = response.choices[0].message.content

    if fname != "":
        f = open(fname, "w")
        for chr in notes_out:
            try:
                f.write(chr)
                f.flush()
            except:
                continue

    t_summarization = float(summarization_t_end-summarization_t_start)/(10**9)

    return notes_out, t_summarization, response.usage.completion_tokens, response.usage.total_tokens