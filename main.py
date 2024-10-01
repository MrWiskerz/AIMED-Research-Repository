import google.generativeai as genai
import os
from src.form import Func_Library
Form_Lib = Func_Library()

# Instantiation
# DOCS: https://ai.google.dev/gemini-api/docs/
genai.configure(api_key="AIzaSyDj7tSP_om4mob1LXAmVim1qxFDV8w6PiE")

# Model Creation
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

# Dietary Section
target_diretory = "results"
data_directory = "participant_data"
participant_data = data_directory+r"/DietDroid3000 Questionnaire  (Responses) - Form Responses.csv" # Participant Form Responses
AI_data_directory = "AI_DATA"     
AI_data_list = [ f"{AI_data_directory}/{file}" for file in os.listdir(AI_data_directory)]
AI_data_list.remove(f"{AI_data_directory}/AI_TABLE_DATA.csv")

Form_Lib.process_csv(participant_data)
master_dic = Form_Lib.master_dic
participant_num = len(master_dic["Full Name"])
# Form_Lib.display_information(master_dic, "file") # Make data files

for name in Form_Lib.participant_names:
   print(f"{name}: {Form_Lib.participant_names[name].split(" ")[0]}")

def make_dietary_plan(AI_response, display_type):
  participant_name, text = AI_response
  if display_type == "print":
    print(text)
  elif display_type == "file":
    with open( (f"{target_diretory}/{participant_name}_diet_plan.rtf"), "w", encoding="utf-8") as diet_plan:
       diet_plan.write(text)

AI_prompt = "Using the provided background information in text_data and table_data, make a personalized dietary plan based off the participant_info. Give an approximate price and calorie count for each meal. Provide all specific nutritional facts for each food item, including: carbohydrates, sugars, protiens, fats, sodium and cholestrol in grams. Provide a brief summary of the participant and their dietary needs. Provide notes on activity. Provide 4 different diverse options for each meal. Make sure to include foods outside their culture based off their willingess to try new food."

def get_AI_response(participant_index):
  participant_name = master_dic["Full Name"][participant_index]
  participant_info = genai.upload_file(path=(f"{data_directory}/diet_{participant_name}.txt"))

  # File uploading
  prompt_list = [AI_prompt, participant_info] + [genai.upload_file(path=file) for file in AI_data_list]
  AI_response = model.generate_content(prompt_list)

  return (participant_name, AI_response.text)

def get_all_responses(response_type):
   for index in range(participant_num):
      AI_response = get_AI_response(index)
      make_dietary_plan(AI_response, response_type)

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

#get_all_responses("file") # Get Results

