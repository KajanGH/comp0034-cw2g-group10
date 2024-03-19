import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Load the data
df = pd.read_csv('/Users/omeryurttutmus/Desktop/prepared_rgn.csv', parse_dates=['extract_date'])
df.sort_values('extract_date', inplace=True)

# Filter the data to start from '2017-04-01'
start_date = pd.to_datetime('2017-04-01')
df = df[df['extract_date'] >= start_date]

# Iterate through each Region and process the data
forecasts = {}
forecast_data = pd.DataFrame()  # DataFrame to store all forecasts
for Region in df['Region'].unique():
    for sex in df['sex'].unique():
        # Filter the DataFrame for the current Region and sex
        Region_sex_df = df[(df['Region'] == Region) & (df['sex'] == sex)]

        # Drop duplicate dates within this Region-sex specific DataFrame
        Region_sex_df = Region_sex_df.drop_duplicates(subset='extract_date')

        # Check if 'extract_date' is in the DataFrame columns
        if 'extract_date' not in Region_sex_df.columns:
            print(f"Warning: 'extract_date' not found in columns for Region {Region}, sex {sex}. Skipping.")
            continue

        # Set the index to 'extract_date' and set the frequency
        Region_sex_df['extract_date'] = pd.to_datetime(Region_sex_df['extract_date'])
        Region_sex_df.set_index('extract_date', inplace=True)

        # Use forward fill for missing values
        Region_sex_df = Region_sex_df.ffill()

        # Check for NaN values in the 'sex' column
        if Region_sex_df[['sex']].isnull().values.any():
            print(f"NaN values found in Region {Region}, sex {sex} data. Check and handle missing values.")
            continue

        for age_col in [col for col in Region_sex_df.columns if 'age_' in col]:
            # Check for NaN values in the current age column
            if Region_sex_df[age_col].isnull().values.any():
                print(f"NaN values found in Region {Region}, sex {sex}, {age_col}. Check and handle missing values.")
                continue

            # Create a specific series for each Region, sex, and age group
            series = Region_sex_df[age_col]

            if len(series) < 2 * 12:  # Ensure at least two full years of data
                print(f"Not enough data for Region {Region}, sex {sex}, {age_col} to estimate seasonality.")
                continue

            # Fit the Exponential Smoothing model
            fitted_model = ExponentialSmoothing(series, trend='add', seasonal='add', seasonal_periods=12).fit()

            # Generate forecasts for the next two years (adjust as needed)
            future_periods = 24  # Forecast for the next two years
            forecast_key = f"{Region}_{sex}_{age_col}"
            forecasts[forecast_key] = fitted_model.forecast(future_periods)

            # Append the forecasted data to the DataFrame
            forecast_data[forecast_key] = forecasts[forecast_key]

# Export the forecasted data to a CSV file
forecast_data.to_csv('/Users/omeryurttutmus/Desktop/forecast_Region_sex_age_group.csv')
