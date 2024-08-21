import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

def load_post(filenames):
    # Create an empty list to store data
    data = []

    # Define filename mapping
    filename_map = {
        filenames[0]: 'TC - Ap3G (2.51Å)',
        filenames[1]: 'TC - Ap4G (2.53Å)',
        filenames[2]: 'TC - Ap4A (2.52Å)',
        filenames[3]: 'TC - GTP (2.76Å)',
        filenames[4]: 'aTT - Ap4A (2.91Å)'
    }

    # Iterate through the XML files
    for filename in filenames:
        # Parse the XML file
        tree = ET.parse(filename)
        root = tree.getroot()

        # Extract data from XML and append to the list
        for child in root:
            row = {}
            for subchild in child:
                row[subchild.tag] = subchild.text

            # Set filename based on the mapping
            row['filename'] = filename_map.get(filename, 'Default Value')
            data.append(row)

    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(data)
    return df

# Example usage
filenames = [
'caps_411_postprocess_fsc.xml', 
'caps_211_postprocess_fsc.xml', 
'caps_301_postprocess_fsc.xml', 
'caps_129_postprocess_fsc.xml', 
'caps_229_postprocess_fsc.xml' ] # Replace with your XML file names

df = load_post(filenames)

# Plotting two curves with specified colors
fig, ax = plt.subplots()

for filename, group_df in df.groupby('filename'):
    ax.plot(group_df['x'].astype(float), group_df['y'].astype(float), label=filename)

fsc_line = ax.axhline(0.143, color="black", linestyle=":", label='FSC of 0.143')

# Annotation for the FSC line
ax.text(1.02, 0.143, '0.143', va='center', ha='left', color='black', transform=ax.get_yaxis_transform())

# Plot the Nyquist frequency
# Nyq_line = ax.axvline(0.5988, color="black", linestyle=":")

# Annotation for the Nyquist frequency line
# ax.text(0.5988, 1.1, 'Nyquist frequency\nof extracted particles\nat 1.67 Å', va='bottom', ha='center', color='black')

# Axis labels
ax.set_xlabel('Resolution [1/Å]')
ax.set_ylabel('Fourier Shell Correlation')

# Hide right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Legend placement
ax.legend(loc='center left', bbox_to_anchor=(0.7, 0.8))

# Save the figure as a high-quality JPEG image
plt.savefig("plot.jpg", format='jpg', dpi=300, quality=95)

plt.show()