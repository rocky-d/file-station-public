import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalysis:
    def __init__(self):
        self.df = None

    def dataset_loading(self):
        file_path = "test.csv"
        print(f"Now loading from {file_path}...")
        self.df = pd.read_csv(file_path)

    def list_column_types(self):
        column_types = {}  
    
        for column_name in self.df.columns:
            print(f"Column: {column_name} - Head: {self.df[column_name].head()}")

            if pd.api.types.is_object_dtype(self.df[column_name]) and all(
                i.isnumeric() for i in self.df[column_name]
            ):
                self.df[column_name] = pd.to_numeric(self.df[column_name])

            column = self.df[column_name]
            unique_count = column.nunique()

            if pd.api.types.is_numeric_dtype(column):
                is_ordinal = unique_count < 20

                if is_ordinal:
                    print("Numeric ordinal!")
                    column_types[column_name] = "numeric ordinal"
                else:
                    print("Interval!")
                    column_types[column_name] = "interval"
            else:
                is_ordinal = unique_count < 20
                if is_ordinal:
                    print("Non-numeric ordinal!")
                    column_types[column_name] = "non-numeric ordinal"
                else:
                    print("Nominal!")
                    column_types[column_name] = "nominal"

        return column_types

    def select_variable(self, data_type, max_categories=None, allow_skip=False):
        available_vars = self.column_types 
        print("Here are the available options:")
        for key, value in available_vars.items():
            print(f"{key}: {value}")

        interval_value = input("Please select one interval column: ")
        return interval_value

    def check_normality(self, data, size_limit=2000):
        """Remember to handle missing values"""
        data.dropna(inplace=True)

        """Based on the size of the data and its comparison with size_limit, do the suitable test for nomality"""
        """Return the stat values and the p-value from whichever test you do"""
        
        if len(data) <= size_limit:
            stat, p_value = stats.shapiro(data)
            test_name = 'Shapiro-Wilk'
        else:
            stat, p_value = stats.anderson(data, dist='norm')
            test_name = 'Anderson-Darling'
        
        print(f"Using {test_name} Test")
        if test_name == 'Shapiro-Wilk':
            return stat, p_value
        else:
            return stat, None
    
    def perform_regression(self, x_var, y_var):
        X = self.df[x_var].dropna()
        Y = self.df[y_var].dropna()
        
        min_length = min(len(X), len(Y))
        X = X[:min_length]
        Y = Y[:min_length]

        slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)

        print(f"Slope: {slope:.4f}")
        print(f"Intercept: {intercept:.4f}")
        print(f"R-squared: {r_value**2:.4f}")
        print(f"P-value: {p_value:.15f}")
        print(f"Standard error: {std_err:.4f}")

        plt.scatter(X, Y, label='Data points')
        plt.plot(X, intercept + slope * X, 'r', label='Fitted line')
        plt.legend()
        
        plt.xlabel(x_var)
        plt.ylabel(y_var)

        plt.show()
        
    def t_test_or_mannwhitney(self, continuous_var, categorical_var):
        _, p_value = self.check_normality(continuous_var)
        
        unique_categories = categorical_var.dropna().unique()
        
        if len(unique_categories) != 2:
            raise ValueError("This test is only applicable to binary categorical variables.")
        
        group1 = continuous_var[categorical_var == unique_categories[0]]
        group2 = continuous_var[categorical_var == unique_categories[1]]
        
        if p_value is not None and p_value > 0.05:  
            stat, p_val = stats.ttest_ind(group1, group2)
            test_name = "t-Test"
        else:
            stat, p_val = stats.mannwhitneyu(group1, group2)
            test_name = "Mann-Whitney U Test"
        
        print(f"Using {test_name}")
        return stat, p_val

    def chi_square_test(self, categorical_var_1, categorical_var_2):
        contingency_table = pd.crosstab(categorical_var_1, categorical_var_2)
        stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        print(f"Chi-Square Statistic: {stat}, p-value: {p_value}, Degrees of Freedom: {dof}")
        return stat, p_value

def main():
    pass


if __name__ == "__main__":
    main()
