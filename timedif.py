import datetime

# Example epoch times (in seconds)
epoch_time1 = 1633072800  # Example epoch time 1
epoch_time2 = 1633076400  # Example epoch time 2
1741576049000
# Convert epoch times to datetime objects
date_time1 = datetime.datetime.fromtimestamp(epoch_time1)
date_time2 = datetime.datetime.fromtimestamp(epoch_time2)

# Print the datetime objects
print("Datetime 1:", date_time1)
print("Datetime 2:", date_time2)

# Calculate the difference between the two datetime objects
time_difference = date_time2 - date_time1

# Convert the difference to minutes
difference_in_minutes = time_difference.total_seconds() / 60

print(f"The difference between the two epoch times is {difference_in_minutes} minutes.")