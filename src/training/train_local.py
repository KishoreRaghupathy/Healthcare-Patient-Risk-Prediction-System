import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score
import pickle
import os

def train_model():
    # Load data
    data_path = 'data/processed/training_data-00000-of-00001.csv'
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}. Please run ETL first.")
        return

    print("Loading data...")
    df = pd.read_csv(data_path)
    
    # Split features and target
    X = df.drop('readmitted', axis=1)
    y = df['readmitted']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train XGBoost
    print("Training model...")
    model = xgb.XGBClassifier(
        objective='binary:logistic',
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        eval_metric='logloss'
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    accuracy = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"ROC-AUC: {auc:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    
    # Save model using Pickle
    output_dir = 'models'
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, 'readmission_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {model_path}")
    
    # Also save as pickle for easier loading in some cases, although JSON is standard for XGB
    # pickle_path = os.path.join(output_dir, 'readmission_model.pkl')
    # with open(pickle_path, 'wb') as f:
    #     pickle.dump(model, f)

if __name__ == "__main__":
    train_model()
