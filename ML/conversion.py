import os
import json
import openai

# set API Key
openai.api_key = os.environ['OPENAI_API_KEY']

# mapping
sex_mapping = {
    "Male": 1,
    "Female": 0
}

fitness_goal_mapping = {
    "Fat Loss": 1,
    "Maintenance": 2,
    "Muscle Gain": 3
}

# change this mapping into something more meaningful
activity_mapping = {
    "None": 0,
    "Lifting": 1,
    "Cardio": 2,
    "Sports": 3,
    "Everything": 4,
}

# inputs
age = input("Enter your age: ")
sex = input("Enter your sex (M/F): ")
weight = float(input("Enter your weight (pounds): "))
height = float(input("Enter your height (inches): "))
fitness_goal = input("Enter your fitness goal: ")
activity_goal = input("Describe your typical activity level: ")

# adjust input values
weight *= 0.45359237 # kg/lb factor
height *= 2.54 # cm/in factor
sex = sex_mapping[sex]
fitness_goal = fitness_goal_mapping[fitness_goal]
activity_goal = activity_mapping[activity_goal]

#===========STEP 1: CALORIE INTAKE===========

cal_difference = 0
cal_intake = 0
cal_burnt = 0
maintenance_cal = 0
excercise_cal = 0

cal_difference = 500 * (fitness_goal-2) 

if sex == 1:
    maintenance_cal = 10 * weight + 6.25 * height - 5 * age + 5
else:
    maintenance_cal = 10 * weight + 6.25 * height - 5 * age - 161 

# temporary calculation (use AI to figure how much they burnt from their activity description)
cal_burnt = 250 * activity_goal

cal_intake = cal_difference + cal_burnt

#===========STEP 2: MACROS AMOUNT===========

# these ratios are grams/pound and they're based on studies available online
# need to adjust some of these values further
protein_ratio = 1 + 0.2 * (fitness_goal-2)
fat_ratio = 0.3 + 0.1 * (fitness_goal-2)

protein = weight * protein_ratio
fat = weight * fat_ratio
carbs = weight - (protein + fat)

# protein = 4 cal/g
# carbs = 4 cal/g
# fat = 9 cal/g

#===========STEP 3: FOOD RECS ===========

# using info above, filter database to get relevant results



# generate additional/similar nutrient food recommendations using AI

prompt = f"Weight: ${weight}. Age: ${age}. Sex: ${sex}. Height: ${height}. Calories Intake per day: ${cal_intake}. Amount of protein (g) per day: ${protein}. Amount of fat (g) per day: ${fat}. Amount of carbs (g) per day: ${carbs}. Please generate a list of food recommendations that add up to the provided calorie intake of {cal_intake} based on the information of a certain individual above. "

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant with extensive experience in nutrition and food science."},
    {"role": "user", "content": prompt}
  ]
)

print(completion.choices[0].message.get("content"))


#===========STEP 4: CLASSIFIER===========

# classify all the foods above into breakfast, lunch, dinner, sweets, and snacks
# provide three recs per category (pad/truncate accordingly)