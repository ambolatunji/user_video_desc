import re
import pandas as pd

# Sample Excel data for column A
data = xl("B:B")

# Convert to DataFrame (if not already)
df = pd.DataFrame(data)

# Define a function to extract matching patterns
def extract_patterns(text):
    # Define the patterns you're searching for
    pattern = r"(PL\d+|PLT\d+|BL\d+|BLK\d+|SHOP\d+|Phase)"
    match = re.search(pattern, text)
    
    # Return the match if found, else return empty string
    return match.group(0) if match else ''

# Apply the function to Column A and create a new Column B
dfX1['K:K']'] = dfX1'b:b'].apply(extract_patterns)

# Show the result
print(df)