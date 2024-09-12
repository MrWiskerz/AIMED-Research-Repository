import re
import csv

#TODO (Things to add):
# Fix height and weight translations
# Add BMI, calorie maintence amount attribute
# Training system (Bard API)

# Function library
class Func_Library():

    master_dic = {} # "Question Name" = [user0, user1, user2]

    change_keys = {
        # "Height (in inches)" : "height_in_inches", (its not working rn)
        # "Weight (in pounds)": "weight_prettifier", 
        "Minutes of activity per day": "average_hours", 
        "How much money are you willing to spend per week on food?(The more, the better quality food)": "average_hours", 
    }
    
    remove_keys = [
        "Timestamp",
        "Upon receiving the AI generated diet plan, we will ask you to identify which plan you find more beneficial for further research purposes.",
        "If comfortable, provide your Yearly Gross Income.(This will give the AI a range of certainty)",
        "Email Address"
    ]

    def height_in_inches(self, string):
        pattern = r"(?<!')\d\d\.?\d*"
        pattern2 = r"\d'\d\d?"

        match = re.search(pattern, string)

        if match:
            return float(f"{match.group()}")
        else:
            match = re.search(pattern2, string)

            if match:
                match_string = f"{match.group()}"
                match_list = match_string.split("'")
                return float(12*int(match_list[0]) + int(match_list[1]))

            else:
                return 'error!'
            
    def weight_prettifier(self, height_input):
        pattern = r"\d+\.?\d*"
        match = re.search(pattern, height_input)

        if match:
            return float(f"{match.group()}")
        else:
            return 'Error!'

    def average_hours(self, active_input):
        pattern = r"\d+-\d+"
        pattern2 = r"\d+(?=\+)"

        match = re.search(pattern, active_input)

        if match:
            numbers = f"{match.group()}".split('-')
            return float(numbers[0])/2+float(numbers[1])/2
        else:
            match = re.search(pattern2, active_input)

            if match:
                return f"{match.group()}"
            else:
                return 'Error!'

    def get_BMI(self, height, weight):
        # In inches and Pounds
        return (weight*703)/(height*height)

    def change_value(self, val, key):
        for change_key in self.change_keys.keys():
            if key == change_key:
                replacement_func = getattr(self, self.change_keys[change_key])
                return replacement_func(val)
        return val

    def process_csv(self, data_file):
        with open(data_file, "r", encoding="utf-8", newline="") as data_text:
            spamreader = csv.reader(data_text, delimiter=",", quotechar="\"")
            key_delete_formats = [r'\ \[.*\]', "\n"]
            first_row = True
            row_num = 0
            for row in spamreader:
                question_num = len(row)
                for question_index in range(question_num):
                    if row_num == 0:
                        for format in key_delete_formats:
                            pattern = re.search(format, row[question_index])
                            if pattern:
                                left, right = pattern.span()
                                row[question_index] = row[question_index][:left]+row[question_index][right:]
                        self.master_dic[row[question_index]] = []
                        first_row = row
                    else:
                        new_val = self.change_value(row[question_index], first_row[question_index])
                        self.master_dic[first_row[question_index]].append(new_val)

                row_num += 1
        
        # Final Addons
        keys_to_remove = []
        for key in self.master_dic.keys():
            for remove_key in self.remove_keys:
                if remove_key == key:
                    keys_to_remove.append(key)
        for key in keys_to_remove:
            self.master_dic.pop(key)

    # Displaying
    def get_keys(self, dic, display_type, user_index, file=None):
        for key in dic.keys():
            format = f"{key}: {self.master_dic[key][user_index] or None} \n"
            if display_type == "file":
                file.write(format)
            elif display_type == "print":
                print(format)

    def display_information(self, dic, display_type):
        names = dic["Full Name"]
        for user_index in range(len(names)):
            if display_type == "file":
                with open(f"assests/diet_{names[user_index]}.txt", "w", encoding="utf-8") as file:
                    self.get_keys(dic, display_type, user_index, file)
            elif display_type == "print":
                self.get_keys(dic, display_type, user_index)
            elif display_type == "return":
                return self.master_dic

