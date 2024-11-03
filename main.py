import pandas as pd # type: ignore
import numpy as np # type: ignore

def find_top_k_candidates(csv_file, user_responses, k):
    # Load the data from CSV
    df = pd.read_csv(csv_file)
    
    # Separate candidate names and their responses
    candidate_names = df.iloc[:, 0].values  # First column is names
    candidate_responses = df.iloc[:, 1:].values  # Remaining columns are responses (-1, 0, 1)

    # Extract user responses and weights
    user_values = np.array([resp[0] for resp in user_responses])  # user response values
    weights = np.array([resp[1] for resp in user_responses])      # corresponding weights

    # Calculate weighted Euclidean distance for each candidate
    distances = []
    for i, candidate_response in enumerate(candidate_responses):
        distance = np.sqrt(np.sum(weights * (candidate_response - user_values) ** 2))
        distances.append((candidate_names[i], distance))
    
    # Sort by distance, then alphabetically by name for ties
    distances.sort(key=lambda x: (x[1], x[0]))

    # Return top-k candidates in a dictionary
    return {name: dist for name, dist in distances[:k]}


# Example usage with customizable user responses and weights for 46 issues

user_responses = [
    (0.5, 1.2),  # Issue 1 response and weight
    (-0.2, 0.8), # Issue 2 response and weight
    (1.0, 1.1),  # Issue 3 response and weight
    (0.3, 0.9),  # Issue 4 response and weight
    (-1.0, 1.3), # Issue 5 response and weight
    (0.7, 1.0),  # Issue 6 response and weight
    (-0.5, 1.4), # Issue 7 response and weight
    (1.0, 1.2),  # Issue 8 response and weight
    (0.2, 0.7),  # Issue 9 response and weight
    (0.9, 1.1),  # Issue 10 response and weight
    (0.1, 1.3),  # Issue 11 response and weight
    (-0.3, 1.5), # Issue 12 response and weight
    (0.8, 1.0),  # Issue 13 response and weight
    (-0.7, 0.8), # Issue 14 response and weight
    (0.6, 1.4),  # Issue 15 response and weight
    (-0.1, 1.2), # Issue 16 response and weight
    (1.2, 1.0),  # Issue 17 response and weight
    (0.0, 1.1),  # Issue 18 response and weight
    (-1.1, 1.3), # Issue 19 response and weight
    (0.4, 0.9),  # Issue 20 response and weight
    (1.3, 1.2),  # Issue 21 response and weight
    (-0.4, 0.8), # Issue 22 response and weight
    (0.5, 1.1),  # Issue 23 response and weight
    (-0.9, 1.4), # Issue 24 response and weight
    (0.3, 1.0),  # Issue 25 response and weight
    (1.1, 1.3),  # Issue 26 response and weight
    (-1.2, 1.5), # Issue 27 response and weight
    (0.6, 1.0),  # Issue 28 response and weight
    (0.0, 1.1),  # Issue 29 response and weight
    (-0.6, 0.9), # Issue 30 response and weight
    (1.4, 1.2),  # Issue 31 response and weight
    (-0.8, 1.3), # Issue 32 response and weight
    (0.9, 1.4),  # Issue 33 response and weight
    (0.7, 1.1),  # Issue 34 response and weight
    (-0.3, 1.0), # Issue 35 response and weight
    (1.0, 1.2),  # Issue 36 response and weight
    (0.2, 1.3),  # Issue 37 response and weight
    (-0.7, 0.8), # Issue 38 response and weight
    (0.8, 1.1),  # Issue 39 response and weight
    (-1.3, 1.0), # Issue 40 response and weight
    (0.4, 1.2),  # Issue 41 response and weight
    (0.0, 0.9),  # Issue 42 response and weight
    (-0.1, 1.3), # Issue 43 response and weight
    (1.5, 1.4),  # Issue 44 response and weight
    (-0.2, 1.1), # Issue 45 response and weight
    (0.6, 1.5)   # Issue 46 response and weight
]

# Specify the CSV file path and desired number of top candidates (k)
csv_file = "formatted_political_stances.csv"
top_k = 10

# Run the function with your specified responses and weights
top_candidates = find_top_k_candidates(csv_file, user_responses, top_k)
#print(top_candidates)

# Print each top candidate on a new line
for name, dist in top_candidates.items():
    print(f"{name}: {dist}")
