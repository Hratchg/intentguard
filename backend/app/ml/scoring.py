import pickle
from pathlib import Path

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, IsolationForest

from app.ml.features import FEATURE_NAMES
from app.ml.explain import explain_features, recommend_action


class ChurnModel:
    def __init__(self):
        self.model = GradientBoostingClassifier(
            n_estimators=50, max_depth=3, random_state=42
        )
        self.trained = False

    def train(self, features_list: list[dict], labels: list[int]) -> None:
        X = np.array([[f.get(k, 0) for k in FEATURE_NAMES] for f in features_list])
        y = np.array(labels)
        self.model.fit(X, y)
        self.trained = True

    def predict(self, features: dict) -> dict:
        X = np.array([[features.get(k, 0) for k in FEATURE_NAMES]])
        proba = self.model.predict_proba(X)[0][1]
        score = round(proba * 100, 1)

        importances = self.model.feature_importances_
        feature_values = [(FEATURE_NAMES[i], features.get(FEATURE_NAMES[i], 0))
                          for i in np.argsort(importances)[::-1][:5]]

        return {
            "score": score,
            "confidence": round(max(proba, 1 - proba), 3),
            "top_features": feature_values,
            "explanation": explain_features(feature_values),
            "recommended_action": recommend_action("churn", score),
        }

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(self.model, f)

    def load(self, path: str) -> None:
        with open(path, "rb") as f:
            self.model = pickle.load(f)
        self.trained = True


class FraudModel:
    def __init__(self):
        self.model = IsolationForest(
            n_estimators=50, contamination=0.15, random_state=42
        )
        self.trained = False

    def train(self, features_list: list[dict]) -> None:
        X = np.array([[f.get(k, 0) for k in FEATURE_NAMES] for f in features_list])
        self.model.fit(X)
        self.trained = True

    def predict(self, features: dict) -> dict:
        X = np.array([[features.get(k, 0) for k in FEATURE_NAMES]])
        raw_score = -self.model.score_samples(X)[0]
        score = round(min(max(raw_score * 50, 0), 100), 1)

        feature_vals = [(FEATURE_NAMES[i], features.get(FEATURE_NAMES[i], 0))
                        for i in range(len(FEATURE_NAMES))]
        feature_vals.sort(key=lambda x: abs(x[1]), reverse=True)
        top_features = feature_vals[:5]

        return {
            "score": score,
            "confidence": round(min(raw_score / 2, 1.0), 3),
            "top_features": top_features,
            "explanation": explain_features(top_features),
            "recommended_action": recommend_action("fraud", score),
        }

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(self.model, f)

    def load(self, path: str) -> None:
        with open(path, "rb") as f:
            self.model = pickle.load(f)
        self.trained = True
