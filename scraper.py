import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import os
import random 
import time
import csv

def get_first_search_result(query):
    """
    Searches Google for the given query and retrieves the first result's link.

    This function constructs a Google search URL based on the provided query, sends an HTTP GET request, 
    and parses the response to find the first result link. It handles cases where the link is missing 
    or inaccessible due to rate limiting.

    Parameters:
    query (str): The search query string.

    Returns:
    str or None: The URL of the first search result if found, otherwise None if the link is missing or
    there is an error fetching results.
    """
    
    query = query.replace(' ', '+')
    url = f'https://www.google.com/search?q={query}'

    # Rotate user agents to mimic different browsers
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/85.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36'
    ]

    headers = {'User-Agent': random.choice(user_agents)}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        first_result = soup.find('h3')

        if first_result:
            parent_a_tag = first_result.find_parent('a')
            if parent_a_tag and 'href' in parent_a_tag.attrs:
                link = parent_a_tag['href']
                parsed_url = urlparse(link)
                main_url = parse_qs(parsed_url.query).get('url', [link])[0]
                return main_url
            else:
                print("No valid link found for this query.")
                return None
        else:
            print("No search results found for this query.")
            return None  # No results found
    else:
        print(f"Error fetching results, status code: {response.status_code}")
        return None  # Error fetching results

def process_legislators(input_file, output_file):
    """
    Reads an Excel file of legislators, searches for each legislator's "Political Courage Test" link, 
    and saves the results to a CSV file.

    This function reads the legislator names from the specified Excel file (expects 'first_name' and 'last_name' 
    as the first two columns), constructs a search query for each name, and retrieves the first result link using 
    the `get_first_search_result` function. It stores the names and links in a CSV file, with progress printed to 
    the console.

    Parameters:
    input_file (str): Path to the Excel file containing legislator names (first and last name columns).
    output_file (str): Path to the CSV file where the names and retrieved links will be saved.

    Returns:
    None
    """
    # Read the Excel file
    df = pd.read_excel(input_file, usecols=[5])  # Assuming the first two columns are 'last_name' and 'first_name'
    
    results = []
    total_legislators = len(df)

    for index, row in df.iterrows():
        full_name = row['full_name']
        query = f"just facts vote smart candidate political courage test {full_name}"
        link = get_first_search_result(query)
        name = f"{full_name}"
        results.append({"name": name, "link": link})

        # Print progress
        print(f"Processed {index + 1}/{total_legislators}: {name} -> {link}")

    # Check if the output file already exists
    file_exists = os.path.isfile(output_file)

    # Create a DataFrame from the results
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, mode='a', header=not file_exists, index=False)  # Append to CSV without index

def update_missing_links(input_file):
    """
    Reads a CSV file of legislators with potentially missing links, re-runs search queries for missing entries, 
    and updates the file with newly fetched links.

    This function opens the specified CSV file, iterates over each row to check for missing links, and re-queries 
    Google for those entries to retrieve the first search result link. It then saves the updated information back 
    to the CSV file.

    Parameters:
    input_file (str): The file path of the CSV file to read and update.

    Returns:
    None
    """

    # Load the existing CSV file
    df = pd.read_csv(input_file)
    
    # Iterate through the rows and check for empty or None links
    for index, row in df.iterrows():
        name = row['name']
        link = row['link']
        
        # If the link is empty or None, re-run the search query
        if pd.isna(link) or link == "None":
            first_name, last_name = name.split(" ", 1)
            query = f"just facts vote smart candidate political courage test {first_name} {last_name}"
            print(f"Updating link for {name}...")  # Print progress
            
            # Get a new link using the search function
            new_link = get_first_search_result(query)
            df.at[index, 'link'] = new_link
            
            # Print the result
            print(f"Updated link for {name}: {new_link}")
            
            # Add a delay to avoid being rate-limited
            time.sleep(random.uniform(5, 10))
    
    # Save the updated DataFrame back to the same CSV file
    df.to_csv(input_file, index=False)
    print(f"Updated file saved to {input_file}")

from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Lock for thread-safe access to shared resources
csv_lock = Lock()
issues_lock = Lock()
unique_issues = set()  # To store all unique issues encountered across threads

def scrape_candidate_issues(link):
    """
    Fetches the issues and responses from a candidate's page.
    
    Parameters:
    link (str): URL to the candidate's political courage test page.
    
    Returns:
    dict: A dictionary with issue titles as keys and responses as values.
    """
    try:
        page = requests.get(link)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")

        # Extract issues and responses
        issues = soup.findAll("div", attrs={"class": "col-lg-8 col-md-6 col-sm col-10 text-left candidate-text"})
        responses = soup.findAll("div", attrs={"class": "col-lg-2 col-md-3 col-sm-3 col-10 text-left candidate-text pct-accordion-assigned-item-pre-break"})

        # Pair issues and responses
        issue_response_pairs = {}
        for issue, response in zip(issues, responses):
            issue_text = issue.text.strip()
            response_text = response.text.strip() if response else "Couldn't fetch response"
            issue_response_pairs[issue_text] = response_text

        # Update global unique issues
        with issues_lock:
            unique_issues.update(issue_response_pairs.keys())

        return issue_response_pairs
    except requests.RequestException as e:
        print(f"An error occurred while fetching {link}: {e}")
        return None

def process_candidate(name, link):
    """
    Processes a single candidate, scraping issues and responses.
    
    Parameters:
    name (str): Candidate's name.
    link (str): URL to the candidate's political courage test page.
    
    Returns:
    dict: A dictionary representing the row to be written to the CSV.
    """
    row = {'name': name}
    
    if link and link != "None":
        # Scrape candidate issues and responses
        issues_responses = scrape_candidate_issues(link)
        if issues_responses:
            row.update(issues_responses)
        else:
            row.update({issue: "Couldn't fetch response" for issue in unique_issues})
    else:
        row.update({issue: "Couldn't fetch response" for issue in unique_issues})
        print(f"Error fetching {name}: Link missing or invalid")
    
    # Random delay to prevent getting blocked
    time.sleep(random.uniform(1, 2))
    return row

def create_political_stance_csv(legislators_file, output_file):
    """
    Reads candidates' links from a CSV file, scrapes their issues and responses in parallel, 
    and saves the results in a new CSV file with dynamically added issue columns.

    Parameters:
    legislators_file (str): Path to the CSV file containing candidate names and links.
    output_file (str): Path to the output CSV file to save candidate issues and responses.

    Returns:
    None
    """
    # Read links from legislators file
    with open(legislators_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        candidates = {row[0]: row[1] for row in reader}

    total_candidates = len(candidates)  # Total number of candidates
    rows = []

    # Process candidates in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_candidate = {executor.submit(process_candidate, name, link): name for name, link in candidates.items()}
        for i, future in enumerate(as_completed(future_to_candidate), start=1):
            candidate_name = future_to_candidate[future]
            try:
                row = future.result()
                rows.append(row)
                print(f"Processed {i}/{total_candidates}: {candidate_name} -> {row.get('name', 'No Link')}")
            except Exception as e:
                print(f"Error processing {candidate_name}: {e}")

    # Write rows to CSV
    with csv_lock:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name'] + sorted(unique_issues)  # Updated header with all issues
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                # Fill missing issues with placeholders
                for issue in fieldnames:
                    row.setdefault(issue, "Couldn't fetch response")
                writer.writerow(row)

# Usage
create_political_stance_csv('legislators_links.csv', 'political_stance.csv')

#uncomment from here 

# def scrape_candidate_issues(link):
#     """
#     Fetches the issues and responses from a candidate's page.
    
#     Parameters:
#     link (str): URL to the candidate's political courage test page.
    
#     Returns:
#     dict: A dictionary with issue titles as keys and responses as values.
#     """
#     try:
#         page = requests.get(link)
#         page.raise_for_status()
#         soup = BeautifulSoup(page.content, "html.parser")

#         # Extract issues and responses
#         issues = soup.findAll("div", attrs={"class": "col-lg-8 col-md-6 col-sm col-10 text-left candidate-text"})
#         responses = soup.findAll("div", attrs={"class": "col-lg-2 col-md-3 col-sm-3 col-10 text-left candidate-text pct-accordion-assigned-item-pre-break"})

#         # Pair issues and responses
#         issue_response_pairs = {}
#         for issue, response in zip(issues, responses):
#             issue_text = issue.text.strip()
#             response_text = response.text.strip() if response else "Couldn't fetch response"
#             issue_response_pairs[issue_text] = response_text

#         return issue_response_pairs
#     except requests.RequestException as e:
#         print(f"An error occurred while fetching {link}: {e}")
#         return None

# def create_political_stance_csv(legislators_file, output_file):
#     """
#     Reads candidates' links from a CSV file, scrapes their issues and responses, 
#     and saves the results in a new CSV file with dynamically added issue columns.

#     Parameters:
#     legislators_file (str): Path to the CSV file containing candidate names and links.
#     output_file (str): Path to the output CSV file to save candidate issues and responses.

#     Returns:
#     None
#     """
#     # Read links from legislators file
#     with open(legislators_file, 'r', newline='', encoding='utf-8') as infile:
#         reader = csv.reader(infile)
#         headers = next(reader)
#         candidates = {row[0]: row[1] for row in reader}

#     # Initial fieldnames with just the 'name' column
#     fieldnames = ['name']
#     rows = []

#     # Process each candidate
#     for i, (name, link) in enumerate(candidates.items(), start=1):
#         print(f"Processing {i}/{len(candidates)}: {name}")

#         row = {'name': name}
        
#         if link and link != "None":
#             # Scrape candidate issues and responses
#             issues_responses = scrape_candidate_issues(link)

#             if issues_responses:
#                 # Add any new issues as columns if not already in fieldnames
#                 for issue in issues_responses:
#                     if issue not in fieldnames:
#                         fieldnames.append(issue)
#                         # Rewrite CSV file with updated headers
#                         with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
#                             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                             writer.writeheader()
#                             writer.writerows(rows)  # Re-write all previous rows with new header

#                 # Populate row data with issues and responses
#                 for issue in fieldnames[1:]:  # Skip 'name' column
#                     row[issue] = issues_responses.get(issue, "Couldn't fetch response")
#             else:
#                 # If issues_responses is None, log an error
#                 for issue in fieldnames[1:]:
#                     row[issue] = "Couldn't fetch response"
#         else:
#             # Log an error if the link is missing or invalid
#             for issue in fieldnames[1:]:
#                 row[issue] = "Couldn't fetch response"
#             print(f"Error fetching {name}: Link missing or invalid")

#         # Add row to the list of rows and write to CSV
#         rows.append(row)
#         with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             writer.writerow(row)

#         # Random delay to prevent getting blocked
#         time.sleep(random.uniform(2, 4))

# # Usage
# create_political_stance_csv('legislators_links.csv', 'political_stance.csv')
#create_political_stance_csv('test.csv', 'test_out.csv')

#Example usage
# input_file = 'legislators_links.csv'
# update_missing_links(input_file)

#Example usage
# input_file = 'legislators-current.xlsx'
# output_file = 'legislators_links.csv'
# process_legislators(input_file, output_file)
# print(f"Results saved to {output_file}")

# Example usage
# query = "just facts vote smart candidate political courage test Sanders Bernard"
# first_link = get_first_search_result(query)
# print(first_link)
