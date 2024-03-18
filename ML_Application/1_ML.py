import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

class IntentPredictionModel:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None
#test
    def load_data(self):
        self.data = pd.read_csv(self.dataset_path)

    def preprocess_data(self, input1, input2, input3):
        # Drop rows with missing values
        self.data.dropna(inplace=True)
        
        # Define features (X) and target variable (y)
        X = self.data[['Age', 'Sex', 'Race', 'Education', 'Time', 'Place of Death', 'Police Presence']]
        y = self.data['Intent']
        
        # Add user inputs to the features
        X['Input1'] = input1
        X['Input2'] = input2
        X['Input3'] = input3
        
        # One-hot encode categorical variables
        X = pd.get_dummies(X)
        
        # Split data into training and testing sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Standardize features
        scaler = StandardScaler()
        self.X_train = scaler.fit_transform(self.X_train)
        self.X_test = scaler.transform(self.X_test)

    def train_model(self):
        # Initialize and train the Logistic Regression model
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(self.X_train, self.y_train)

    def evaluate_model(self):
        # Make predictions
        y_pred = self.model.predict(self.X_test)
        
        # Evaluate model performance
        accuracy = accuracy_score(self.y_test, y_pred)
        report = classification_report(self.y_test, y_pred)
        return accuracy, report

# Create Streamlit application
def main():
    st.title('Intent Prediction Model')

    # Load the dataset
    df = pd.read_csv('guns_cleaned.csv')

    # Sidebar inputs
    st.sidebar.title('User Inputs')
    input1 = st.sidebar.slider('Age', min_value=0, max_value=100, value=30)
    input2 = st.sidebar.selectbox('Sex', ['Male', 'Female'])
    input3 = st.sidebar.selectbox('Race', df['Race'].unique())

    # Create an instance of the IntentPredictionModel class
    model = IntentPredictionModel(dataset_path='guns_cleaned.csv')

    # Preprocess the data with user inputs
    model.preprocess_data(input1, input2, input3)

    # Train the model
    model.train_model()

    # Evaluate the model
    accuracy, report = model.evaluate_model()
    st.write('Model Accuracy:', accuracy)
    st.write('Classification Report:')
    st.write(report)

    # Visualization
    st.subheader('Visualization')
    fig, ax = plt.subplots()
    sns.countplot(data=df, x='Intent', hue='Race')
    plt.title('Intent vs. Race')
    plt.xlabel('Intent')
    plt.ylabel('Count')
    st.pyplot(fig)

if __name__ == '__main__':
    main()
