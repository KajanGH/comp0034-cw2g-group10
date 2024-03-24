import pandas as pd

def transform_and_round_forecast_data_region(forecast_path, output_path=None):
    """
    Transforms the forecasted data to match the structure of the original dataset,
    keeps the 'persons' category, and rounds the age group data to integers.

    Parameters:
    - forecast_path: str, path to the forecasted data CSV file.
    - output_path: str, optional path to save the transformed data CSV file.

    Returns:
    - DataFrame of the transformed and rounded forecasted data.
    """
    # Load the forecasted data, ensuring the first column is correctly named 'extract_date'
    forecast = pd.read_csv(forecast_path)
    forecast.rename(columns={forecast.columns[0]: 'extract_date'}, inplace=True)

    # Melting the forecast data to long format
    forecast_long = pd.melt(forecast, id_vars=['extract_date'], var_name='combined', value_name='count')

    # Parsing the 'combined' column to separate region, gender, and age
    forecast_long['region'] = forecast_long['combined'].apply(lambda x: x.split('_')[0])
    forecast_long['gender'] = forecast_long['combined'].apply(lambda x: x.split('_')[1])
    forecast_long['age_group'] = forecast_long['combined'].apply(lambda x: 'age_' + x.split('_')[-1])

    # Pivot the data to have age groups as columns, keeping 'persons' in the data
    forecast_pivoted = forecast_long.pivot_table(index=['extract_date', 'region', 'gender'],
                                                 columns='age_group', values='count', aggfunc='sum').reset_index()

    # Rename columns to match 'prepared_rgn.csv' style and convert counts to integers
    forecast_pivoted.columns = [col if isinstance(col, str) else f'age_{col}' for col in forecast_pivoted.columns]
    for col in forecast_pivoted.columns:
        if col.startswith('age_'):
            forecast_pivoted[col] = forecast_pivoted[col].fillna(0).astype(int)

    # Add the 'Country' column assuming all regions belong to the same country, e.g., 'England'
    forecast_pivoted['Country'] = 'England'  # Example country name

    # Rearrange columns to match 'prepared_rgn.csv' order
    columns_order = ['Country', 'region', 'gender', 'extract_date'] + [f'age_{i}' for i in range(96)]
    forecast_final = forecast_pivoted.reindex(columns=columns_order)

    # Rename 'region' and 'gender' to match 'prepared_rgn.csv' column names
    forecast_final.rename(columns={'region': 'Region', 'gender': 'sex'}, inplace=True)

    # Optionally, save the transformed DataFrame to a new CSV file
    if output_path:
        forecast_final.to_csv(output_path, index=False)

    return forecast_final

def transform_and_round_forecast_data_ITL(forecast_path, output_path=None):
    """
    Transforms the forecasted data to match the structure of the original dataset,
    keeps the 'persons' category, and rounds the age group data to integers.

    Parameters:
    - forecast_path: str, path to the forecasted data CSV file.
    - output_path: str, optional path to save the transformed data CSV file.

    Returns:
    - DataFrame of the transformed and rounded forecasted data.
    """
    # Load the forecasted data, ensuring the first column is correctly named 'extract_date'
    forecast = pd.read_csv(forecast_path)
    forecast.rename(columns={forecast.columns[0]: 'extract_date'}, inplace=True)

    # Melting the forecast data to long format
    forecast_long = pd.melt(forecast, id_vars=['extract_date'], var_name='combined', value_name='count')

    # Parsing the 'combined' column to separate region, gender, and age
    forecast_long['ITL'] = forecast_long['combined'].apply(lambda x: x.split('_')[0])
    forecast_long['gender'] = forecast_long['combined'].apply(lambda x: x.split('_')[1])
    forecast_long['age_group'] = forecast_long['combined'].apply(lambda x: 'age_' + x.split('_')[-1])

    # Pivot the data to have age groups as columns, keeping 'persons' in the data
    forecast_pivoted = forecast_long.pivot_table(index=['extract_date', 'ITL', 'gender'],
                                                 columns='age_group', values='count', aggfunc='sum').reset_index()

    # Rename columns to match 'prepared_rgn.csv' style and convert counts to integers
    forecast_pivoted.columns = [col if isinstance(col, str) else f'age_{col}' for col in forecast_pivoted.columns]
    for col in forecast_pivoted.columns:
        if col.startswith('age_'):
            forecast_pivoted[col] = forecast_pivoted[col].fillna(0).astype(int)

    # Add the 'Country' column assuming all regions belong to the same country, e.g., 'England'
    forecast_pivoted['Country'] = 'England'  # Example country name

    # Rearrange columns to match 'prepared_rgn.csv' order
    columns_order = ['Country', 'ITL', 'gender', 'extract_date'] + [f'age_{i}' for i in range(96)]
    forecast_final = forecast_pivoted.reindex(columns=columns_order)

    # Rename 'region' and 'gender' to match 'prepared_rgn.csv' column names
    forecast_final.rename(columns={'ITL': 'ITL', 'gender': 'sex'}, inplace=True)

    # Optionally, save the transformed DataFrame to a new CSV file
    if output_path:
        forecast_final.to_csv(output_path, index=False)

    return forecast_final

def transform_and_round_forecast_data_LAD(forecast_path, output_path=None):
    """
    Transforms the forecasted data to match the structure of the original dataset,
    keeps the 'persons' category, and rounds the age group data to integers.

    Parameters:
    - forecast_path: str, path to the forecasted data CSV file.
    - output_path: str, optional path to save the transformed data CSV file.

    Returns:
    - DataFrame of the transformed and rounded forecasted data.
    """
    # Load the forecasted data, ensuring the first column is correctly named 'extract_date'
    forecast = pd.read_csv(forecast_path)
    forecast.rename(columns={forecast.columns[0]: 'extract_date'}, inplace=True)

    # Check if 'extract_date' column exists
    if 'extract_date' not in forecast.columns:
        raise ValueError("The 'extract_date' column is not correctly set in the DataFrame.")

    # Melting the forecast data to long format
    forecast_long = pd.melt(forecast, id_vars=['extract_date'], var_name='combined', value_name='count')

    # Parsing the 'combined' column to separate LAD, gender, and age
    forecast_long['LAD'] = forecast_long['combined'].apply(lambda x: x.split('_')[0])
    forecast_long['gender'] = forecast_long['combined'].apply(lambda x: x.split('_')[1])
    forecast_long['age_group'] = forecast_long['combined'].apply(lambda x: 'age_' + x.split('_')[-1])

    # Pivot the data to have age groups as columns, keeping 'persons' in the data
    forecast_pivoted = forecast_long.pivot_table(index=['extract_date', 'LAD', 'gender'],
                                                 columns='age_group', values='count', aggfunc='sum').reset_index()

    # Rename columns to match the desired style and convert counts to integers
    forecast_pivoted.columns = [col if isinstance(col, str) else f'age_{col}' for col in forecast_pivoted.columns]
    for col in forecast_pivoted.columns:
        if col.startswith('age_'):
            forecast_pivoted[col] = forecast_pivoted[col].fillna(0).astype(int)

    # Add the 'Country' column assuming all LADs belong to the same country, e.g., 'England'
    forecast_pivoted['Country'] = 'England'  # Example country name

    # Rearrange columns to match the desired order
    columns_order = ['Country', 'LAD', 'gender', 'extract_date'] + [f'age_{i}' for i in range(96)]
    forecast_final = forecast_pivoted.reindex(columns=columns_order)

    # Rename 'gender' to match the desired column names
    forecast_final.rename(columns={'gender': 'sex'}, inplace=True)

    # Optionally, save the transformed DataFrame to a new CSV file
    if output_path:
        forecast_final.to_csv(output_path, index=False)

    return forecast_final

def transform_and_round_forecast_data_CTRY(forecast_path, output_path=None):
    """
    Transforms the forecasted data to match the structure of the original dataset,
    keeps the 'persons' category, and rounds the age group data to integers.

    Parameters:
    - forecast_path: str, path to the forecasted data CSV file.
    - output_path: str, optional path to save the transformed data CSV file.

    Returns:
    - DataFrame of the transformed and rounded forecasted data.
    """
    # Load the forecasted data, ensuring the first column is correctly named 'extract_date'
    forecast = pd.read_csv(forecast_path)
    forecast.rename(columns={forecast.columns[0]: 'extract_date'}, inplace=True)

    # Melting the forecast data to long format
    forecast_long = pd.melt(forecast, id_vars=['extract_date'], var_name='combined', value_name='count')

    # Parsing the 'combined' column to separate region, gender, and age
    
    forecast_long['gender'] = forecast_long['combined'].apply(lambda x: x.split('_')[0])
    forecast_long['age_group'] = forecast_long['combined'].apply(lambda x: 'age_' + x.split('_')[-1])

    # Pivot the data to have age groups as columns, keeping 'persons' in the data
    forecast_pivoted = forecast_long.pivot_table(index=['extract_date','gender'],
                                                 columns='age_group', values='count', aggfunc='sum').reset_index()

    # Rename columns to match 'prepared_rgn.csv' style and convert counts to integers
    forecast_pivoted.columns = [col if isinstance(col, str) else f'age_{col}' for col in forecast_pivoted.columns]
    for col in forecast_pivoted.columns:
        if col.startswith('age_'):
            forecast_pivoted[col] = forecast_pivoted[col].fillna(0).astype(int)

    # Add the 'Country' column assuming all regions belong to the same country, e.g., 'England'
    forecast_pivoted['Country'] = 'England'  # Example country name

    # Rearrange columns to match 'prepared_rgn.csv' order
    columns_order = ['Country','extract_date','gender'] + [f'age_{i}' for i in range(96)]
    forecast_final = forecast_pivoted.reindex(columns=columns_order)

    # Rename 'region' and 'gender' to match 'prepared_rgn.csv' column names
    forecast_final.rename(columns={'gender': 'sex'}, inplace=True)

    # Optionally, save the transformed DataFrame to a new CSV file
    if output_path:
        forecast_final.to_csv(output_path, index=False)

    return forecast_final


transformed_data_LAD = transform_and_round_forecast_data_CTRY('/Users/omeryurttutmus/Desktop/forecast_ctry.csv', '/Users/omeryurttutmus/Desktop/edited_forecast_ctry_sex_age_group.csv')
transformed_data_region = transform_and_round_forecast_data_region('/Users/omeryurttutmus/Desktop/forecast_Region_sex_age_group.csv', '/Users/omeryurttutmus/Desktop/edited_forecast_Region_sex_age_group.csv')
transformed_data_ITL = transform_and_round_forecast_data_ITL('/Users/omeryurttutmus/Desktop/forecast_ITL_sex_age_group.csv', '/Users/omeryurttutmus/Desktop/edited_forecast_ITL_sex_age_group.csv')
transformed_data_LAD = transform_and_round_forecast_data_LAD('/Users/omeryurttutmus/Desktop/forecast_lad_sex_age_group-1.csv', '/Users/omeryurttutmus/Desktop/edited_forecast_LAD_sex_age_group.csv')