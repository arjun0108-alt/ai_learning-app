import google.generativeai as genai

# 🔐 Configure API Key
genai.configure(api_key="AIzaSyBoEgcrPoT5ozan1k_aglOMObGzVUSzqvE")

# ✅ Correct & supported model
model = genai.GenerativeModel("models/gemini-2.5-flash")


def generate_content(subject, topic, content_type):
    try:
        print("DEBUG INPUT:", subject, topic, content_type)

        if not subject or not topic:
            return "Subject or Topic is empty."

        # 📘 PARAGRAPH
        if content_type == "paragraph":
            prompt = f"""
Explain "{topic}" in the subject "{subject}" in one simple paragraph.
Use easy language.
"""

        # 📄 SHORT TEXT
        elif content_type == "text":
            prompt = f"""
Explain "{topic}" in the subject "{subject}" in exactly 5 simple lines.
Each line must be on a new line.
"""

        # 🧠 QUIZ (MOST IMPORTANT 🔥)
        elif content_type == "quiz":
            prompt = f"""
Create EXACTLY 3 MCQ questions on "{topic}" in the subject "{subject}".

STRICT RULES (MUST FOLLOW):
1. Each question must be in a separate block
2. Each option (A, B, C, D) MUST be on a new line
3. DO NOT merge options in one line
4. ALWAYS include the answer in this format: Answer: A
5. Leave ONE empty line between questions
6. DO NOT add explanations or extra text

FORMAT (FOLLOW EXACTLY):

Q1. Question?
A) option
B) option
C) option
D) option
Answer: A

Q2. Question?
A) option
B) option
C) option
D) option
Answer: B
"""

        # ⭐ IMPORTANCE POINTS
        elif content_type == "importance":
            prompt = f"""
Give exactly 5 important exam points about "{topic}" in the subject "{subject}".
Each point must be on a new line.
"""

        # 🔁 FALLBACK
        else:
            prompt = f"""
Explain "{topic}" in the subject "{subject}" in simple words.
"""

        print("DEBUG PROMPT:", prompt)

        # 🤖 Generate content
        response = model.generate_content(prompt)

        # 🧪 Debug response
        print("DEBUG RESPONSE:", response)

        if response and hasattr(response, "text") and response.text:
            return response.text.strip()
        else:
            return "AI returned empty response."

    except Exception as e:
        print("AI ERROR:", e)
        return f"AI Exception: {str(e)}"
