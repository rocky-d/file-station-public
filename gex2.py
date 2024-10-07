import pandas as pd
import matplotlib.pyplot as plt


class DataInspection:
    def __init__(self):
        self.df = None

    def load_csv(self, file_path):
        self.df = pd.read_csv(file_path)

    def plot_histogram(self, col):
        plt.figure()
        plt.hist(self.df[col])
        plt.title(f"Histogram of '{col}'")
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.grid()
        plt.show()

    def plot_boxplot(self, x_col, y_col):
        plt.figure()
        plt.boxplot([self.df[x_col], self.df[y_col]], tick_labels=[x_col, y_col])
        plt.title(f"Box Plot of '{x_col}' and '{y_col}'")
        plt.xlabel('Columns')
        plt.ylabel('Value')
        plt.grid()
        plt.show()

    def plot_bar_chart(self, col):
        plt.figure()
        counts = self.df[col].value_counts()
        plt.bar(counts.index, counts.values)
        plt.title(f"Bar Chart of '{col}'")
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.grid()
        plt.show()

    def plot_scatter(self, x_col, y_col):
        plt.figure()
        plt.scatter(self.df[x_col], self.df[y_col])
        plt.title(f"Scatter Plot of '{x_col}' and '{y_col}'")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.grid()
        plt.show()

    def handle_missing_values(self, col):
        if 0.5 < self.df[col].isna().sum() / len(self.df):
            self.df.drop(columns=[col], inplace=True)
            return False
        filling_val = self.df[col].median() if pd.api.types.is_numeric_dtype(self.df[col]) else self.df[col].mode()[0]
        self.df[col] = self.df[col].fillna(filling_val)
        return True
    
    def check_data_types(self, col):
        if pd.api.types.is_object_dtype(self.df[col]) and all(val.isnumeric() for val in self.df[col]):
            self.df[col] = pd.to_numeric(self.df[col])

    def classify_and_calculate(self, col):
        if not self.handle_missing_values(col):
            return None
        self.check_data_types(col)
        norminal_ordinal = self.df[col].nunique() / len(self.df[col]) < 0.1
        if pd.api.types.is_object_dtype(self.df[col]) or pd.api.types.is_bool_dtype(self.df[col]):
            if norminal_ordinal:
                self.plot_bar_chart(col)
                res = self.df[col].mode()[0]
            else:
                res = None
        else:
            if norminal_ordinal:
                self.plot_boxplot(col, col)
                res = self.df[col].median()
            else:
                self.plot_histogram(col)
                res = self.df[col].mean()
        return res

    def classify_columns(self):
        for col in self.df.columns:
            self.classify_and_calculate(col)

    def ask_for_scatterplot(self):
        numeric_cols = self.numeric_columns()
        print('=== Numeric Columns ===')
        print(*(f"({idx}) {col}." for idx, col in enumerate(numeric_cols, start=1)), sep='\n')
        print()
        choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        while not (choice_input.isdigit() and 1 <= int(choice_input) <= len(numeric_cols)):
            choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        col1 = numeric_cols[int(choice_input) - 1]
        print()
        choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        while not (choice_input.isdigit() and 1 <= int(choice_input) <= len(numeric_cols)):
            choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        col2 = numeric_cols[int(choice_input) - 1]
        print()
        self.plot_scatter(col1, col2)

    def ask_for_boxplot(self):
        numeric_cols = self.numeric_columns()
        print('=== Numeric Columns ===')
        print(*(f"({idx}) {col}." for idx, col in enumerate(numeric_cols, start=1)), sep='\n')
        print()
        choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        while not (choice_input.isdigit() and 1 <= int(choice_input) <= len(numeric_cols)):
            choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        col1 = numeric_cols[int(choice_input) - 1]
        print()
        choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        while not (choice_input.isdigit() and 1 <= int(choice_input) <= len(numeric_cols)):
            choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        col2 = numeric_cols[int(choice_input) - 1]
        print()
        self.plot_boxplot(col1, col2)

    def numeric_columns(self):
        # return list(filter(pd.api.types.is_numeric_dtype, self.df.columns))
        return [col for col in self.df.columns if pd.api.types.is_numeric_dtype(self.df[col])]

    def ask_for_correlation(self, numeric_cols):
        print('=== Numeric Columns ===')
        print(*(f"({idx}) {col}." for idx, col in enumerate(numeric_cols, start=1)), sep='\n')
        print()
        choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        while not (choice_input.isdigit() and 1 <= int(choice_input) <= len(numeric_cols)):
            choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        col1 = numeric_cols[int(choice_input) - 1]
        print()
        choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        while not (choice_input.isdigit() and 1 <= int(choice_input) <= len(numeric_cols)):
            choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        col2 = numeric_cols[int(choice_input) - 1]
        print()
        return self.df[col1].corr(self.df[col2])

    def ask_for_std(self, numeric_cols):
        print('=== Numeric Columns ===')
        print(*(f"({idx}) {col}." for idx, col in enumerate(numeric_cols, start=1)), sep='\n')
        print()
        choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        while not (choice_input.isdigit() and 1 <= int(choice_input) <= len(numeric_cols)):
            choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        col = numeric_cols[int(choice_input) - 1]
        print()
        return self.df[col].std()

    def ask_for_kurtosis(self, numeric_cols):
        print('=== Numeric Columns ===')
        print(*(f"({idx}) {col}." for idx, col in enumerate(numeric_cols, start=1)), sep='\n')
        print()
        choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        while not (choice_input.isdigit() and 1 <= int(choice_input) <= len(numeric_cols)):
            choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        col = numeric_cols[int(choice_input) - 1]
        print()
        return self.df[col].kurt()

    def ask_for_skewness(self, numeric_cols):
        print('=== Numeric Columns ===')
        print(*(f"({idx}) {col}." for idx, col in enumerate(numeric_cols, start=1)), sep='\n')
        print()
        choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        while not (choice_input.isdigit() and 1 <= int(choice_input) <= len(numeric_cols)):
            choice_input = input(f"Please select a column (an integer in [1, {len(numeric_cols)}]) >> ")
        col = numeric_cols[int(choice_input) - 1]
        print()
        return self.df[col].skew()


def main():
    analysis = DataInspection()
    analysis.load_csv(input('Please enter a CSV file path >> '))
    analysis.classify_columns()
    analysis.ask_for_scatterplot()
    analysis.ask_for_boxplot()
    numeric_cols = analysis.numeric_columns()
    print(numeric_cols)


if __name__ == "__main__":
    main()
