import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import zipfile
import io
import pdfcrowd

# Set Streamlit page title and icon
st.set_page_config(page_title="Data Viz App", page_icon=":bar_chart:")

# Title
st.title("Data Visualization Streamlit Web App")

# Create data and tutorial pages
page = st.sidebar.selectbox("Select a Page", ["Data Visualizer", "Tutorial"])

if page == "Data Visualizer":
    # Option to upload a CSV file or use an example dataset
    st.sidebar.title("Choose Data Source")
    data_source = st.sidebar.radio("Select Data Source", ("Upload CSV", "Use Example Dataset"))

    data = None  # Initialize data as None

    if data_source == "Upload CSV":
        uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

        if uploaded_file is not None:
            try:
                data = pd.read_csv(uploaded_file)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.stop()  # Stop execution if there's an error

    else:
        st.sidebar.subheader("Example Datasets")
        example_datasets = {
            "Iris Dataset": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv",
            "Titanic Dataset": "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
        }
        selected_example = st.sidebar.selectbox("Select an example dataset", list(example_datasets.keys()))

        try:
            data = pd.read_csv(example_datasets[selected_example])
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.stop()  # Stop execution if there's an error

    if data is not None:  # Check if data is loaded successfully
        # Sidebar - Variable selection and interaction
        st.sidebar.subheader("Visualization Settings")
        selected_columns = st.sidebar.multiselect("Select columns for visualization", data.columns)

        # Color customization
        color = st.sidebar.color_picker("Select a color", "#ff5733")

        # Create a dictionary to store generated plots
        generated_plots = {}

        # Add interaction for Matplotlib Line Plot
        matplotlib_line_plot = st.sidebar.checkbox("Line Plot (Matplotlib)")
        if matplotlib_line_plot:
            st.sidebar.write("### Matplotlib Line Plot Options")
            x_column = st.sidebar.selectbox("X-axis", selected_columns)
            y_column = st.sidebar.selectbox("Y-axis", selected_columns)
            line_label = st.sidebar.text_input("Line Label", "Line")
            line_style = st.sidebar.selectbox("Line Style", ["-", "--", "-.", ":", "None"])
            
            if st.button("Plot Matplotlib Line Plot"):
                st.write("### Matplotlib Line Plot")
                fig, ax = plt.subplots()
                ax.plot(data[x_column], data[y_column], label=line_label, color=color, linestyle=line_style)
                ax.set_xlabel(x_column)
                ax.set_ylabel(y_column)
                ax.legend()
                generated_plots["Matplotlib Line Plot"] = fig

        # Add interaction for Seaborn Pairplot
        seaborn_pairplot = st.sidebar.checkbox("Pairplot (Seaborn)")
        if seaborn_pairplot:
            if st.button("Plot Seaborn Pairplot"):
                st.write("### Seaborn Pairplot")
                pairplot = sns.pairplot(data[selected_columns], palette=color)
                generated_plots["Seaborn Pairplot"] = pairplot

        # Add interaction for Plotly Scatter Plot
        plotly_scatter_plot = st.sidebar.checkbox("Scatter Plot (Plotly)")
        if plotly_scatter_plot:
            st.sidebar.write("### Plotly Scatter Plot Options")
            x_column = st.sidebar.selectbox("X-axis", selected_columns)
            y_column = st.sidebar.selectbox("Y-axis", selected_columns)
            color_column = st.sidebar.selectbox("Color by", selected_columns)
            
            if st.button("Plot Plotly Scatter Plot"):
                st.write("### Plotly Scatter Plot")
                scatter_fig = px.scatter(data, x=data[x_column], y=data[y_column], color=data[color_column])
                generated_plots["Plotly Scatter Plot"] = scatter_fig

        # Add interaction for Seaborn Violin Plot
        seaborn_violin_plot = st.sidebar.checkbox("Violin Plot (Seaborn)")
        if seaborn_violin_plot:
            if st.button("Plot Seaborn Violin Plot"):
                st.write("### Seaborn Violin Plot")
                violin_plot = sns.violinplot(data=data[selected_columns], inner="quart", palette=color)
                generated_plots["Seaborn Violin Plot"] = violin_plot

        # Add interaction for Matplotlib Area Plot
        matplotlib_area_plot = st.sidebar.checkbox("Area Plot (Matplotlib)")
        if matplotlib_area_plot:
            st.sidebar.write("### Matplotlib Area Plot Options")
            area_column = st.sidebar.selectbox("Select column for the Area Plot", selected_columns)
            if st.button("Plot Matplotlib Area Plot"):
                st.write("### Matplotlib Area Plot")
                fig, ax = plt.subplots()
                area_plot = data[selected_columns].plot(kind="area", ax=ax, color=color)
                ax.set_xlabel("X-axis")
                ax.set_ylabel("Y-axis")
                ax.legend()
                generated_plots["Matplotlib Area Plot"] = fig

        # Add interaction for Seaborn Heatmap
        seaborn_heatmap = st.sidebar.checkbox("Heatmap (Seaborn)")
        if seaborn_heatmap:
            if st.button("Plot Seaborn Heatmap"):
                st.write("### Seaborn Heatmap")
                heatmap = sns.heatmap(data[selected_columns].corr(), annot=True, cmap="coolwarm")
                generated_plots["Seaborn Heatmap"] = heatmap

        # Add interaction for Matplotlib Pie Chart
        matplotlib_pie_chart = st.sidebar.checkbox("Pie Chart (Matplotlib)")
        if matplotlib_pie_chart:
            if st.button("Plot Matplotlib Pie Chart"):
                st.write("### Matplotlib Pie Chart")
                fig, ax = plt.subplots()
                pie_chart = ax.pie(data[selected_columns].sum(), labels=selected_columns, autopct='%1.1f%%', startangle=140)
                generated_plots["Matplotlib Pie Chart"] = fig

        # Display the generated plots
        if generated_plots:
            st.subheader("Generated Plots")
            for plot_name, plot in generated_plots.items():
                if isinstance(plot, plt.Figure):
                    st.write(f"**{plot_name}**")
                    st.pyplot(plot)
                else:
                    st.write(f"**{plot_name}**")
                    st.pyplot(plot)

        # Option to save generated plots
        if st.button("Save Generated Plots"):
            zip_buffer = io.BytesIO()
            with st.spinner("Saving..."):
                with zipfile.ZipFile(zip_buffer, 'w') as zipf:
                    for plot_name, plot in generated_plots.items():
                        if isinstance(plot, plt.Figure):
                            plotfile = io.BytesIO()
                            plot.savefig(plotfile, format="png")
                            plotfile.seek(0)
                            zipf.writestr(f"{plot_name}.png", plotfile.read())
                        else:
                            plot_bytes = plot.to_image(format="png")
                            zipf.writestr(f"{plot_name}.png", plot_bytes)

            zip_buffer.seek(0)
            st.write("Download Zip File")

    # Add error handling if data is not loaded
    else:
        st.warning("Please provide a valid CSV file or select a different dataset.")

# Tutorial page
if page == "Tutorial":
    st.title("Tutorial - Data Visualization Metrics")

    st.write("Welcome to the tutorial page where you can learn about different data visualization metrics.")
    st.write("We'll briefly explain each visualization metric.")

    # Explanation for Matplotlib Line Plot
    st.subheader("Matplotlib Line Plot")
    st.write("A line plot is a type of chart that displays data points on a line.")
    st.write("It is commonly used to visualize trends over time.")
    st.write("In our app, you can customize the X-axis, Y-axis, line label, and line style.")

    # Explanation for Seaborn Pairplot
    st.subheader("Seaborn Pairplot")
    st.write("A pairplot is a grid of plots that displays pairwise relationships between multiple variables.")
    st.write("It is useful for exploring correlations and distributions in your data.")

    # Explanation for Plotly Scatter Plot
    st.subheader("Plotly Scatter Plot")
    st.write("A scatter plot is used to visualize the relationship between two variables.")
    st.write("Plotly is a library that provides interactive plots with zoom and hover features.")

    # Explanation for Seaborn Violin Plot
    st.subheader("Seaborn Violin Plot")
    st.write("A violin plot is used to visualize the distribution of data across different categories.")
    st.write("It shows the probability density of the data at different values.")

    # Explanation for Matplotlib Area Plot
    st.subheader("Matplotlib Area Plot")
    st.write("An area plot is similar to a line plot but with the area below the line filled in with color.")
    st.write("It's used to represent accumulated totals over time.")

    # Explanation for Seaborn Heatmap
    st.subheader("Seaborn Heatmap")
    st.write("A heatmap is a graphical representation of data where individual values are represented as colors.")
    st.write("It's used to visualize relationships and correlations between data points.")

    # Explanation for Matplotlib Pie Chart
    st.subheader("Matplotlib Pie Chart")
    st.write("A pie chart is a circular chart that displays data as slices of a pie.")
    st.write("It's used to show the proportion of each category in a dataset.")

    # Add more explanations for other visualization metrics

    # Option to download the tutorial as a PDF
    st.subheader("Download Tutorial as PDF")
    tutorial_pdf = st.button("Download Tutorial PDF")

    if tutorial_pdf:
        # Create a PDFCrowd client using your API key
        pdf_client = pdfcrowd.Client("YOUR_PDFCROWD_API_KEY")

        # Generate the PDF
        st.write("Generating the PDF...")
        pdf_filename = "data_viz_tutorial.pdf"

        # HTML content for the tutorial page
        html_content = """
        <html>
        <head>
        <title>Data Visualization Tutorial</title>
        </head>
        <body>
        <h1>Data Visualization Tutorial</h1>
        <p>Welcome to the tutorial page where you can learn about different data visualization metrics.</p>
        <p>Here are some explanations for common data visualization metrics:</p>
        <ul>
            <li>Matplotlib Line Plot: A line plot displays data points on a line. It's used to visualize trends over time.</li>
            <li>Seaborn Pairplot: A pairplot is a grid of plots that displays pairwise relationships between variables.</li>
            <li>Plotly Scatter Plot: A scatter plot visualizes the relationship between two variables with interactivity.</li>
            <li>Seaborn Violin Plot: A violin plot shows the distribution of data across categories.</li>
            <li>Matplotlib Area Plot: An area plot is similar to a line plot but with the area filled in with color.</li>
            <li>Seaborn Heatmap: A heatmap represents data with colors to visualize relationships.</li>
            <li>Matplotlib Pie Chart: A pie chart displays data as slices of a pie to show proportions.</li>
        </ul>
        <p>Learn more about data visualization and create your own visualizations using the Data Visualizer page.</p>
        </body>
        </html>
        """

        try:
            with open(pdf_filename, 'wb') as pdf_file:
                pdf_client.convertString(html_content, pdf_file)
            st.write(f"PDF generated successfully. You can download it [here]({pdf_filename}).")
        except pdfcrowd.Error as why:
            st.error(f"PDF generation failed: {why}")


