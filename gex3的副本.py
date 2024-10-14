import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns


class DataAnalysis:
    def __init__(self):
        """Initialize the class with an empty dataset, just like GEX2"""
        self.df = None

    def dataset_loading(self):
        """Load the dataset from a CSV file."""
        file_path = "test.csv"
        print(f"Now loading from {file_path}...")
        self.df = pd.read_csv(file_path)

        """ Also store the list of column types in self.column_types."""
        self.column_types = self.list_column_types()

    def list_column_types(self):
        """use the same logic as from the GEX2"""
        """This function will check if the type of data is numeric ordinal, non-numeric ordinal, interval, or nominal."""
        """The output will be a dictionary where the key is the column name and the value is the type. """
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

    """The following function will ask the user to select one interval and one nominal/ordinal variable"""
    """The function will also allow user to skip selecting a nominal variable and instead select an ordinal variable"""

    def select_variable(self, data_type, allow_skip=False):
        """First display all the columns that are available in the column_types along with the types"""
        available_vars = self.column_types 
        print("Here are the available options:")
        for key, value in available_vars.items():
            print(f"{key}: {value}")

        """Ask the user to select a variable from the above list"""
        interval_value = input("Please select one interval column: ")
        print("Your test code is shitty thing!")
        return interval_value

        """
        if allow_skip:
            return interval_value
        else:
            nominal_ordinal_value = input("Please select one nominal/ordinal column (Can skip): ")

            if nominal_ordinal_value.strip() == "":
                print("Skipping is not allowed. Please select a nominal/ordinal column.")
                return None
            else:
                return interval_value
        """

    """This method will prompt the user to select either a numeric or non-numeric ordinal variable"""

    def select_ordinal_variable(self):
        """Store all the numeric and non-numeric ordinal variables"""
        all_ordinal_vars = {} 
        print("Here are the numeric or non-numeric ordinal variables:")
        
        for key, value in self.list_column_types().items():
            if value == "numeric ordinal" or value == "non-numeric ordinal":
                print(f"{key}: {value}")
                all_ordinal_vars[key] = value  

        if not all_ordinal_vars:
            print("No ordinal variables available.")
            return None

        """Ask the user to pick one"""
        ordinal_value = input("Please select one interval column:")

        """If the user selects a variable from the list of ordinal variables, return that selected variable"""
        """Otherwise, print invalid choice and call the select_variable method again"""
        if ordinal_value in all_ordinal_vars:
            print(f"You have selected: {ordinal_value}")
            return ordinal_value
        else:
            print("Invalid choice, please try again.")
            return None 

    """The following function simply plots Q-Q and histogram for the chosen variable"""

    def plot_qq_histogram(self, data, title):
        plt.hist(data[title], bins=30, color='skyblue', edgecolor='black')  
        plt.title(title)  
        plt.xlabel('Value')  
        plt.ylabel('Frequency')  
        sm.qqplot(data[title], line = 's')
        plt.show()

    """This function checks the normality of the variable supplied and compress it with size_limit to decide 
    if Shapiro-Wilk must be used or Anderson-Darling Test"""

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


    """This function checks for skewness in your variable. It will return True if the data is highly skewed"""

    def check_skewness(self, data):
        
        skewness = data.skew()
        print(f"Skewness: {skewness}")

        """True if the data is highly skewed"""
        return abs(skewness) > threshold


    """This function performs either ANOVA or Kruskal-Wallis based on skewness."""

    def hypothesis_test(self, continuous_var, categorical_var, skewed, null_hyp):
        """Regardless of the test you do, the function must return both the statistic and the p-value that every test returns"""
        if skewed:
            statistic, p_value = stats.kruskal(*(self.df[self.df[categorical_var] == category][continuous_var] for category in self.df[categorical_var].unique()))
            test_name = "Kruskal-Wallis Test"
        
        else:
            statistic, p_value = stats.f_oneway(*(self.df[self.df[categorical_var] == category][continuous_var] for category in self.df[categorical_var].unique()))
            test_name = "ANOVA Test"

        print(f"Test Used: {test_name}")
        print(f"Null Hypothesis: {null_hyp}")
        print(f"Statistic: {statistic}, p-value: {p_value}")
        
        """return both the statistic and p-value"""
        return statistic, p_value

def main():
    analysis = DataAnalysis()
    
    # 1. 加载数据集
    analysis.dataset_loading()
    
    # 2. 让用户选择一个连续变量，并检查其正态性并可视化 (Q-Q图和直方图)
    selected_continuous_var = analysis.select_variable(data_type='interval')
    analysis.plot_qq_histogram(analysis.df, selected_continuous_var["interval_column_name"])
    
    # 3. 让用户选择一个类别变量
    selected_categorical_var = analysis.select_variable(data_type='nominal/ordinal', allow_skip=True)
    
    # 4. 计算连续变量的偏度
    continuous_var_data = analysis.df[selected_continuous_var["interval_column_name"]]
    skewed = analysis.check_skewness(continuous_var_data)
    
    # 5. 让用户输入零假设
    null_hyp = input("Please enter the null hypothesis: ")
    
    # 6. 根据偏度进行假设检验
    categorical_var_data = analysis.df[selected_categorical_var["nominal_column_name"]]
    analysis.hypothesis_test(continuous_var_data, categorical_var_data, skewed, null_hyp)

    """The main funciton should have the following sequence:
    1. Dataset is loaded
    2. Ask the user to select a continuous variable and then check its normality and visualize it using Q-Q and histogram
    3. Ask the user to select a categorical variable
    4. Calculate skewness of the continuous variable
    5. Ask the user to enter the null hypothesis
    6. Conduct the analysis"""


if __name__ == "__main__":
    main()
