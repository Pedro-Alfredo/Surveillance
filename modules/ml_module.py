python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Treina modelo ML básico para dados estruturados
def treinar_ml():
    data = pd.DataFrame([
        {'tempo':5,'local_cameras':3,'online_posts':1,'risco':1},
        {'tempo':10,'local_cameras':0,'online_posts':0,'risco':0},
        {'tempo':3,'local_cameras':0,'online_posts':5,'risco':1},
        {'tempo':8,'local_cameras':1,'online_posts':0,'risco':0},
    ])
    X = data[['tempo','local_cameras','online_posts']]
    y = data['risco']
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    pipeline.fit(X, y)
    return pipeline
