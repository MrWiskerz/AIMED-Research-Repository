import re
import csv

master_string = """9/9/2024 0:20:19,Ryan Shrestha,Male,18,5'11,189,"Black; Hispanic or Latino; Asian","Nigeria; Egypt",Hinduism,60-75,4,I eat crayons,I have diabetes since i was a child fr,"Sweet, Bitter","Crunchy, Creamy, Brittle",2,"Japanese; Chinese",,No Restriction,Kosher,"Peanut; cheese","Beef; corn",140-160,"$120,000",Gain weight (calorie surplus),More activity,4"""
master_dic = {
    
}

def get_BMI(height, weight):
    #height in inches, weight in pounds
    return (weight*703)/(height*height)

def height_in_inches(string):
    pattern = "(?<!')\d\d"
    pattern2 = "\d'\d\d?"

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
            return "error!"

   