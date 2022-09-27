# !/usr/bin/env python
# Load necessary packages
import pandas as pd
import recordlinkage as rl
import json

def dublettenerkennung(df: pd.DataFrame):
    # From scratch
    indexer = rl.Index()
    # Set the mode to blocking with `nationalitaet_id`
    indexer.block('nationalitaet_id')

    # Set the mode to full
    # indexer.full()

    # Generate pairs
    pairs = indexer.index(df)
    print(len(pairs))

    # Create a comparing object
    compare = rl.Compare()

    # Query the exact matches of state
    # exact_columns = []
    # for col in exact_columns:
    #     compare.exact(col, col, label=col)
        
    # Query the fuzzy matches for strings
    string_columns = ['name',
                        'vorname',
                        'beruf',
                        'geburtsname',
                        'geburtsort',
                        'nationalitaet',
                        'taufort',
                        'spitzname',
                        'titel',
                        'strasse',
                        'plz',
                        'ort',
                        'land',
                        'telefonprivat',
                        'telefonhandy',
                        'fax',
                        'email']
    for col in string_columns:
        compare.string(col, col, threshold=0.85, 
                    method='levenshtein', label=col)

    # Query the fuzzy matches for dates
    date_columns = ['geburtsdatum','hochzeitsdatum','taufdatum']
    for col in date_columns:
        df[col]= pd.to_datetime(df[col])
        compare.date(col, col, label=col)

    # Compute the matches, this will take a while
    print('Computing algorithm to find duplicates...')
    matches = compare.compute(pairs, df, df)

    # print(matches)

    """ TESTS
    i = 1
    # Query matches with score over i
    while i < 20:
        full_matches = matches[matches.sum(axis='columns') >= i]
        # full_matches.sample(5) #test print
        print(f'For score over {i}: {full_matches.shape[0]} pairs') #test print
        i= i+1
        if full_matches.shape[0] == 0:
            break
    """

    full_matches = matches[matches.sum(axis='columns') >= 6]
    # print(full_matches)

    full_pairs = full_matches.index
    full_pairs = full_pairs.to_frame(index=False)

    # To return:
    result = full_pairs.to_json(orient="records")

    return result

def main():
    
    # Load json file to a dict
    with open("table.json", "r") as read_file:
        data_dict = json.load(read_file)
    # Load dict as a Dataframe
    df = pd.DataFrame.from_dict(data_dict)
    df = df.set_index('id')

    dubletten = dublettenerkennung(df)

    parsed = json.loads(dubletten)
    print(json.dumps(parsed, indent=4))


if __name__ == '__main__':
    main()