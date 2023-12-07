import sqlite3
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_success_rate(database):
    # Connect to the SQLite database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Retrieve the distinct self_rating values for attr_id = 1 from the self_ratings table
    cursor.execute('SELECT DISTINCT self_rating_value FROM self_ratings WHERE attr_id = 1')
    self_ratings = cursor.fetchall()
    self_ratings = [self_rating[0] for self_rating in self_ratings]

    # Initialize dictionaries to store the success percentages for each self-rating category for males and females
    success_percentages_males = {self_rating: [] for self_rating in self_ratings}
    success_percentages_females = {self_rating: [] for self_rating in self_ratings}

    # Iterate over each self-rating category
    for self_rating in self_ratings:
        # Retrieve the iids for the current self-rating category from the self_ratings table
        cursor.execute('SELECT iid FROM self_ratings WHERE attr_id = 1 AND self_rating_value = ?', (self_rating,))
        iids = cursor.fetchall()
        iids = [iid[0] for iid in iids]

        # Iterate over each iid in the current self-rating category
        for iid in iids:
            # Retrieve the gender for the current iid from the participants table
            cursor.execute('SELECT gender FROM participants WHERE iid = ?', (iid,))
            gender = cursor.fetchone()[0]

            # Retrieve the date_ids for the current iid from the dates table
            cursor.execute('SELECT date_id FROM dates WHERE iid = ?', (iid,))
            date_ids = cursor.fetchall()
            date_ids = [date_id[0] for date_id in date_ids]

            # Retrieve the dec_o values for the date_ids of the current iid from the dates table
            cursor.execute('SELECT dec_o FROM dates WHERE date_id IN ({})'.format(','.join('?' * len(date_ids))), date_ids)
            dec_o_values = cursor.fetchall()
            dec_o_values = [dec_o[0] for dec_o in dec_o_values]

            # Calculate the success percentage for the current iid based on gender
            success_percent_iid = (sum(dec_o_values) / len(dec_o_values)) * 100

            if gender == 1:  # Male
                success_percentages_males[self_rating].append(success_percent_iid)
            elif gender == 0:  # Female
                success_percentages_females[self_rating].append(success_percent_iid)

    # Close the connection
    conn.close()

    # Extract success percentages for males and females
    male_success_percentages = [success_percentages_males[value] for value in sorted(self_ratings)]
    female_success_percentages = [success_percentages_females[value] for value in sorted(self_ratings)]
    self_ratings.sort()

    # Convert to DataFrame
    data_males = []
    data_females = []
    for i, rating in enumerate(self_ratings):
        for percentage in male_success_percentages[i]:
            data_males.append([percentage, rating, 'male'])
        for percentage in female_success_percentages[i]:
            data_females.append([percentage, rating, 'female'])

    df_males = pd.DataFrame(data_males, columns=['success_percentage', 'self_rating', 'gender'])
    df_females = pd.DataFrame(data_females, columns=['success_percentage', 'self_rating', 'gender'])

    df = pd.concat([df_males, df_females], ignore_index=True)

    # Specify the desired axis and legend titles
    x_axis_title = "Self Rating of Attractiveness"
    y_axis_title = "Percentage of Successful Second Dates"
    color_legend_title = "Gender"
    plot_title = 'Relationship Between Self-Rating of Attractiveness and Success Rate'

    # Create the box plot
    fig = px.box(df, x="self_rating", y="success_percentage", color="gender", boxmode='group')

    # Update the marker colors for each gender
    fig.for_each_trace(lambda t: t.update(marker_color="#003f5c", marker_line=dict(width=2)) if t.name == "male" else t.update(marker_color="#ff6361", marker_line=dict(width=2)))

    # Update the layout with the desired titles
    fig.update_layout(
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        coloraxis_colorbar_title=color_legend_title,
        title=plot_title,
        paper_bgcolor='#dadfe1',
        plot_bgcolor='#dadfe1'
    )

    # Show the plot
    fig.show()
plot_success_rate('speed_dating.db')
