from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

# Replace the path with the actual path to your TSV file
file_path = '/Users/jaibhatia/Desktop/CalHacks/en.openfoodfacts.org.products.tsv'
df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
selected_columns = df[['product_name']]
app = FastAPI()


class Category(Enum):
    TOOLS = 'tools'
    CONSUMABLES = 'consumables'


class Item(BaseModel):
    product_name: str


items = {
    0: selected_columns.iloc[0]
}


# FastAPI handles JSON serialization and deserialization for us.
# We can simply use built-in python and Pydantic types, in this case dict[int, Item].
@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items}
