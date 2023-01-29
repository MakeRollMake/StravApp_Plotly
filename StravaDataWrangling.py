import pandas as pd
import polyline

# read csv file
df = pd.read_csv('Data/activities.csv')

# drop unwanted columns
drop_columns = ['workout_type', 'location_city', 'utc_offset', 'location_city', 'location_state',
                'location_country', 'trainer', 'commute', 'manual', 'gear_id', 'has_heartrate',
                'heartrate_opt_out', 'display_hide_heartrate_option', 'from_accepted_tag']
df = df.drop(columns=drop_columns)

# convert to datetime format
# converts the start_date_local columns to a datetime format
df['start_date_local'] = pd.to_datetime(df['start_date_local'])
# creates 2 new columns for date and time
df['start_date'] = df['start_date_local'].dt.date
df['start_time'] = df['start_date_local'].dt.time
# converts the 'start_date' column to datetime format
df['start_date'] = pd.to_datetime(df['start_date'])

# speed conversion from m/s to km/h
df['average_speed'] = df['average_speed'] * 3.6
df['max_speed'] = df['max_speed'] * 3.6

# Delete rows where 'average_speed' column is greater than 100 (geolocalisation bug during workout)
df.drop(df[(df['average_speed'] > 100) & (df['type'] == 'Ride')].index, inplace=True)

# creates a second df_demo with only activities with GPX values
# drop rows with Nan values in the map.summary_polyline
df_map = df.dropna(subset=['map.summary_polyline'])

# add decoded summary polylines to create a list of latitude and longitude coordinates
df_map['map.polyline'] = df_map['map.summary_polyline'].apply(polyline.decode)


# Saves the dataframes to a new csv file
df.to_csv('Data/activities_clean.csv')
df_map.to_csv('Data/activities_clean_map.csv')
