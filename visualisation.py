import matplotlib.pyplot as plt
import pandas as pd


def lineplot(df, headers):
    """plot line chart and writes into a file.

    Parameters:
        - df (dataframe): Dataset.
        - headers (list of headers): column headers of dataset
    
    Example:
        >>> linechart(df, headers)

    Returns:
        None
    """

    plt.figure(figsize=(12, 12))

    for head in headers:
        print(df[head])
        plt.plot(df["Year"], df[head], label=head)

    # labelling
    plt.xlabel("Time")
    plt.ylabel("Movie Relesed")

    # removing white space left and right. Both standard and pandas min/max
    # can be used
    plt.xlim(min(df["Year"]), df["Year"].max())

    plt.legend()
    # save as png
    plt.savefig("linplot.png")
    plt.show()

    return


def pieplot(df, year):
    """plot pie chart by taking data of particular year in dataset and writes into a file.

    Parameters:
        - df (dataframe): Dataset.
        - year (int): year of which data needs to be plotted
    
    Example:
        >>> piechart(MoviesDataset, 2023)

    Returns:
        None
    """

    plt.figure(figsize=(8, 8))

    headers = ["Netflix", "Hulu", "Prime Video", "Disney+"]

    total_releases = 0
    for column_header in headers:
        total_releases += df.loc[df["Year"] == year, column_header].values[0]

    values = []
    for column_header in headers:
        values.append(
            (df.loc[df["Year"] == year, column_header].values[0]) * 100 / total_releases
        )

    colors = ["lightcoral", "lightblue", "lightgreen", "lightyellow"]
    explode = (0, 0, 0, 0)

    plt.pie(
        values,
        explode=explode,
        labels=headers,
        colors=colors,
        autopct="%1.1f%%",
        shadow=True,
        startangle=140,
    )

    plt.legend()
    plt.savefig("pieplot_" + str(year) + ".png")
    plt.show()

    return


def barplot(df):
    """plot bar chart by taking data of particular year in dataset and writes into a file.

    Parameters:
        - df (dataframe): Dataset.
       
    Example:
        >>> piechart(MoviesDataset, 2023)

    Returns:
        None
    """

    plt.figure(figsize=(10, 6))

    x_values = range(len(df))
    ml_engineer_salaries = df["Machine Learning Engineer"]
    ml_scientist_salaries = df["Machine Learning Scientist"]

    bar_width = 0.29

    plt.bar(
        x_values,
        ml_scientist_salaries,
        width=bar_width,
        label="ML Scientist",
        alpha=0.7,
    )

    x_values = [i + bar_width for i in x_values]

    plt.bar(
        x_values, ml_engineer_salaries, width=bar_width, label="ML Engineer", alpha=0.7
    )

    plt.xticks([i + bar_width / 2 for i in range(len(df))], df["experience_level"])

    plt.xlabel("Experience")
    plt.ylabel("Salary in USD")
    plt.title("Comparision of salaries b/w different experience levels")
    plt.legend()
    plt.savefig("barchart.png")
    plt.show()

    return


def create_Plots():
    csv_file_path = "datasets/MoviesOnStreamingPlatforms.csv"

    df = pd.read_csv(csv_file_path)

    summary_year = (
        df.groupby("Year")[["Netflix", "Hulu", "Prime Video", "Disney+"]]
        .sum()
        .reset_index()
    )

    # Drop the first 81 rows
    summary_year = summary_year.drop(index=range(81))

    lineplot(summary_year, ["Netflix", "Hulu", "Prime Video", "Disney+"])

    pieplot(summary_year, 2001)

    pieplot(summary_year, 2021)


    path_dataset2 = "datasets/ds_salaries.csv"

    df_data_science_salaries = pd.read_csv(path_dataset2)


    summary_jobType = (
        df_data_science_salaries.groupby(["experience_level", "job_title"])["salary"]
        .mean()
        .reset_index()
    )

    filtered_df = summary_jobType[
        summary_jobType["job_title"].isin(
            ["Machine Learning Engineer", "Machine Learning Scientist"]
        )
    ]


    filtered_df = filtered_df[~filtered_df["experience_level"].isin(["EX"])]

    pivoted_df = filtered_df.pivot(
        index="experience_level", columns="job_title", values="salary"
    ).reset_index()
    pivoted_df["experience_level"] = ["Entry Level", "Mid Level", "Senior Level"]
    barplot(pivoted_df)
    
    return 

if __name__ == "__main__":
    create_Plots()