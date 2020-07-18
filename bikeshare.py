import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

Month_list = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']

Weekday_user_choice_list = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']
Weekday_map = { 'mo': 'Monday',
                'tu': 'Tuesday',
                'we': 'Wednesday',
                'th': 'Thursday',
                'fr': 'Friday',
                'sa': 'Saturday',
                'su': 'Sunday'}

def get_city_input():
    """ Get city input from user referring the city list defined """
    exit_msg = 'Exit'
    city_list = list(CITY_DATA.keys())
    city = ""

    print('-'*40)
    for index, city in enumerate(city_list):
        print("* {} : {}".format(index, city.title()))
    print("* {} : {}".format((index + 1), exit_msg))
    
    while True:
        # Read user input
        city = str(input("Input a city name to analyze: ").lower())
        
        if city not in city_list:
            # Check if user choice is to exit
            if city == exit_msg.lower():
                print('Chosen to exit, have a nice day. :)')
                exit(0)
            print("Invalid city, please try again :(")
            continue
        # valid input received, return
        break

    return city

def get_month_input():
    """ Get a particular month or all months as input from user """
    all_months = 'All'
    print('-'*40)
    for index, month in enumerate(Month_list):
        print("* {} : {}".format(index, month.title()))

    print("* {} : {}".format(len(Month_list), all_months))

    month = 'unknown'
    while True:
        # Read user input
        month = str(input("Select a month index to analyze: ")).lower()

        if month not in Month_list:
            if month != all_months.lower():
                print('Incorrect choice. please try again.')
                continue
        # valid input received
        break
    return month

def get_weekday_input():
    """ Get a weekday or all weekdays as input from the user """
    all_days = 'All'
    print('-'*40)
    for index, weekday in enumerate(Weekday_user_choice_list):
        print("* {} : {}".format(index, weekday.title()))        

    print("* {} : {}".format(len(Weekday_user_choice_list), all_days))

    weekday = 'unknown'
    while True:
        # Read user input
        weekday = str(input("Select a weekday index to analyze: ")).lower()

        if weekday not in Weekday_user_choice_list:
            if weekday != all_days.lower():
                print('Incorrect choice. please try again.')
                continue
        # valid input received
        break
    if weekday in Weekday_user_choice_list:
        weekday = Weekday_map[weekday]
    else:
        print('Invalid weekday.')
        exit(1)
    return weekday


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # Print cities to choose from
    city = get_city_input()
    
    # get user input for month (all, january, february, ... , june)
    month = get_month_input()

    # get user input for weekday (all, mo, tu, we, th, fr, sa, su)
    day = get_weekday_input()

    print("User select choice: City = {}, Month = {}, Weekday = {}".format(city.title(), month.title(), day.title()))
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
    
    city = city.lower()
    month = month.lower()
    day = day.title()

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Add columns for month and weekday
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday_name
    
    # Filter base don month selected
    if (month != 'all'):
        # input month is in string format and the month in month column is in int format with 1-12 range
        # Convert month name to month number to match 'month' column format
        if month in Month_list:
            month_no = Month_list.index(month) + 1
            df = df[ df['month'] == month_no]
        else:
            print('Invalid month: {}.'.format(month))
            exit(1)
    
    if (day != 'all'):
        if day in Weekday_map.values():
            df = df[ df['weekday'] == day]
        else:
            print('Invalid weekday: {}.'.format(day) )
            exit(1)
    
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (DataFrame) df - input data frame whose time stistics to be calculated

    """

    print('\n')
    print('*'*40)
    print('Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("TODO {}".format(len(df['month'].mode())))
    popular_month_no = df['month'].mode()[0]
    popular_month_name = Month_list[popular_month_no - 1]
    popular_month_count = df['month'].value_counts()[popular_month_no]
    
    print('- '*40)
    print("{:30s}\t{:15s}".format("Popular Month", "Ride Count"))
    print('- '*40)
    print("{:30s}\t{:<15d}".format(popular_month_name.title(), popular_month_count))

    # display the most common day of week
    popular_weekday = df['weekday'].mode()[0]
    popular_weekday_count = df['weekday'].value_counts()[popular_weekday]
    
    print('\n')
    print('- '*40)
    print("{:30s}\t{:15s}".format("Popular Weekday", "Ride Count"))
    print('- '*40)
    print("{:30s}\t{:<15d}".format(popular_weekday.title(), popular_weekday_count))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = df['hour'].value_counts()[popular_hour]
    
    print('\n')
    print('- '*40)
    print("{:30s}\t{:15s}".format("Popular Hour", "Ride Count"))
    print('- '*40)
    print("{:< 30d}\t{:<15d}".format(popular_hour, popular_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (DataFrame) df - input data frame whose station stistics to be calculated

    """

    print('\n')
    print('*'*40)
    print('Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_counts = df['Start Station'].value_counts()[popular_start_station]

    print('- '*40)
    print("{:30s}\t{:15s}".format("Popular Start Station", "Ride Count"))
    print('- '*40)
    print("{:30s}\t{:<15d}".format(popular_start_station, popular_start_station_counts))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_counts = df['End Station'].value_counts()[popular_end_station]

    print('\n')
    print('- '*40)
    print("{:30s}\t{:15s}".format("Popular End Station", "Ride Count"))
    print('- '*40)
    print("{:30s}\t{:<15d}".format(popular_end_station, popular_end_station_counts))

    # display most frequent combination of start station and end station trip
    df['Start & End Stations'] = df['Start Station'] + ' : ' +  df['End Station']
    popular_start_end_station = df['Start & End Stations'].mode()[0]
    popular_start_end_station_counts = df['Start & End Stations'].value_counts()[popular_start_end_station]
    popular_trip_start_station = popular_start_end_station.split(' : ')[0]
    popular_trip_end_station = popular_start_end_station.split(' : ')[1]
    
    print('\n')
    print('Most frequent combination of start station and end station trip:')
    print('- '*40)
    print("{:25s}\t{:25s}\t{:15s}".format("Popular Start Station", "Popular End Station", "Ride Count"))
    print('- '*40)
    print("{:25s}\t{:25s}\t{:<15d}".format(popular_trip_start_station, popular_trip_end_station, popular_start_end_station_counts))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        (DataFrame) df - input data frame whose trip stistics to be calculated

    """

    print('\n')
    print('*'*40)
    print('Calculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    secs_per_min = 60
    secs_per_hour = secs_per_min * 60
    secs_per_day = secs_per_hour * 24
    secs_per_year = secs_per_day * 365
    
    total_years = int(total_trip_duration/ secs_per_year)
    remaining_secs = total_trip_duration % secs_per_year
    total_days = int(remaining_secs/secs_per_day)
    remaining_secs = remaining_secs % secs_per_day
    total_hours = int(remaining_secs/secs_per_hour )
    remaining_secs = remaining_secs % secs_per_hour
    tot_mins = int(remaining_secs/secs_per_min)
    remaining_secs = remaining_secs % secs_per_min
    print("Total Trip Duration\t: {} seconds ( {} years, {} days, {} hours, {} mins and {} seconds )".format(total_trip_duration, total_years, total_days, total_hours, tot_mins, remaining_secs))

    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    print("\nMean Trip Duration\t: {} seconds".format(mean_trip_duration))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        (DataFrame) df - input data frame whose user stistics to be calculated

    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = dict(df['User Type'].value_counts())
    
    print('- '*20)
    print("{:20s} {:<20s}".format("User Type", "User Count"))
    print('- '*20)
    for user_type, counts in user_type_counts.items():
        print("{:20s} {:<20d}".format(user_type, int(counts)))

    # Display counts of gender
    if 'Gender' in df:
        gender_type_counts = dict(df['Gender'].value_counts())
        print()
        print('- '*20)
        print("{:20s} {:<20s}".format("Gender", "Gender Count"))
        print('- '*20)
        for gender_type, counts in gender_type_counts.items():
            print("{:20s} {:<20d}".format(gender_type, int(counts)))
    else:
        print('\nNOTE: This city database does not have gender information.')


    if 'Birth Year' in df:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])

        print()
        print('- '*40)
        print(' User bith year Stats:')
        print('- '*40)
        print("{:30s} : {}".format('Earliest Year of Birth', earliest_birth_year))
        print("{:30s} : {}".format('Recent Year of Birth', recent_birth_year))
        print("{:30s} : {}".format('Most Common Year of Birth', common_birth_year))
    else:
        print('\nNOTE: This city database does not contain "Birth year" information.')
          
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Displays raw data on bikeshare users if user requests.

    Args:
        (DataFrame) df - input data frame whose contents to be displayed

    """
    rec_pos = 0
    while rec_pos < len(df):
        user_choice = input('\nDo you want to see raw data (5 records at a time)? choose (y/n)?').lower()
        if user_choice == 'n':
            break
        elif user_choice != 'y':
            print('wrong choice!')
            continue
        
        print(df.iloc[rec_pos : (rec_pos + 5)])
        rec_pos += 5

def main():
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
