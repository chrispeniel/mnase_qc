import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

# loading the saved model
loaded_model = pickle.load(open(r'trained_model_smote (1).sav', 'rb'))

st.set_page_config(layout="wide")


def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://www.dropbox.com/scl/fi/26omg03zr1pyqksnaz9mx/Untitled-design.png?raw=1&rlkey=1y36e61nkndoxkh9sw65aa1fk");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()
     


 
# Define a function to make predictions
def predict(df):
    predictions = []
    thresholds = []
    probabilities = []
    threshold = 0.4857142857142857  # Set the threshold value here
    
    for index, row in df.iterrows():
        features = row[['Mono', 'Under', 'Over']]
        reshaped_features = np.reshape(features, (1, -1))
        prediction_proba = loaded_model.predict_proba(reshaped_features)[0][1]  # Get the probability for positive class
        prediction = loaded_model.predict(reshaped_features)[0]
        
        if prediction == 0:
            result = 'Under or Over digested Sample'
        else:
            result = 'Good Sample'
            
        predictions.append(result)
        thresholds.append(threshold)
        probabilities.append(prediction_proba)
    
    return predictions, thresholds, probabilities

# Streamlit app main
def main():

 

     
 

    # giving a title

    text = "Felix Müller-Planitz Laboratory🧬"
    st.write(f'<p style="font-weight:bold; font-size:30px; color:White; top:0px; right:10px;">{text}</p>', unsafe_allow_html=True)

    original_title = '<p style="font-weight:bold;color:White; font-size:45px;">Mnase Digestion QC Prediction App</p>'
    st.markdown(original_title, unsafe_allow_html=True)

    sub = '<p style="font-weight:bold;color:White; font-size:20px;">MNase_QC prediction app is a machine learning (ML) model that predicts if a MNase digested sample is Good or Bad after obtaining data from the MNase_QC tool, which analyses electrophoresis images following MNase digestion of chromatin</p>'
    st.markdown(sub, unsafe_allow_html=True)
    
     
    file = st.file_uploader(type="csv")
    
    if file is not None:
        # Read the CSV file
        df = pd.read_csv(file, delimiter='\t')
        
        # Display the contents of the CSV file
        st.title("Input CSV:")
        st.dataframe(df)

        # Make predictions
        predictions, thresholds, probabilities = predict(df)
        
        # Create a new DataFrame to store the results
        result_df = pd.DataFrame({'Lane_id': df['Lane_id'], 'Prediction': predictions, 'Threshold': thresholds, 'Probability': probabilities})

        # Display the predictions
        st.title("Predictions:")

         

         # Create a layout with two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Predictions:")
            st.write(result_df)
        
        with col2:
            lane_ids = result_df['Lane_id']
            probabilities = result_df['Probability']


            st.write("Predicted probabilities Plot")
            fig, ax = plt.subplots()
            ax.bar(lane_ids, probabilities, color='green', edgecolor='black')
            ax.set_xlabel('Lane ID')
            ax.set_ylabel('Predicted Probability')
            ax.set_title('Predicted Probabilities for Lanes')
            # Add a horizontal line at the threshold value
            threshold = 0.4857142857142857
            ax.axhline(y=threshold, color='red', linestyle='--', label='Threshold')
            plt.xticks(rotation=90)

        
            st.pyplot(fig)
          

        st.write("In this classification task, the objective is to differentiate between Good and Under/Over digested samples. To determine an optimal threshold for classification, the Youden's J statistic is utilized. The Youden's J statistic assesses the balance between the true positive rate (TPR) and false positive rate (FPR) at various threshold values.")
        st.write("The TPR represents the proportion of correctly identified 'Good' samples, while the FPR denotes the proportion of 'Under/Over digested' samples mistakenly classified as 'Good'. By computing J = TPR - FPR for different threshold values, we can identify the threshold that maximizes this statistic.")
        st.write("The chosen threshold strikes a crucial balance, allowing for accurate identification of 'Good' samples while minimizing the misclassification of 'Under/Over digested' samples as 'Good'. This ensures the best overall classification performance.")
        st.write("The J statistic is computed for multiple threshold values, and the threshold with the highest J value is determined as the optimal threshold (best_threshold). This optimal threshold is then utilized to classify new samples as 'Good' or 'Under/Over digested' based on their predicted probabilities.")
        
        
        st.title("Count of predictions Plot")
        # Plot the count of predictions
        prediction_counts = pd.Series(predictions).value_counts()
        fig, ax = plt.subplots()
        ax.bar(prediction_counts.index, prediction_counts.values, color='purple', edgecolor='black')
        ax.set_xlabel('Prediction')
        ax.set_ylabel('Count')
        ax.set_title('Count of Predictions')
        st.pyplot(fig)

# Run the app
if __name__ == "__main__":
    main()
