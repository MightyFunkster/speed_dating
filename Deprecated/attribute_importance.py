import sqlite3
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
import plotly.graph_objects as go

# Retrieve various ratings of various attributes
def retrieve_attribute_ratings(cursor, attribute_count):
    # Generate attribute columns and joins dynamically
    attribute_columns = [f'r{i}.rating_value AS attr{i}_rating' for i in range(1, attribute_count + 1)]
    attribute_joins = ' '.join([f'JOIN ratings AS r{i} ON d.date_id = r{i}.date_id AND r{i}.attr_id = {i}' for i in range(1, attribute_count + 1)])

    # Construct the query
    query = f'''
        SELECT d.date_id, {', '.join(attribute_columns)}, d.dec_o, p.gender
        FROM dates AS d
        {attribute_joins}
        JOIN participants AS p ON d.iid = p.iid
    '''

    # Execute the query and fetch the results
    cursor.execute(query)
    rows = cursor.fetchall()

    return rows

def process_data(rows):
    # Separate the attribute ratings and match outcomes into separate arrays
    X = []
    y = []
    genders = []
    
    # Iterate through the rows and append the values to the respective arrays
    for row in rows:
        date_id = row[0]
        attr_ratings = row[1:6]  # Extract attribute ratings from the row
        match_outcome = row[6]
        gender = row[7]
        
        X.append(attr_ratings)
        y.append(match_outcome)
        genders.append(gender)

    # Convert the arrays to numpy arrays
    X = np.array(X)
    y = np.array(y)
    genders = np.array(genders)
    
    # Separate the data for men and women
    men_indices = np.where(genders == 1)[0]
    women_indices = np.where(genders == 0)[0]
    
    X_men = X[men_indices]
    y_men = y[men_indices]
    
    X_women = X[women_indices]
    y_women = y[women_indices]
    return X_men, y_men, X_women, y_women


def train_and_evaluate(X, y):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a random forest regressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Fit the model to the training data
    model.fit(X_train, y_train)

    # Predict on the test data
    y_pred = model.predict(X_test)

    # Calculate the mean squared error
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)

    # Get the feature importances from the random forest model
    feature_importances = model.feature_importances_

    # Convert the continuous predictions to binary class labels using a threshold
    y_pred_binary = (y_pred > 0.5).astype(int)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred_binary)
    print("Accuracy:", accuracy)

    return feature_importances


def create_bar_plot(feature_importances_men, feature_importances_women):
    # Set the bar width
    bar_width = 0.35

    # Create the bar plot for men
    men_bars = go.Bar(
        x=np.arange(len(feature_importances_men)),
        y=feature_importances_men,
        width=bar_width,
        name='Men',
        marker=dict(color='#003f5c')
    )

    # Create the bar plot for women
    women_bars = go.Bar(
        x=np.arange(len(feature_importances_women)) + bar_width,
        y=feature_importances_women,
        width=bar_width,
        name='Women',
        marker=dict(color='#ff6361')
    )

    # Define the layout
    layout = go.Layout(
        xaxis=dict(
            tickvals=np.arange(len(feature_importances_men)) + bar_width / 2,
            ticktext=['Attractive', 'Sincere', 'Intelligent', 'Fun', 'Ambitious'],
            title='Attributes'
        ),
        yaxis=dict(
            title='Relative Feature Importance'
        ),
        title='Feature Importance for Successful Second Date Prediction',
        barmode='group',
        legend=dict(title='Gender'),
        plot_bgcolor='#dadfe1',
        paper_bgcolor='#dadfe1'
    )

    # Create the figure
    fig = go.Figure(data=[men_bars, women_bars], layout=layout)

    # Show the plot
    fig.show()
    
# Connect to the SQLite database
conn = sqlite3.connect('speed_dating.db')
cursor = conn.cursor()

# Get attribute ratings
rows = retrieve_attribute_ratings(cursor, 5)

# Process rows
men_attribute_ratings, men_match_outcomes, women_attribute_ratings, women_match_outcomes = process_data(rows)

# Call the function for men
feature_importances_men = train_and_evaluate(men_attribute_ratings, men_match_outcomes)

# Call the function for women
feature_importances_women = train_and_evaluate(women_attribute_ratings, women_match_outcomes)

# Plot
create_bar_plot(feature_importances_men, feature_importances_women)
