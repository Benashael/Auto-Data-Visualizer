import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set Streamlit page title and icon
st.set_page_config(page_title="Data Viz App", page_icon=":bar_chart:")

# Title
st.title("Data Visualization Streamlit Web App")

# Create data and tutorial pages
page = st.sidebar.selectbox("Select a Page", ["Data Visualizer", "Tutorial"])

if page == "Data Visualizer":
    # Option to upload a CSV file or use an example dataset
    st.sidebar.title("Choose Data Source")
    data_source = st.sidebar.radio("Select Data Source", ["Upload CSV", "Use Example Dataset"])

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
        }
        selected_example = st.sidebar.selectbox("Select an example dataset", list(example_datasets.keys()))

        if selected_example:
            try:
                data = pd.read_csv(example_datasets.get(selected_example, ""))
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.stop()  # Stop execution if there's an error

    if data is not None and not data.empty:
        # Automatically select visualization options
        st.sidebar.subheader("Visualization Settings")
        selected_columns = data.columns

        # Color customization
        color = st.sidebar.color_picker("Select a color", "#ff5733")

        # Create a dictionary to store generated plots
        generated_plots = {}

        # Matplotlib Line Plot (Automated)
        if len(selected_columns) > 1:
            x_column = selected_columns[0]  # Automatically select the first column
            y_column = selected_columns[1]  # Automatically select the second column
            line_label = "Line"  # Use a default line label
            line_style = "-"  # Use a default line style
            fig, ax = plt.subplots()
            ax.plot(data[x_column], data[y_column], label=line_label, color=color, linestyle=line_style)
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            ax.legend()
            generated_plots["Matplotlib Line Plot"] = fig

        # Seaborn Pairplot (Automated)
        if len(selected_columns) > 1:
            pairplot = sns.pairplot(data[selected_columns], palette=color)
            generated_plots["Seaborn Pairplot"] = pairplot

        # Plotly Scatter Plot (Automated)
        if len(selected_columns) > 2:
            x_column = selected_columns[0]  # Automatically select the first column
            y_column = selected_columns[1]  # Automatically select the second column
            color_column = selected_columns[2]  # Automatically select the third column
            scatter_fig = px.scatter(data, x=data[x_column], y=data[y_column], color=data[color_column])
            generated_plots["Plotly Scatter Plot"] = scatter_fig

        # Seaborn Violin Plot (Automated)
        if len(selected_columns) > 1:
            violin_plot = sns.violinplot(data=data[selected_columns], inner="quart", palette=color)
            generated_plots["Seaborn Violin Plot"] = violin_plot

        # Seaborn Heatmap (Automated)
        if len(selected_columns) > 1:
            heatmap = sns.heatmap(data[selected_columns].corr(), annot=True, cmap="coolwarm")
            generated_plots["Seaborn Heatmap"] = heatmap

        # Matplotlib Pie Chart (Automated)
        if len(selected_columns) > 1:
            fig, ax = plt.subplots()
            pie_chart = ax.pie(data[selected_columns].sum(), labels=selected_columns, autopct='%1.1f%%', startangle=140)
            generated_plots["Matplotlib Pie Chart"] = fig

        # Display the generated plots
        st.subheader("Generated Plots")
        for plot_name, plot in generated_plots.items():
            st.write(f"**{plot_name}**")

            if isinstance(plot, plt.Figure):
                st.pyplot(plot)
            else:
                st.plotly_chart(plot)

        st.warning("Please note that the data used for these visualizations is not displayed or stored.")
    else:
        st.warning("Please provide a valid CSV file or select a different dataset.")

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

   
   

