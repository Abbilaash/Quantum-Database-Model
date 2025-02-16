import time
import pandas as pd

# Function to perform linear search on the database based on ID
def linear_search():
    start_time = time.time()

    df = pd.read_csv("C:/Users/abbil/Downloads/Crime_Data_from_2020_to_Present.csv",delimiter=',')
    count = 0
    for record in df.iterrows():
        if record[1]['DR_NO'] == 250504051:  # last record in the dataset
            print(record)
            break
        count+=1
    end_time = time.time()

    end_time = time.time()
    print(f"Number of records: {count}")
    print(f"Time taken for linear traversal: {end_time - start_time:.5f} seconds")


# Example usage
if __name__ == "__main__":
    linear_search()