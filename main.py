import google.generativeai as genai
import PyPDF2

# Instantiation
# DOCS: https://ai.google.dev/gemini-api/docs/
genai.configure(api_key="AIzaSyDj7tSP_om4mob1LXAmVim1qxFDV8w6PiE")

# Response Formating

meal_format = """ 

Breakfast: {a1} 
Lunch: {a2} 
Dinner: {a2} 

And heres a fun fact about food:
{a3}

""".format(a1=None, a2 = None, a3 = None)

# File Extractor
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        extracted_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text
        return extracted_text

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
)

#chat_session = model.generate_content()

chat_session = model.start_chat(
  history=[
  ],
)

#response = chat_session.send_message("What is a unique name?")
running = True

def run_response(response_input):
    if response_input != -1:
      AI_response = chat_session.send_message(response_input)
      user_input = input(AI_response.text+"\nGenerate Response:")
      if user_input == "break":
          return -1
      else:
          run_response(user_input)
    else:
        print("Program Terminated")

run_response(input("Generate Response: "))

