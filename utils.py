from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd
import numpy as np

def list_seasons(first_year, last_year):
    
    seasons = [f"{y:02d}{y+1:02d}" for y in range(first_year, last_year % 100 + 1)]
    
    return seasons

def confusion_classification(table, test_size):
    tablena = table.copy().dropna(subset=['FTR', 'pred'])
    # Confusion Matrix
    conf_matrix = confusion_matrix(tablena['FTR'].head(test_size), tablena['pred'].head(test_size))
    print("Confusion Matrix:")
    print(conf_matrix)

    # Classification Report
    class_report = classification_report(tablena['FTR'].head(test_size), tablena['pred'].head(test_size), zero_division=0)
    print("\nClassification Report:")
    print(class_report)
    
    
def accuracy_double_strict(y_true, y_pred_proba, threshold=0.05):
    y_pred = np.argmax(y_pred_proba, axis=1)
    
    top3_indices = np.argsort(y_pred_proba, axis=1)[:, -3:]
    second_pred = top3_indices[:, 1]
    
    valid_condition = ((y_true == y_pred) | (y_true == second_pred))
    final_accuracy = np.sum(valid_condition) / len(y_true)
    
    data = {
        'True Class': y_true,
        'Predicted Class': y_pred,
        'Second Prediction': second_pred,
        'Probabilities': [np.round(probs,2) for probs in y_pred_proba],
        'Valid' : valid_condition
    }
    
    df = pd.DataFrame(data)

    return df, final_accuracy

def accuracy_double_margin(y_true, y_pred_proba, threshold=0.05):
    y_pred = np.argmax(y_pred_proba, axis=1)
    
    top3_indices = np.argsort(y_pred_proba, axis=1)[:, -3:]
    second_pred = top3_indices[:, 1]
    third_pred = top3_indices[:, 0]

    diff_condition_trd = (np.abs(y_pred_proba[np.arange(len(y_true)), top3_indices[:, 2]] - y_pred_proba[np.arange(len(y_true)), top3_indices[:, 0]]) < threshold) & (third_pred == y_true)
        
    valid_condition = (y_true == y_pred) | (y_true == second_pred) | (diff_condition_trd )
    final_accuracy = np.sum(valid_condition) / len(y_true)
    
    data = {
        'True Class': y_true,
        'Predicted Class': y_pred,
        'Second Prediction': second_pred,
        'Probabilities': [np.round(probs,2) for probs in y_pred_proba],
        'Valid' : valid_condition
    }
    
    df = pd.DataFrame(data)

    return df, final_accuracy

def custom_accuracy_margin(y_true, y_pred_proba, threshold=0.05):
    y_pred = np.argmax(y_pred_proba, axis=1)
    
    top3_indices = np.argsort(y_pred_proba, axis=1)[:, -3:]
    second_pred = top3_indices[:, 1]
    third_pred = top3_indices[:, 0]
    
    diff_condition_snd = (np.abs(y_pred_proba[np.arange(len(y_true)), top3_indices[:, 2]] - y_pred_proba[np.arange(len(y_true)), top3_indices[:, 1]]) < threshold) & (second_pred == y_true)
    diff_condition_trd = (np.abs(y_pred_proba[np.arange(len(y_true)), top3_indices[:, 2]] - y_pred_proba[np.arange(len(y_true)), top3_indices[:, 0]]) < threshold) & (third_pred == y_true)
    
    valid_condition = (y_true == y_pred) | diff_condition_snd | diff_condition_trd
    final_accuracy = np.sum(valid_condition) / len(y_true)
    
    data = {
        'True Class': y_true,
        'Predicted Class': y_pred,
        'Second Prediction': second_pred,
        'Third Prediction': third_pred,
        'Probabilities': [np.round(probs,2) for probs in y_pred_proba],
        'Diff Condition 1': diff_condition_snd,
        'Diff Condition 2': diff_condition_trd,
        'Valid' : valid_condition
    }
    
    df = pd.DataFrame(data)

    return df, final_accuracy
