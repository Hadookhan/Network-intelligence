from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd
import math

class Intelligence:
    def __init__(self, rows: list[dict], target: str) -> None:
        self.rows = rows
        self.__df = self.__conv_to_dataframe()

        self.__X = self.__df.drop(columns=[target]) # X = features
        self.__y = self.__df[target] # Y = target

        self.__cats = ["node"]
        self.__X = self.__encode_categoricals() if self.__cats else self.__X

        self.__X_train, self.__X_test, self.__y_train, self.__y_test = self.__train_test_split()

        self.__model = self.__fit_model_with_train()
    
    def __conv_to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.rows)
    
    def __encode_categoricals(self) -> pd.DataFrame:
        return pd.get_dummies(self.__X, columns=self.__cats, drop_first=True)
    
    def __train_test_split(self, test_size: float = 0.2, random_state: int = 42) -> tuple:
        return train_test_split(self.__X, self.__y, test_size=test_size, random_state=random_state)
    
    def __fit_model_with_train(self) -> RandomForestRegressor:
        model = RandomForestRegressor(random_state=42)
        model.fit(self.__X_train, self.__y_train)
        return model

    def display_model_score(self) -> None:
        print(f"R^2: {self.r_squared()}")
        print(f"MAE (Mean Abs Error): {self.mae()}")
        print(f"RMSE (Root Mean Square Error): {self.rmse()}")

    def r_squared(self) -> float:
        """
            Calculates variance of a feature
        """
        return self.__model.score(self.__X_test, self.__y_test)

    def mae(self) -> float:
        """
            Average error of prediction compared to real values
        """
        y_pred = self.__model.predict(self.__X_test)
        return mean_absolute_error(self.__y_test, y_pred)

    def rmse(self) -> float:
        """
            Error of worst prediction
        """
        y_pred = self.__model.predict(self.__X_test)
        return math.sqrt(mean_squared_error(self.__y_test, y_pred))

    def save(self) -> None:
        self.__df.to_csv("simulation_dataset.csv", index=False)

    def predict(self, X: list[list[float]]) -> float:
        preds = self.__model.predict(X)
        return float(sum(preds) / len(preds))