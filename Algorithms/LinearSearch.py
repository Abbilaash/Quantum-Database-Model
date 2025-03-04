import time
import pandas as pd

# Function to perform linear search on the database based on ID
def linear_search():
    start_time = time.time()

    df = pd.read_csv("dataset.csv")
    count = 0
    for record in df.iterrows():
        count+=1
        if record[1]["Problem"] == 'Fever':
            print(record[1]['PatientID'],record[1]['Name'],record[1]['Problem'])
    end_time = time.time()

    print(f"Number of records: {count}")
    print(f"Time taken for linear traversal: {end_time - start_time:.5f} seconds")


# Example usage
if __name__ == "__main__":
    linear_search()