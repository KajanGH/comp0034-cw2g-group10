import pandas as pd

def transform_and_round_forecast_data_region(forecast_path, original_data_path, output_path=None):
    """
    Transforms the forecasted data to match the structure of the original dataset,
    keeps the 'persons' category, rounds the age group data to integers, and adds latitude and longitude data.

    Parameters:
    - forecast_path: str, path to the forecasted data CSV file.
    - original_data_path: str, path to the original data CSV file with latitude and longitude.
    - output_path: str, optional path to save the transformed data CSV file.

    Returns:
    - DataFrame of the transformed and rounded forecasted data with latitude and longitude.
    """
    # Load the forecasted data, ensuring the first column is correctly named 'extract_date'
    forecast = pd.read_csv(forecast_path)
    forecast.rename(columns={forecast.columns[0]: 'extract_date'}, inplace=True)

    # Load the original data and create a unique mapping of regions to their latitude and longitude
    original_data = pd.read_csv(original_data_path)
    region_lat_lon = original_data[['Region', 'Latitude', 'Longitude']].drop_duplicates()

    # Melting the forecast data to long format
    forecast_long = pd.melt(forecast, id_vars=['extract_date'], var_name='combined', value_name='count')

    # Parsing the 'combined' column to separate region, sex, and age
    forecast_long['Region'] = forecast_long['combined'].apply(lambda x: x.split('_')[0])
    forecast_long['sex'] = forecast_long['combined'].apply(lambda x: x.split('_')[1])
    forecast_long['age_group'] = forecast_long['combined'].apply(lambda x: 'age_' + x.split('_')[-1])

    # Pivot the data to have age groups as columns, keeping 'persons' in the data
    forecast_pivoted = forecast_long.pivot_table(index=['extract_date', 'Region', 'sex'],
                                                 columns='age_group', values='count', aggfunc='sum').reset_index()

    # Rename columns to match the desired style and convert counts to integers
    forecast_pivoted.columns = [col if isinstance(col, str) else f'age_{col}' for col in forecast_pivoted.columns]
    for col in forecast_pivoted.columns:
        if col.startswith('age_'):
            forecast_pivoted[col] = forecast_pivoted[col].fillna(0).astype(int)

    forecast_pivoted['Country'] = 'England'  
    # Merge with the unique region mapping to get latitude and longitude for each region
    forecast_merged = pd.merge(forecast_pivoted, region_lat_lon, on='Region', how='left')
    
    # Combine the original data with the transformed forecast data
    combined_data = pd.concat([original_data, forecast_merged])

    # Optionally, save the combined DataFrame to a new CSV file
    if output_path:
        combined_data.to_csv(output_path, index=False)

    return combined_data

def transform_and_round_forecast_data_ITL(forecast_path, original_data_path, output_path=None):
    """
    Transforms the forecasted data to match the structure of the original dataset,
    keeps the 'persons' category, rounds the age group data to integers, and adds latitude and longitude data.

    Parameters:
    - forecast_path: str, path to the forecasted data CSV file.
    - original_data_path: str, path to the original data CSV file with latitude and longitude.
    - output_path: str, optional path to save the transformed data CSV file.

    Returns:
    - DataFrame of the transformed and rounded forecasted data with latitude and longitude.
    """
    # Load the forecasted data, ensuring the first column is correctly named 'extract_date'
    forecast = pd.read_csv(forecast_path)
    forecast.rename(columns={forecast.columns[0]: 'extract_date'}, inplace=True)

    # Load the original data and create a unique mapping of ITLs to their latitude and longitude
    original_data = pd.read_csv(original_data_path)
    ITL_lat_lon_reg = original_data[['ITL', 'Latitude', 'Longitude',"Region"]].drop_duplicates()

    # Melting the forecast data to long format
    forecast_long = pd.melt(forecast, id_vars=['extract_date'], var_name='combined', value_name='count')

    # Parsing the 'combined' column to separate ITL, sex, and age
    forecast_long['ITL'] = forecast_long['combined'].apply(lambda x: x.split('_')[0])
    forecast_long['sex'] = forecast_long['combined'].apply(lambda x: x.split('_')[1])
    forecast_long['age_group'] = forecast_long['combined'].apply(lambda x: 'age_' + x.split('_')[-1])

    # Pivot the data to have age groups as columns, keeping 'persons' in the data
    forecast_pivoted = forecast_long.pivot_table(index=['extract_date', 'ITL', 'sex'],
                                                 columns='age_group', values='count', aggfunc='sum').reset_index()

    # Rename columns to match the desired style and convert counts to integers
    forecast_pivoted.columns = [col if isinstance(col, str) else f'age_{col}' for col in forecast_pivoted.columns]
    for col in forecast_pivoted.columns:
        if col.startswith('age_'):
            forecast_pivoted[col] = forecast_pivoted[col].fillna(0).astype(int)

    forecast_pivoted['Country'] = 'England'  
    # Merge with the unique ITL mapping to get latitude and longitude for each ITL
    forecast_merged = pd.merge(forecast_pivoted, ITL_lat_lon_reg, on='ITL', how='left')

    # Combine the original data with the transformed forecast data
    combined_data = pd.concat([original_data, forecast_merged])

    # Optionally, save the combined DataFrame to a new CSV file
    if output_path:
        combined_data.to_csv(output_path, index=False)

    return combined_data

def transform_and_round_forecast_data_LAD(forecast_path, original_data_path, output_path=None):
    """
    Transforms the forecasted data to match the structure of the original dataset,
    keeps the 'persons' category, rounds the age group data to integers, and adds latitude and longitude data.

    Parameters:
    - forecast_path: str, path to the forecasted data CSV file.
    - original_data_path: str, path to the original data CSV file with latitude and longitude.
    - output_path: str, optional path to save the transformed data CSV file.

    Returns:
    - DataFrame of the transformed and rounded forecasted data with latitude and longitude.
    """
    # Load the forecasted data, ensuring the first column is correctly named 'extract_date'
    forecast = pd.read_csv(forecast_path)
    forecast.rename(columns={forecast.columns[0]: 'extract_date'}, inplace=True)

    # Load the original data and create a unique mapping of LADs to their latitude and longitude
    original_data = pd.read_csv(original_data_path)
    LAD_lat_lon_ITL_reg = original_data[['LAD', 'Latitude', 'Longitude',"ITL", "Region"]].drop_duplicates()

    # Melting the forecast data to long format
    forecast_long = pd.melt(forecast, id_vars=['extract_date'], var_name='combined', value_name='count')

    # Parsing the 'combined' column to separate LAD, sex, and age
    forecast_long['LAD'] = forecast_long['combined'].apply(lambda x: x.split('_')[0])
    forecast_long['sex'] = forecast_long['combined'].apply(lambda x: x.split('_')[1])
    forecast_long['age_group'] = forecast_long['combined'].apply(lambda x: 'age_' + x.split('_')[-1])

    # Pivot the data to have age groups as columns, keeping 'persons' in the data
    forecast_pivoted = forecast_long.pivot_table(index=['extract_date', 'LAD', 'sex'],
                                                 columns='age_group', values='count', aggfunc='sum').reset_index()

    # Rename columns to match the desired style and convert counts to integers
    forecast_pivoted.columns = [col if isinstance(col, str) else f'age_{col}' for col in forecast_pivoted.columns]
    for col in forecast_pivoted.columns:
        if col.startswith('age_'):
            forecast_pivoted[col] = forecast_pivoted[col].fillna(0).astype(int)

    forecast_pivoted['Country'] = 'England'  
    # Merge with the unique LAD mapping to get latitude and longitude for each LAD
    forecast_merged = pd.merge(forecast_pivoted, LAD_lat_lon_ITL_reg, on='LAD', how='left')
    
    # Combine the original data with the transformed forecast data
    combined_data = pd.concat([original_data, forecast_merged])

    # Optionally, save the combined DataFrame to a new CSV file
    if output_path:
        combined_data.to_csv(output_path, index=False)

    return combined_data

def transform_and_round_forecast_data_CTRY(forecast_path, original_data_path, output_path=None):
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

    original_data = pd.read_csv(original_data_path)
    region_lat_lon = original_data[['Country', 'Latitude', 'Longitude']].drop_duplicates()


    # Melting the forecast data to long format
    forecast_long = pd.melt(forecast, id_vars=['extract_date'], var_name='combined', value_name='count')

    # Parsing the 'combined' column to separate region, sex, and age
    
    forecast_long['sex'] = forecast_long['combined'].apply(lambda x: x.split('_')[0])
    forecast_long['age_group'] = forecast_long['combined'].apply(lambda x: 'age_' + x.split('_')[-1])

    # Pivot the data to have age groups as columns, keeping 'persons' in the data
    forecast_pivoted = forecast_long.pivot_table(index=['extract_date','sex'],
                                                 columns='age_group', values='count', aggfunc='sum').reset_index()

    # Rename columns to match 'prepared_rgn.csv' style and convert counts to integers
    forecast_pivoted.columns = [col if isinstance(col, str) else f'age_{col}' for col in forecast_pivoted.columns]
    for col in forecast_pivoted.columns:
        if col.startswith('age_'):
            forecast_pivoted[col] = forecast_pivoted[col].fillna(0).astype(int)

    # Add the 'Country' column assuming all regions belong to the same country, e.g., 'England'
    forecast_pivoted['Country'] = 'England'  # Example country name
    
    forecast_merged = pd.merge(forecast_pivoted, region_lat_lon, on='Country', how='left')
    # Rearrange columns to match 'prepared_rgn.csv' order
    # Combine the original data with the transformed forecast data
    combined_data = pd.concat([original_data, forecast_merged])

    # Optionally, save the combined DataFrame to a new CSV file
    if output_path:
        combined_data.to_csv(output_path, index=False)

    return combined_data



transformed_data_CTRY = transform_and_round_forecast_data_CTRY('/Users/omeryurttutmus/Desktop/forecast_ctry.csv',"/Users/omeryurttutmus/Desktop/prepared_ctry.csv",'/Users/omeryurttutmus/Desktop/combined_forecast_ctry_sex_age_group.csv')
#transformed_data_region = transform_and_round_forecast_data_region('/Users/omeryurttutmus/Desktop/forecast_Region_sex_age_group.csv', "/Users/omeryurttutmus/Desktop/prepared_rgn.csv",'/Users/omeryurttutmus/Desktop/combined_forecast_Region_sex_age_group.csv')
#transformed_data_ITL = transform_and_round_forecast_data_ITL('/Users/omeryurttutmus/Desktop/forecast_ITL_sex_age_group.csv', "/Users/omeryurttutmus/Desktop/prepared_itl.csv",'/Users/omeryurttutmus/Desktop/combined_forecast_ITL_sex_age_group.csv')
#transformed_data_LAD = transform_and_round_forecast_data_LAD('/Users/omeryurttutmus/Desktop/forecast_lad_sex_age_group-1.csv', "/Users/omeryurttutmus/Desktop/prepared_lad.csv",'/Users/omeryurttutmus/Desktop/combined_forecast_LAD_sex_age_group.csv')