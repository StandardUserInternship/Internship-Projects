# Defining imports for the script
import os
import matplotlib.pyplot as plt
import pandas as pd


"""
    The create_bar_chart, create_line_chart and main functions will not have to be altered in order for this program to succesfully run.
    Only modify the create_Monthly_Chart and create_Yearly_Chart functions.
    filePaths variable might have to be modified dependant upon your project structure
"""



# Creating our X and Y array to hold different data
xArray = []
yArray = []

# Creating a filePaths variable to get our absolute path so that it can be used for selecting different datasets
filePaths = os.path.join(os.getcwd(), 'Handwashing_Data_Science')

# Function to create a bar chart with the specified arguments
def create_bar_chart(xData, yData, title, xLabel, yLabel, color):
    """
    Create Bar Chart
    Args:
        xData (list): List of x data
        yData (list): List of Y data
        title (str): The title of the chart
        xLabel (str): The label for the X position
        yLabel (str): The label for the Y position
        color (str): Color to set for the lines (orange, red, yellow, green, blue)
    
    Returns:
        A bar chart generated from the arguments passed above.
    """
    # Visualizing the data so that it can be understood easier.
    fig, ax = plt.subplots(figsize=(10,4))
    plt.bar(xData, yData, width=0.6, color=color)
    plt.title(title, fontsize=16)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.show()

# Function to create a line chart with the specified arguments
def create_line_chart(xData, yData, title, xLabel, yLabel, color):
    """
    Create Line Chart
    Args:
        xData (list): List of x data
        yData (list): List of Y data
        title (str): The title of the chart
        xLabel (str): The label for the X position
        yLabel (str): The label for the Y position
        color (str): Color to set for the lines (orange, red, yellow, green, blue)
    
    Returns:
        A line chart generated from the arguments passed above.
    """
    fig,ax = plt.subplots(figsize = (10,4))
    plt.plot(xData, yData, color=color)
    plt.title(title, fontsize=16)
    plt.xlabel(xLabel, fontsize=14)
    plt.ylabel(yLabel, fontsize=14)
    plt.show()


# Function to create charts based upon the monthly dataset
def create_Monthly_Chart():
    """
    Create Monthly Charts
    
    Returns:
        Different charts and information about the monthly deaths dataset.
    """
    csvFile = pd.read_csv('monthly_deaths.csv')

    # Printing out the first 5 rows
    print(csvFile.head(5))

    # Calculating proportions of deaths per month
    csvFile['Proportion of Deaths'] = csvFile['deaths'] // csvFile['births']

    # Change the data type of the 'date' column from string to datetime
    csvFile['date'] = pd.to_datetime(csvFile['date'])

    # The summer of 1847 is when it was made obligatory for doctors to wash their hands.
    start_handwashing = pd.to_datetime('1847-06-01')

    # Split monthly data into before and after handwashing
    before_washing = csvFile[csvFile['date'] < start_handwashing]
    after_washing = csvFile[csvFile['date'] >= start_handwashing]

    # Create before handwashing chart
    create_line_chart(before_washing['data'], before_washing['Proportion of Deaths'], 'Before Handwashing', 'Date', 'Proportion of Deaths', 'red')

    # Create after handwashing chart
    create_line_chart(after_washing['data'], after_washing['Proportion of Deaths'], 'After Handwashing', 'Date', 'Proportion of Deaths', 'green')

    # Create a chart showing both before and after on the same chart
    ax = before_washing.plot(x='date', y='Proportion of Deaths', label='Before Handwashing', color='red')
    after_washing.plot(x= "date", y= "Proportion of Deaths", label= "After Handwashing", ax=ax, ylabel= "Proportion deaths", color="green")
    plt.show()

    # Calculating the difference to determine how much handwashing actually effected
    before_proportion = before_washing['Proportions of Deaths']
    after_proportion = after_washing['Proportions of Deaths']

    mean_difference = after_proportion.mean() - before_proportion.mean()

    # Printing out the proportions before handwashing
    print(before_proportion.mean())

    # Printing out the proportions after handwashing
    print(after_proportion.mean())

    # Printing percentage change
    print(f'After handwashing, there was a {mean_difference:.0%} reduction in the proportion of deaths.')

# Function to create charts based upon the yearly dataset
def create_Yearly_Chart():
    """
    Create Yearly Charts
    
    Returns:
        Different charts and information about the yearly deaths dataset.
    """
    # Loading the CSV file
    csvFile = pd.read_csv('{filePaths}/yearly_deaths_by_clinic.csv')

    # Printing the shape of the data
    print(csvFile.shape)

    # Grouping the data by clinic and deaths
    groupedData = csvFile.groupby('clinic')['death'].sum()
    
    # Printing the grouped data, to make the analysis easier, we can calculate the proportion of deaths to births.
    print(groupedData)

    # Creating new row of data in the csv file
    csvFile['Proportion of Deaths'] = csvFile['deaths'] / csvFile['births']

    # Splitting the datasets by clinic
    clinic_1 = csvFile[csvFile['clinic'] == 'clinic 2']
    clinic_2 = csvFile[csvFile['clinic'] == 'clinic 1']

    # Printing out Clinic 1 and Clinic 2
    print(clinic_1, clinic_2)

    # Creating Clinic 1 and Clinic 2 charts
    create_bar_chart(clinic_1.year, clinic_1.deaths, 'Clinic 1: Deaths per Year','Year', 'Number of Deaths', 'red')
    create_bar_chart(clinic_2.year, clinic_2.deaths, 'Clinic 2: Deaths per Year','Year', 'Number of Deaths', 'orange')

    # Plotting Clinic 1 and Clinic 2 on a line chart so that they can be directly compared.
    ax = clinic_1.plot(x='year', y='Proportion of Deaths', label='Clinic 1', color='red')
    clinic_2.plot(x='year', y='Proportion of Deaths', label='Clinic 2', ax=ax, ylabel='Proportion of Deaths', color='orange')
    plt.show()

# Main run function to execute both functions to create yearly and monthly charts,
if __name__ in '__main__':
    create_Yearly_Chart()
    create_Monthly_Chart()