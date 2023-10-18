from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
from typing import Optional

# Replace the path with the actual path to your TSV file
file_path = '/Users/abhinavgoel/Downloads/en.openfoodfacts.org.products.tsv'
df = pd.read_csv(file_path, sep='\t', encoding='utf-8')

# Change the data types of all columns to strings
df = df.astype(str)

selected_columns = df[['product_name', 'quantity', 'ingredients_text', 'allergens', 'traces_en', 'serving_size', 'additives_en', 'main_category_en', 'image_url', 'energy_100g', 'fat_100g', 'saturated-fat_100g', 'trans-fat_100g', 'cholesterol_100g', 'carbohydrates_100g', 'sugars_100g', 'fiber_100g', 'proteins_100g', 'sodium_100g', 'calcium_100g', 'iron_100g']]

# Save the cleaned DataFrame to a new CSV file
output_csv_path = '/Users/abhinavgoel/PycharmProjects/CalHacksNutritionProj/selected_columns.csv'  # Specify the output file path
selected_columns.to_csv(output_csv_path, index=False)
app = FastAPI()


class Category(Enum):
    TOOLS = 'tools'
    CONSUMABLES = 'consumables'


class Item(BaseModel):
    product_name: Optional[str]
    quantity: Optional[str]
    ingredients_text: Optional[str]
    allergens: Optional[str]
    traces: Optional[str]
    serving_size: Optional[str]
    additives_en: Optional[str]
    main_category_en: Optional[str]
    image_url: Optional[str]
    energy_100g: Optional[str]
    fat_100g: Optional[str]
    cholesterol_100g: Optional[str]
    carbohydrates_100g: Optional[str]
    sugars_100g: Optional[str]
    fiber_100g: Optional[str]
    proteins_100g: Optional[str]
    sodium_100g: Optional[str]
    calcium_100g: Optional[str]
    iron_100g: Optional[str]

default_values = {
    "quantity": 0,  # Default value for numeric columns
    "serving_size": 0,  # Default value for numeric columns
    "ingredients_text": "N/A",  # Default value for string columns
    "allergens": "N/A",  # Default value for string columns
    "traces_en": "N/A",  # Default value for string columns
    "additives_en": "N/A",  # Default value for string columns
    "main_category_en": "N/A",  # Default value for string columns
    "energy_100g": 0,  # Default value for numeric columns
    "fat_100g": 0,  # Default value for numeric columns
    "cholesterol_100g": 0,  # Default value for numeric columns
    "carbohydrates_100g": 0,  # Default value for numeric columns
    "sugars_100g": 0,  # Default value for numeric columns
    "fiber_100g": 0,  # Default value for numeric columns
    "proteins_100g": 0,  # Default value for numeric columns
    "sodium_100g": 0,  # Default value for numeric columns
    "calcium_100g": 0,  # Default value for numeric columns
    "iron_100g": 0,  # Default value for numeric columns
}

# User input dictionary (customize this based on user input)
user_input = {
    "proteins_100g": 50,
    "sugars_100g": 5,
}

mask = pd.Series(True, index=df.index)
for column, value in user_input.items():
    if column in default_values:
        threshold = value if value is not None else default_values[column]
        if column in df:
            column_values = df[column].apply(lambda x: float(x) if x != "N/A" else default_values[column])
            mask &= (column_values >= threshold)
filtered_df = df[mask]

items = {}
limit = 4

for i, row in filtered_df.iterrows():
    items[row['product_name']] = Item(**row.to_dict())

# We can simply use built-in python and Pydantic types, in this case dict[int, Item].
@app.get("/")
def index() -> dict[str, dict[str, Item]]:
    return {"items": items}
