import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.ensemble import VotingClassifier

data = pd.read_csv('hundred_filtered_cleaned_data.tsv', sep='\t')

data['full_text'] = data['product_name'] + ' ' + data['ingredients_text']

X_text = data['full_text']
X_numeric = data[['proteins_100g', 'energy_100g', 'fat_100g', 'saturated-fat_100g', 'trans-fat_100g', 'cholesterol_100g', 'carbohydrates_100g', 'sugars_100g', 'fiber_100g', 'proteins_100g', 'calcium_100g']]  # Add more numeric columns as needed
y = data['categories']

X_text_train, X_text_test, X_numeric_train, X_numeric_test, y_train, y_test = train_test_split(
    X_text, X_numeric, y, test_size=0.2, random_state=42
)

text_transformer = Pipeline([
    ('tfidf', TfidfVectorizer(
        stop_words='english',
        lowercase=True,
        token_pattern=r'\b\w+\b',
    )),
])

numeric_transformer = Pipeline([
    ('scaler', StandardScaler()),
])

text_classifier = Pipeline([
    ('tfidf', text_transformer),
    ('clf', RandomForestClassifier()),
])

text_classifier.fit(X_text_train, y_train)

numeric_classifier = Pipeline([
    ('scaler', numeric_transformer),
    ('clf', RandomForestClassifier()),
])

numeric_classifier.fit(X_numeric_train, y_train)

y_pred_text = text_classifier.predict(X_text_test)

y_pred_numeric = numeric_classifier.predict(X_numeric_test)

combined_classifier = VotingClassifier(
    estimators=[
        ('text', text_classifier),
        ('numeric', numeric_classifier)
    ],
    voting='soft'
)

combined_classifier.fit(X_text_test, y_test)

y_pred_combined = combined_classifier.predict(X_text_test)

accuracy_combined = accuracy_score(y_test, y_pred_combined)
report_combined = classification_report(y_test, y_pred_combined)

print("Combined Classifier Accuracy:", accuracy_combined)
print("Combined Classifier Report:")
print(report_combined)
