import requests
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Get the current date
current_date = datetime.now()

# Define the endpoint URL with the start year and month and the current year and month
start_year = 2021
start_month = 1
current_year = 2021
current_month = 12

# Create a list to store the data for each month
data_list = []

# Loop through the months from the start date to the current date
while start_year <= current_year or (start_year == current_year and start_month <= current_month):
    endpoint_url = f"https://api.bnm.gov.my/public/msb/1.24/year/{start_year}"
    headers = {
        "Accept": "application/vnd.BNM.API.v1+json"
    }
    response = requests.get(endpoint_url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        data_list.append(data)
    else:
        print(f"Failed to retrieve data for year {start_year}. HTTP Status Code: {response.status_code}")

    if start_month == 12:
        start_year += 1
        start_month = 1
    else:
        start_month += 1

# Extracted Json data
json_data = data_list

# Extract the 'data' part for time series
data_list = [item['data'] for item in json_data]

# Flatten the list of dictionaries
flat_data_list = [entry for sublist in data_list for entry in sublist]

# Create a DataFrame
df = pd.DataFrame(flat_data_list)

# Sort the DataFrame by 'date' in ascending order
df.sort_values(by='month_dt', inplace=True)

# Set 'date' column as the index
df.set_index('month_dt', inplace=True)

# Convert 'dem_depo' values to numeric (float) and then divide by 1000
df['dem_depo'] = pd.to_numeric(df['dem_depo'])/1000
print(df)

# Now, you can use this DataFrame for time series charting with matplotlib
plt.figure(figsize=(15, 7.5))
plt.plot(df.index, df['dem_depo'], marker='o', linestyle='-')

# Add data labels to the points
for i, txt in enumerate(df['dem_depo']):
    # Iterate through the DataFrame using iterrows() method
    for index, row in df.iterrows():
        plt.text(index, row['dem_depo'], f'{row["dem_depo"]:.2f}K', ha='center')
plt.title('Demand Deposit 2021')
plt.xlabel('Month')
plt.ylabel('Grand Total (RM in Thousands )')
plt.grid(True,color='lightgray')  # Customize grid lines color
plt.legend()

# Configure x-axis labels to display at regular intervals
ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True, prune='both'))

y_format = ticker.FuncFormatter(lambda x, pos: f'{x:,.2f}K')  # Formats y-values with commas and no decimal places
plt.gca().yaxis.set_major_formatter(y_format)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()