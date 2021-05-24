import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = 'all'
    month = 'all'
    day = 'all'

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        raw_city = input("Would you like to see data for Chicago, New York or Washington?:")
        if raw_city.lower() not in ('chicago', 'new york', 'washington'):
            print("Not an appropriate choice, please try again!")
        else:
            break

    if raw_city.lower() == 'chicago':
        city = 'chicago'
    elif  raw_city.lower() == 'new york':
        city = 'new york city'
    else: 
        city = 'washington'

    
    #HINT: Use a while loop to handle invalid inputs
    while True:
        filter_type = input("Would you like to filter the data by month, day, both or not at all? Type \"none\" for not time filter:")
        if filter_type.lower() not in ('month', 'day', 'both', 'none'):
            print("Not an appropriate choice, please try again!")
        else:
            break
    if filter_type.lower() in ('month', 'both'):
    # get user input for month (all, january, february, ... , june)
        while True:
            raw_month = input("which month? January, February, March, April, May, or June? Please type out the full month name.")
            if raw_month.lower() not in ('january', 'february', 'march', 'april', 'may', 'june'):
                print("Not an appropriate choice, please try again!")
            else:
                break   
        month = raw_month.lower()
    
    if filter_type.lower() in ('day', 'both'):
        while True:
            try:
                raw_day = int(input("which day? Please type your response as an integer (e.g., 1 = Sunday). "))
                if raw_day > 7 or raw_day < 1:
                    print("Not an appropriate choice, please try again!")
                    continue
                else:
                    break 
            except ValueError:
                print("Sorry, I didn't understand that.")
                continue
            except TypeError:
                print("Sorry, I didn't understand that.")
                continue     
        #age was successfully parsed!
        #we're ready to exit the loop
        week   = ['Sunday', 
              'Monday', 
              'Tuesday', 
              'Wednesday', 
              'Thursday',  
              'Friday', 
              'Saturday']
    # get user input for day of week (all, monday, tuesday, ... sunday)
        day = week[raw_day-1]
    print('-'*40)
    return city, month, day
      

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
   
    # extract month and day of week from Start Time to create new columns
    #weekday_name replace as day_name
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() 


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    
    Args: 
        df - Pandas DataFrame containing city data filtered by month and day
    """


    print('\nCalculating The Most Frequent Times of Travel...\n')
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    start_time = time.time()

    # display the most common month
    popular_month = df['month'].value_counts().keys().tolist()[0]
    popular_month_count = df['month'].value_counts().tolist()[0]

    print('Most frequent start month is {}, which was called {} times.'.format(popular_month, popular_month_count))
        
    # display the most common day of week
    popular_day = df['day_of_week'].value_counts().keys().tolist()[0]
    popular_day_count = df['day_of_week'].value_counts().tolist()[0]
    print('Most frequent start day is {}, which was called {} times.'.format(popular_day, popular_day_count))
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].value_counts().keys().tolist()[0]
    popular_hour_count = df['hour'].value_counts().tolist()[0]
    print('Most frequent start hour is {}, which was called {} times.'.format(popular_hour, popular_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args: 
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().keys().tolist()[0]
    popular_start_station_count = df['Start Station'].value_counts().tolist()[0]
    print('most commonly used start station is {}, Count: {}'.format(popular_start_station,  popular_start_station_count))

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().keys().tolist()[0]
    popular_end_station_count = df['End Station'].value_counts().tolist()[0]
    print('most commonly used end station is {}, count: {}'.format(popular_end_station,popular_end_station_count))
    # display most frequent combination of start station and end station trip

    trip_turple = zip(df['Start Station'], df['End Station'])
    df['Trip'] = list(trip_turple)
    poplular_trip = df['Trip'].value_counts().keys().tolist()[0]
    poplular_trip_count = df['Trip'].value_counts().tolist()[0]
    print('most frequent combination of start station and end station trip is {}, count: {}'.format(poplular_trip,poplular_trip_count))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    trip_duration_sum = df['Trip Duration'].sum()
    trip_duration_avg = df['Trip Duration'].mean()
    trip_duration_count = df['Trip Duration'].count()
    # display total travel time
    print('Totoal Duration: {}, count: {}, Average Duration: {}'.format(trip_duration_sum,trip_duration_count,trip_duration_avg))     
    # display mean travel time

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    len_type = len(df['User Type'].value_counts().keys().tolist())

    for i in range(len_type):
        print('User Type: {},  Count: {}'.format(df['User Type'].value_counts().keys().tolist()[i], df['User Type'].value_counts().tolist()[i]))

    # Display counts of gender
    if 'Gender' in df.columns.values.tolist():
        len_gender = len(df['Gender'].value_counts().keys().tolist())
        for i in range(len_gender):
            print('{}: {}'.format(df['Gender'].value_counts().keys().tolist()[i], df['Gender'].value_counts().tolist()[i]))
    else: 
        print('No gender data to share')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns.values.tolist():
        oldest_birth_year = df['Birth Year'].min()
        youngest_birth_year = df['Birth Year'].max ()
        most_common_birth_year =  df['Birth Year'].value_counts().keys().tolist()[0]
        print("What is the oldest, youngest, and most poplular year of birth?")
        print('({}, {}, {})'.format(oldest_birth_year,youngest_birth_year,  most_common_birth_year))
    else:
        print('No birth year data to share')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
     """Displays 5 lines of raw data."""

    # Interact with the user to view the invividual trip data    
     view_option_raw = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')

     # Assign the start_loc and get the row number 
     start_loc = 0
     count_row = df.shape[0]

     # Set the view_option boolean variable according to the user input
     if view_option_raw.lower() not in ('yes', 'no'):
        print("Sorry, I can't understand your choice. No trip data could be displayed! ")
        view_option = False
     elif view_option_raw.lower() == 'yes':
        view_option = True
     else:
        view_option = False

     # View the trip data until the end row, once the view option are changed by user, break the loop   
     while view_option: 
             if  start_loc + 5 >= count_row:
                 if  start_loc < count_row:
                     print(df.iloc[start_loc:count_row])
                 print ('All data were displayed!')
                 break  
             else:
                  print(df.iloc[start_loc:start_loc+5])
             start_loc += 5 
             view_display = input('Do you wish to continue?Enter yes or no\n: ')    
             if view_display.lower() == 'yes':
                 view_option = True
             elif view_display.lower() == 'no':
                 view_option = False
             else:
                 print("Sorry, I can't understand your option, No more trip data will be displayed!")
                 view_option = False
    


def main():
    #set maximal displayed column using the function set_option
    pd.set_option('display.max_columns',200)
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
