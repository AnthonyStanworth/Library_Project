import pandas as pd
from dateutil.parser import parse, ParserError
from sqlalchemy import create_engine
#import pyodbc

# Function to load a file into a dataframe
def fileLoader(filepath):
    data = pd.read_csv(filepath)
    errors = pd.DataFrame(columns=data.columns)
    return data, errors

# Function to remove rows with NaNs and duplicated rows and add the erroneous rows to an errors df
def deNaN_dedupe(df, errors_df):
    # Move NaN rows to errors_df
    nan_rows = df[df.isna().any(axis=1)]
    errors_df = pd.concat([errors_df, nan_rows], ignore_index=True)
    df.dropna(inplace=True)

    # Move duplicated rows to errors_df
    dupe_rows = df[df.duplicated(keep='first')]
    errors_df = pd.concat([errors_df, dupe_rows], ignore_index=True)
    df.drop_duplicates(inplace=True)

    return df, errors_df

# Function to change ID columns to Ints from floats
def id(df, cols):
    for i in cols:
        df[i] = df[i].astype('Int32')
    return df

# Function to check if dates are valid
def is_valid_date(date):
    """
    This function parses a date to see whether it is valid

    Note: Dates need to be in string format to be parsed correctly
    """
    if not date:
        return False
    try:
        parse(date)
        return True
    except ParserError:
        return False
    
# Function to clean date columns
def dateClean(df, dates, errors_df):

    for i in dates:
        # remove quotation marks from date cols to enable date functionality
        df[i] = df[i].str.replace('"','', regex=True)

        # Check for valid dates and append rows with invalid dates to the errors df
        df['valid date'] = df[i].apply(lambda x: is_valid_date(x))
        invalid_dates = df[df['valid date'] == False].drop('valid date', axis=1)
        errors_df = pd.concat([errors_df, invalid_dates], ignore_index=True)

        # Only keep rows with valid dates and drop valid date col
        df = df[df['valid date']]
        df.drop('valid date', axis=1, inplace=True)

        # Convert cleaned date columns to datetime
        df[i] = pd.to_datetime(df[i], dayfirst=True)
        df[i] = pd.to_datetime(df[i], dayfirst=True)

    return df, errors_df

# Function to calculate the difference between two dates
def enrichDates(df, date1, date2, errors_df):
    df['Loan Days'] = (df[date2] - df[date1]).dt.days

    df['Valid Loan'] = df['Loan Days'] >= 0
    invalid_loan = df[df['Valid Loan'] == False].drop('Valid Loan', axis=1)
    errors_df = pd.concat([errors_df, invalid_loan], ignore_index=True)

    df = df[df['Valid Loan']].drop('Valid Loan', axis=1)

    return df, errors_df


def writeToSQL(df, table_name, server, database):

    # Create the connection string with Windows Authentication
    connection_string = f'mssql+pyodbc://@{server}/{database}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'


    # Create the SQLAlchemy engine
    engine = create_engine(connection_string)

    try:
        # Write the DataFrame to SQL Server
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)

        print(f"Table{table_name} written to SQL")
    except Exception as e:
        print(f"Error writing to the SQL Server: {e}")

if __name__ == '__main__':
    print('**************** Starting Clean ****************')
    
    # Clean book file
    filepath_input = 'data/03_Library Systembook.csv'
    id_columns = ['Id', 'Customer ID']
    date_columns = ['Book checkout', 'Book Returned']

    data, errors = fileLoader(filepath_input)

    data, errors = deNaN_dedupe(data, errors)

    data = id(data, id_columns)

    data, errors = dateClean(data, date_columns, errors)

    data, errors = enrichDates(data, date1='Book checkout', date2='Book Returned', errors_df=errors)

    print(data)
    print(f"{len(errors)} records were removed from the data")
    #Cleaning the customer file
    filepath_input_2 = 'data/03_Library SystemCustomers.csv'

    data2, errors2 = fileLoader(filepath=filepath_input_2)

    # Drop duplicates & NAs
    data2, errors2 = deNaN_dedupe(data2, errors2)

    print(data2)
    print(f"{len(errors2)} records were removed from the data")
    print('**************** DATA CLEANED ****************')
"""
    print('Writing to SQL Server...')

    writeToSQL(
        data, 
        table_name='loans_bronze', 
        server = 'localhost', 
        database = 'LibraryDB'
    )

    writeToSQL(
        data2, 
        table_name='customer_bronze', 
        server = 'localhost', 
        database = 'LibraryDB'
    )
    print('**************** End ****************')
 """


