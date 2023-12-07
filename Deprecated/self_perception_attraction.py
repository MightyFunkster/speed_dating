import sqlite3
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.figure_factory as ff

def process_data(cursor, upper_self_rating : int, lower_self_rating : int):
    # Retrieve the distinct iids and genders from the participants table
    cursor.execute('SELECT DISTINCT iid, gender FROM participants')
    result_iids = cursor.fetchall()

    # Initialize lists to store the data for each iid
    avg_attractiveness = []
    success_percentage = []
    avg_attractiveness_diff = []
    success_percentage_diff = []
    var_attractiveness = []
    genders = []
    
    # Iterate over each iid and gender
    for iid, gender in result_iids:
        # Retrieve the date_ids for the current iid from the dates table
        cursor.execute('SELECT date_id FROM dates WHERE iid = ?', (iid,))
        date_ids = cursor.fetchall()
        date_ids = [date_id[0] for date_id in date_ids]

        # Retrieve the dec_o values for the date_ids of the current iid from the dates table
        cursor.execute('SELECT dec_o FROM dates WHERE date_id IN ({})'.format(','.join('?' * len(date_ids))), date_ids)
        dec_o_values = cursor.fetchall()
        dec_o_values = [dec_o[0] for dec_o in dec_o_values]

        # Retrieve the rating_values for attr_id = 1 and calculate the average attractiveness
        cursor.execute('SELECT rating_value FROM ratings WHERE attr_id = 1 AND date_id IN ({})'.format(','.join('?' * len(date_ids))), date_ids)
        rating_values = cursor.fetchall()
        rating_values = [rating[0] for rating in rating_values]
        avg_attr = np.mean(rating_values)
        var_attr = np.var(rating_values)

        # Retrieve the self-rating value for attr_id = 1 and the current iid
        cursor.execute('SELECT self_rating_value FROM self_ratings WHERE attr_id = 1 AND iid = ?', (iid,))
        self_rating_value = cursor.fetchone()[0]

        # Calculate the difference between the self-rating value and the average attractiveness
        if upper_self_rating > self_rating_value > lower_self_rating:
            avg_attr_diff = self_rating_value - avg_attr
            avg_attractiveness_diff.append(avg_attr_diff)
            success_percent_diff = (sum(dec_o_values) / len(dec_o_values)) * 100
            success_percentage_diff.append(success_percent_diff)

        # Calculate the percentage of successful matches
        success_percent = (sum(dec_o_values) / len(dec_o_values)) * 100

        # Append the average attractiveness, success percentage, and variance to the respective lists
        avg_attractiveness.append(avg_attr)
        var_attractiveness.append(var_attr)
        success_percentage.append(success_percent)
        genders.append(gender)
        
    return avg_attractiveness, success_percentage, avg_attractiveness_diff, success_percentage_diff, var_attractiveness, genders



def filter_data_by_gender(data, genders, target_gender):
    filtered_data = [value for value, gender in zip(data, genders) if gender == target_gender]
    return filtered_data

def create_scatter_plot(avg_attr, success_percent, genders):
    men_avg_attr = filter_data_by_gender(avg_attr, genders, 1)
    men_success_percent = filter_data_by_gender(success_percent, genders, 1)
    women_avg_attr = filter_data_by_gender(avg_attr, genders, 0)
    women_success_percent = filter_data_by_gender(success_percent, genders, 0)
    
    # Create scatter plots for each gender
    men_scatter = go.Scatter(
        x=men_avg_attr,
        y=men_success_percent,
        mode='markers',
        name='Male',
        marker=dict(color='#003f5c', size=14)
    )

    women_scatter = go.Scatter(
        x=women_avg_attr,
        y=women_success_percent,
        mode='markers',
        name='Female',
        marker=dict(color='#ff6361', size=14)
    )

    # Create the figure
    fig = go.Figure(data=[men_scatter, women_scatter])

    # Set the layout
    fig.update_layout(
        xaxis=dict(title='Average Attractiveness Rating Received'),
        yaxis=dict(title='Percentage of Successful Second Dates'),
        title='Influence of Average Attractiveness Rating Received on Second Date Success',
        legend=dict(title='Gender', orientation='h', yanchor='bottom', y=1, xanchor='right', x=1),
        plot_bgcolor='#dadfe1',
        paper_bgcolor='#dadfe1',
        showlegend=False
    )

    # Show the plot
    fig.show()


def create_bell_curve_plot(var_attr, genders):
    men_var_attr = filter_data_by_gender(var_attr, genders, 1)
    women_var_attr = filter_data_by_gender(var_attr, genders, 1)
    # Create histogram data for men and women
    hist_data = [men_var_attr, women_var_attr]

    # Group labels
    group_labels = ['Men Attraction Variance', 'Women Attraction Variance']

    # Create the bell curve plot
    fig = ff.create_distplot(hist_data, group_labels, show_hist=False, curve_type='normal', colors=['#003f5c', '#ff6361'])

    # Update the layout
    fig.update_layout(
        title='Attraction Variance by Gender (Bell Curve)',
        xaxis=dict(title='Attraction Variance'),
        yaxis=dict(title='Density'),
        template='plotly_white',
        plot_bgcolor = '#dadfe1',
        paper_bgcolor = '#dadfe1'
    )

    # Show the plot
    fig.show()

# Connect to the SQLite database
conn = sqlite3.connect('speed_dating.db')
cursor = conn.cursor()

# Get the processed data
avg_attractiveness, success_percentage, avg_attractiveness_diff, success_percentage_diff, var_attractiveness, genders = process_data(cursor, 10.1, 5.5)


# Example usage:
create_scatter_plot(avg_attractiveness, success_percentage, genders)
create_scatter_plot(avg_attractiveness_diff, success_percentage_diff, genders)
create_bell_curve_plot(var_attractiveness, genders)

conn.commit()
conn.close()
