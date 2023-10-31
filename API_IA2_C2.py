import requests
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Get the current date
current_date = datetime.now()

# Define the year and month to retrieve data
year = 2021
month = 1

# API endpoint URL
endpoint_url = f"https://api.bnm.gov.my/public/msb/1.24/year/{year}"

# Make API request
headers = {
    "Accept": "application/vnd.BNM.API.v1+json"
}
response = requests.get(endpoint_url, headers=headers)

# Check if the API request was successful
if response.status_code == 200:
    # Load JSON data
    data = json.loads(response.text)
    
    # Extract the data for the specified month
    month_data = data['data']
    
    # Create a DataFrame from the extracted data
    df = pd.DataFrame(month_data)

    # Convert numeric columns to appropriate data types and divide by 1000
    numeric_columns = ['dem_depo', 'fix_special_gen_inv_depo', 'for_curr_depo','nego_inst_depo_isu','twrq_fix_depo', 'sav_depo','oth_depo_acpt']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric) / 1000
    
     # Calculate total for each month and add it as a new column
    df['total'] = df[numeric_columns].sum(axis=1)
    
    # Set 'year_dt' and 'month_dt' as the index for the DataFrame
    df.set_index(['year_dt', 'month_dt'], inplace=True)
    print (df)
    
    # Plot a stacked bar chart
    plt.figure(figsize=(8, 6))
    ax = df[numeric_columns].plot(kind='bar', stacked=True)
    
    # Add data labels to the center of each bar (divided by 1000)
    for p in ax.patches:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy() 
        ax.annotate(f'{height:.2f}K', (x + width/2, y + height/2), ha='center')
    
    # Plot the total as a line chart
    df['total'].plot(kind='line', marker='o', linewidth=2, color='black', linestyle='dashed', ax=ax)
    for i, txt in enumerate(df['total']):
        ax.annotate(f'{txt:.2f}K', (df.index[i][1] - 1, txt), textcoords="offset points", xytext=(10,10), ha='center')
    plt.title(f'Deposit by Categories for {year} (Values in Thousands)')
    plt.xlabel('Year, Month')
    plt.ylabel('Amount (RMx1000)')
    
    # Set custom lower and upper limits for the y-axis
    lower_limit = 50  # Set your custom lower limit here
    upper_limit = max(df['total']) + 50  # Set your custom upper limit here
    
    ax.set_ylim(lower_limit, upper_limit)
    
    plt.legend(loc='upper left', bbox_to_anchor=(1.1, 1))
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    plt.show()
else:
    print(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")