import pandas as pd
import csv
import sys


def preprocess_csv(input_csv_path, temp_csv_path):
    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as infile, \
            open(temp_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, quotechar='"', escapechar='\\')
        writer = csv.writer(outfile, quotechar='"', escapechar='\\')
        for row in reader:
            writer.writerow(row)


def transform_buttercup_to_protonpass(buttercup_csv_path, output_csv_path):
    temp_csv_path = 'temp_processed.csv'
    preprocess_csv(buttercup_csv_path, temp_csv_path)

    # Load the preprocessed CSV file
    buttercup_df = pd.read_csv(temp_csv_path)

    # Create a dictionary to map group_id to group_name
    group_dict = \
    buttercup_df[buttercup_df['!type'] == 'group'][['!group_id', '!group_name']].set_index('!group_id').to_dict()[
        '!group_name']

    # Filter entries and map their group_id to group_name
    entries_df = buttercup_df[buttercup_df['!type'] == 'entry'].copy()
    entries_df['vault'] = entries_df['!group_id'].map(group_dict)

    # Combine URL fields
    entries_df['url_combined'] = entries_df['URL'].combine_first(entries_df['url'])

    # Combine note fields with additional columns
    entries_df['note_combined'] = entries_df.apply(lambda row: '\n'.join(filter(None, [
        str(row['Notes']) if pd.notna(row['Notes']) else '',
        f"Pseudo: {row['Pseudo']}" if pd.notna(row['Pseudo']) else '',
        f"Email: {row['Email']}" if pd.notna(row['Email']) else '',
        f"pseudo: {row['pseudo']}" if pd.notna(row['pseudo']) else '',
        f"Code: {row['Code']}" if pd.notna(row['Code']) else '',
    ])), axis=1)

    # Perform the transformation
    transformed_df = pd.DataFrame({
        'name': entries_df['title'],
        'url': entries_df['url_combined'],
        'username': entries_df['username'],
        'password': entries_df['password'],
        'note': entries_df['note_combined'],
        'totp': None,  # Assuming there are no TOTP entries in Buttercup data
        'vault': entries_df['vault']  # Using the group name for the vault
    })

    # Remove rows where both 'name' and 'password' are NaN (not useful entries)
    transformed_df.dropna(subset=['name', 'password'], how='all', inplace=True)

    # Save the transformed data to a new CSV file
    transformed_df.to_csv(output_csv_path, index=False)
    print(f"Transformed data saved to {output_csv_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transform.py <input_buttercup_csv> <output_protonpass_csv>")
        sys.exit(1)

    buttercup_csv_path = sys.argv[1]
    output_csv_path = sys.argv[2]

    transform_buttercup_to_protonpass(buttercup_csv_path, output_csv_path)
