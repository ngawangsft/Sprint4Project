# Sprint4Project
Used Car Market Anylysis

Project Description:
This project emphasizes the practice of building and deploying a web application that visualizes insights from a dataset of U.S. used car listings. You can find interactive visualizations that explore:

1) How used car prices are distributed
2) The effect of mileage on price across different fuel types
3) Which vehicle types retain value better over time
4) R² values by vehicle type to measure model performance
4) The dominance of various vehicle types in listings

Methods and Libraries Used:
This project makes use of the following tools and libraries:

1) pandas – For data manipulation, filtering, and analysis
2) plotly.express – To create plots like histograms, scatterplots, and bar charts
3) streamlit – To build an interactive web dashboard with checkboxes, headers, and embedded visualizations
4) plotly.graph_objects – For customizing the bar chart of R² values by vehicle type
5) %matplotlib inline – Only used in the notebook, to display matplotlib plots inline
6) matplotlib.pyplot – Only used in the notebook, for a static bar chart of R² values (not used in the Streamlit version)
7) seaborn – For creating visually appealing statistical plots such as scatterplots and bar charts

Instructions to Run Project Locally:
1) Clone the repository or download project files
2) Must have Python installed
3) Use a virtual environment:
    python -m venv venv
    source venv/bin/activate   #On Windows use: venv\Scripts\activate
4) Install the required libraries:
    pip install -r requirements.txt
5) Launch the Streamlit app:
    streamlit run app.py
6) Browser will open automatically, if not, the URL is shown in terminal

