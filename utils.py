def month_transformer(month_number:int):
    """
    Convert a month number to its corresponding French month name.
    
    Parameters:
    month_number (int): An integer between 1 and 12 representing the month of the year.
    
    Returns:
    str: The name of the month in French corresponding to the input month number.
    
    Example:
    >>> month_transformer(1)
    'Janvier'
    """
    months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    return months[month_number - 1]


def day_of_week_transformer(day_number:int):
    """
    Convert a day number to its corresponding French day name.
    
    Parameters:
    day_number (int): An integer between 0 and 6 representing the day of the week, where 0 is Monday and 6 is Sunday.
    
    Returns:
    str: The name of the day in French corresponding to the input day number.
    
    Example:
    >>> day_of_week_transformer(0)
    'Lundi'
    """
    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    return days[day_number]


def rate_months(feature:str, df):
    """
    Calculate the total sum of a specified feature for each month and the percentage rate of change between the two months with the highest sums.
    
    Parameters:
    feature (str): The name of the feature/column in the DataFrame to be summed and compared.
    df (pandas.DataFrame): The DataFrame containing the data with at least two columns, one for months ('mois') and another for the specified feature.
    
    Returns:
    tuple: A tuple containing:
        - value (float): The sum of the specified feature for the month with the highest total sum.
        - rate (float): The percentage rate of change between the two months with the highest sums of the specified feature.
    
    Example:
    >>> import pandas as pd
    >>> data = {'mois': ['Janvier', 'Février', 'Mars', 'Avril', 'Mai'], 'value': [10, 20, 30, 40, 50]}
    >>> df = pd.DataFrame(data)
    >>> value, rate = rate_months('value', df)
    """
    sum = df.groupby('mois')[feature].sum()
    value = df.groupby('mois')[feature].sum().values[0]
    month_1 = sum.loc[df.groupby('mois')[feature].sum().index[1]]
    month_2 = sum.loc[df.groupby('mois')[feature].sum().index[0]]
    rate = ((month_2 - month_1) / month_1) * 100
    return value, rate