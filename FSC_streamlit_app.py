import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from io import BytesIO

# Streamlit App
def main():
    st.title("XML Data Plotter")

    st.write("""
    Upload XML files and specify a name for each file to visualize the Fourier Shell Correlation (FSC) curves.
    """)

    # File upload section
    uploaded_files = st.file_uploader("Choose XML files", accept_multiple_files=True, type="xml")

    if uploaded_files:
        # Specify filenames
        st.write("### Specify Filenames for Each Uploaded File:")
        filenames = []
        for i, file in enumerate(uploaded_files):
            filename = st.text_input(f"Filename for file {i+1}", "")
            filenames.append(filename)

        # Check if all filenames are provided
        if any(filename.strip() == "" for filename in filenames):
            st.warning("Please provide filenames for all uploaded files.")
            return

        # Create filename mapw
        filename_map = {i: filenames[i] for i in range(len(uploaded_files))}

        # Load and parse the XML files
        df = load_post(uploaded_files, filename_map)

        # Display the dataframe
        st.write("### Parsed Data:")
        st.dataframe(df)

        # Plotting
        st.write("### Fourier Shell Correlation Plot:")
        fig = plot_fsc(df)
        st.pyplot(fig)

        # Option to download the plot
        st.write("### Download Plot:")
        st.download_button(
            label="Download plot as JPEG",
            data=save_plot_to_bytes(fig, format='jpeg'),
            file_name="plot.jpg",
            mime="image/jpeg"
        )

# Function to load and parse XML files
def load_post(files, filename_map):
    # Create an empty list to store data
    data = []

    # Iterate through the uploaded files
    for idx, file in enumerate(files):
        content = file.read()
        tree = ET.ElementTree(ET.fromstring(content))
        root = tree.getroot()

        # Extract data from XML and append to the list
        for child in root:
            row = {}
            for subchild in child:
                row[subchild.tag] = subchild.text
            # Set filename based on the mapping
            row['filename'] = filename_map.get(idx, 'Unknown File')
            data.append(row)

    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(data)
    return df

# Function to plot FSC curves
def plot_fsc(df):
    # Plotting two curves with specified colors
    fig, ax = plt.subplots()

    for filename, group_df in df.groupby('filename'):
        ax.plot(group_df['x'].astype(float), group_df['y'].astype(float), label=filename)

    # Add FSC line at 0.143
    ax.axhline(0.143, color="black", linestyle=":", label='FSC of 0.143')

    # Annotation for the FSC line
    ax.text(1.02, 0.143, '0.143', va='center', ha='left', color='black', transform=ax.get_yaxis_transform())

    # Axis labels
    ax.set_xlabel('Resolution [1/Å]')
    ax.set_ylabel('Fourier Shell Correlation')

    # Hide right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Legend placement
    ax.legend(loc='center left', bbox_to_anchor=(0.7, 0.8))

    return fig

# Function to save the plot to bytes for download
def save_plot_to_bytes(fig, format='png'):
    buf = BytesIO()
    fig.savefig(buf, format=format, dpi=300)
    buf.seek(0)
    return buf.getvalue()

if __name__ == '__main__':
    main()
