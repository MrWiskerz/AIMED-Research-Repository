import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from src.form import Func_Library
Form_Lib = Func_Library()

# Instantiation
# DOCS: https://ai.google.dev/gemini-api/docs/
genai.configure(api_key="AIzaSyDj7tSP_om4mob1LXAmVim1qxFDV8w6PiE")


# Diet stuff
target_diretory = "results"
data_directory = "assests"
participant_data = data_directory+"\DietDroid3000 Questionnaire  (Responses) - Form Responses.csv"

Form_Lib.process_csv(participant_data)
master_dic = Form_Lib.master_dic
participant_num = len(master_dic["Full Name"])
#Form_Lib.display_information(master_dic, "file") # Generate Files

def make_dietary_plan(participant_name, text, display_type):
  if display_type == "print":
    print(text)
  elif display_type == "file":
    with open( (f"{target_diretory}\{participant_name}_diet_plan(V2).rtf"), "w", encoding="utf-8") as diet_plan:
       diet_plan.write(text)
    # diet_plan = canvas.Canvas(target_diretory + "\diet_" + master_dic["Full Name"][participant_index] + ".pdf", pagesize=letter)
    # diet_plan.setFont("Helvetica", 14)
    # diet_plan.drawString(100, 750, text)
    # diet_plan.save()

AI_prompt = "Using the provided background information in text_data and table_data, make a personalized dietary plan based off the participant_info. Give an approximate price for each meal, give an approximate calorie count for each meal, provide notes on activity, and provide 4 different options for each meal. Make sure to include foods outside their culture based off their willingess to try new food."

def get_AI_response(participant_index):
  participant_name = master_dic["Full Name"][participant_index]
  participant_info = genai.upload_file(path=(f"{data_directory}\diet_{participant_name}.txt"))
  text_data = genai.upload_file(path=(f"{data_directory}\AI_TEXT_DATA.txt"))
  table_data = genai.upload_file(path=(f"{data_directory}\AI_TABLE_DATA.csv"))
  AI_response = model.generate_content([AI_prompt, participant_info, text_data, table_data])
  return participant_name, AI_response.text

def get_all_responses(response_type):
   for index in range(participant_num):
      name, text = get_AI_response(index)
      make_dietary_plan(name, text, response_type)
      

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

chat_session = model.start_chat(
  history=[
  ],
)

def run_response_loop(response_input):
    if response_input != -1:
      AI_response = chat_session.send_message(response_input)
      user_input = input(AI_response.text+"\nGenerate Response:")
      if user_input == "break":
          return -1
      else:
          run_response_loop(user_input)
    else:
        print("Program Terminated")


#get_all_responses("file")
