import time
import pandas as pd

CITY_DATA = {'CHICAGO': 'chicago.csv',
             'NEW YORK CITY': 'new_york_city.csv',
             'WASHINGTON': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input(
            "\n\nEnter the City to get data about?\nNew York City, Chicago or Washington?\n")
        city = city.upper()
        if city not in ('NEW YORK CITY', 'CHICAGO', 'WASHINGTON'):
            print("Name not in my list, kindly try\nNew York City, Chicago or Washington")
            continue
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)

    while True:
        month = input(
            "\nWhich month would you like to filter by? January, February, March, April, May, June or type 'all' if you do not have any preference?\n")
        month = month.lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("Sorry, I didn't catch that. Try again.")
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input("\nAre you looking for a particular day? If so, kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you do not have any preference.\n")
        day = day.lower()
        if day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
            print("Sorry, I didn't catch that. Try again.")
            continue
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        the inputs specified accepts both lower and uppercase letters
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    # TO DO: display the most common day of week

    popular_day = df['day_of_week'].mode()[0]
    print('Most Common day:', popular_day)

    # TO DO: display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most used Start station:', Start_Station)

    # TO DO: display most commonly used end station

    End_Station = df['End Station'].value_counts().idxmax()
    print('\nMost used End Station:', End_Station)

    # TO DO: display most frequent combination of start station and end station trip

    Most_Combined_Station = df.groupby(['Start Station', 'End Station']).count()
    print('\nMost Common combination of start and end station trip:',
          Start_Station, " & ", End_Station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total travel time:', Total_Travel_Time/86400, " Days")

    # TO DO: display mean travel time

    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean travel time:', Mean_Travel_Time/60, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    user_types = df['User Type'].value_counts()
    # print(user_types)
    print('User Types:\n', user_types)

    # TO DO: Display counts of gender

    try:
        gender_types = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_types)
    except KeyError:
        print("\nGender Types:\nNo data available for this month.")

    # Displaying the number of gender type for each User type

    try:
        user_type_gender = df.groupby(['User Type', 'Gender'])[
            'Gender'].count()
        print('\nUser types and their Genders:\n', user_type_gender)
        print()
    except KeyError:
        print("\nUser types and their Genders:\nNo data available for this Part")

    # Displaying the youngest user for each user type by gender
    try:
        youngest_user_type_gender = df.groupby(["User Type", "Gender"])[
            'Birth Year'].min()
        print('\nYoungest User for each Gender of specific user Type\n',
              youngest_user_type_gender)
    except:
        print("\nYounger User for each Gender of specific user type:\nNo data available for this Part")
    
    # Displaying the oldest user for each user type by gender
    try:
        oldest_user_type_gender = df.groupby(["User Type", "Gender"])['Birth Year'].max()
        print('\nOldest User for each Gender of specific user Type\n', oldest_user_type_gender)
    except:
        print("\nOldest User for each Gender of specific user type:\nNo data available for this Part")

    # TO DO: Display earliest, most recent, and most common year of birth

    try:
        Earliest_Year = df['Birth Year'].min()
        print('\nEarliest Year:', Earliest_Year)
    except KeyError:
        print("\nEarliest Year:\nNo data available for this month.")

    try:
        Most_Recent_Year = df['Birth Year'].max()
        print('\nMost Recent Year:', Most_Recent_Year)
    except KeyError:
        print("\nMost Recent Year:\nNo data available for this month.")

    try:
        Most_Common_Year = df['Birth Year'].value_counts().idxmax()
        print('\nMost Common Year:', Most_Common_Year)
    except KeyError:
        print("\nMost Common Year:\nNo data available for this month.")

    try:
        Most_Common_Gender_Year = df.groupby(['Birth Year', 'Gender'])[
            'Gender'].count()
        print('\nNumber of People by gender and Year :\n', Most_Common_Gender_Year)
    except KeyError:
        print(
            "\nNumber of People by Gender and Year:\nNo data available for your Selection.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_rawdata(df):
    """ Asks User whether to display the city's raw data, 5 rows at a goal
    input = 'string'; 
    Output = 'dataframe of cities data' = yes displays 5 rows at a time and no breaks away from the function
    """
    raw_data = 0
    get_data = input(
        '\nWould you like to see some raw data? Enter yes / no.\n')
    get_data = get_data.lower()
    while get_data.lower() == 'yes':
        print("\nDimension of the Raw Data")
        df_length = print(df.shape)
        df_slice = df.iloc[raw_data: raw_data+5]
        print('\n', df_slice)
        raw_data += 5
        more_data = input(
            '\nWould you like to see more of this? Enter yes / no.\n')
        more_data = more_data.lower()
        if more_data == 'no':
            get_data = 'no'


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_rawdata(df)
#         gen_description(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
