# inputs: 
# 1= path to all the log files,
# 2= path to the analysis csv file

import os
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib
import csv

# PREPROCESS JPF LOGS, STEP 1
def preprocess_log(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def preprocess_logs(log_dir):
    logs = []
    for root, _, files in os.walk(log_dir):
        for log_file in files:
            if log_file.endswith(".txt"):
                log_path = os.path.join(root, log_file)
                parent_folder = os.path.basename(root)
                project = os.path.basename(os.path.dirname(root))
                tool = os.path.basename(os.path.dirname(os.path.dirname(root)))
                
                log_data = {
                    'content': preprocess_log(log_path),
                    'file_name': log_file,
                    'parent_folder': parent_folder,
                    'project': project,
                    'tool': tool
                }
                logs.append(log_data)
    return logs

log_directory = sys.argv[1]
logs_data = preprocess_logs(log_directory)

# TF-IDF Vectorization, Step 2
def vectorize_logs(logs_data):
    corpus = [log['content'] for log in logs_data]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    return tfidf_matrix

tfidf_matrix = vectorize_logs(logs_data)

# TF-IDF Similarity Comparison (compare vectors) and Identify Differences, Step 3
def compare_vectors(tfidf_matrix):
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix

similarity_matrix = compare_vectors(tfidf_matrix)

# Set a threshold to detect significant differences
threshold = 0.88

# Identify pairs of logs with significant differences
significant_differences = []
for i in range(len(similarity_matrix)):
    for j in range(i + 1, len(similarity_matrix)):
        if similarity_matrix[i, j] < threshold:
            significant_differences.append((i, j, similarity_matrix[i, j]))

# Prepare CSV output
csv_output = []
if significant_differences:
    for diff in significant_differences:
        log_pair = (diff[0], diff[1])
        similarity_score = diff[2]
        
        # Extract the content of the two logs
        log1_data = logs_data[log_pair[0]]
        log2_data = logs_data[log_pair[1]]
        
        log1_lines = log1_data['content'].splitlines()
        log2_lines = log2_data['content'].splitlines()
        
        # Use difflib to find differences
        differ = difflib.Differ()
        diff_lines = list(differ.compare(log1_lines, log2_lines))
        
        # Collect differences
        differences = ""
        for line in diff_lines:
            if line.startswith('- ') or line.startswith('+ '):
                # in line, replace ", with ; to avoid csv issues
                line = line.replace(",", ";")
                differences += line + '\\n'
        
        csv_output.append([
            log1_data['tool'], log1_data['project'],
            log1_data['parent_folder'], log1_data['file_name'],
            log2_data['parent_folder'], log2_data['file_name'],
            similarity_score, differences.strip()
        ])

# Write to CSV file
csv_file_path = sys.argv[2]
# if the file do not exist, create it and write the header
if not os.path.exists(csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile_header:
        csv_writer = csv.writer(csvfile_header, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Tool', 'Project', 'Parent Folder 1', 'File Name 1', 'Parent Folder 2', 'File Name 2', 'Similarity Score', 'Differences'])

with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # csv_writer.writerow(['Tool', 'Project', 'Parent Folder 1', 'File Name 1', 'Parent Folder 2', 'File Name 2', 'Similarity Score', 'Differences'])
    csv_writer.writerows(csv_output)

print(f"Results saved to {csv_file_path}")
