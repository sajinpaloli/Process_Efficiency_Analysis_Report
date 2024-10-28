import streamlit as st
st.set_page_config(page_title="Process Efficiency Analysis", layout="wide")

import pandas as pd
import numpy as np
import plotly.express as px

# Load and clean data


data = pd.read_excel("processed_metrics.xlsx")

print(data.head())
print(data.value_counts())
print(data.isnull().sum())

# Data Cleaning
data = data.dropna(subset=['Process_ID', 'Task_ID', 'Start_Time', 'End_Time'])  # Drop rows with crucial missing values
data['Cost (USD)'] = data['Cost (USD)'].fillna(data['Cost (USD)'].median())      # Fill missing cost with median
data['Resource'] = data['Resource'].fillna("Unknown")                           # Fill missing resource names with "Unknown"

# Preprocessing
data['Start_Time'] = pd.to_datetime(data['Start_Time'], errors='coerce')
data['End_Time'] = pd.to_datetime(data['End_Time'], errors='coerce')
data['Duration (minutes)'] = (data['End_Time'] - data['Start_Time']).dt.total_seconds() / 60

# Feature Engineering
data['Delay_Flag'] = data['Delay (minutes)'] > 0  # Create flag for delays
data['Is_Rework'] = data['Rework_Flag'] == "Yes"  # Create binary feature for rework

# Streamlit App Configuration
st.title("Process Efficiency Analysis for Manufacturing Optimization")

# Exploratory Data Analysis
st.subheader("Exploratory Data Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Processing Times Distribution")
    fig1 = px.histogram(data, x="Duration (minutes)", nbins=50, title="Processing Time Distribution")
    st.plotly_chart(fig1)
    st.write("""
    **Findings**: This histogram shows the distribution of processing times. High variability here can indicate inefficiencies.
    
    **Recommendations**:
    - Standardize processes to reduce variation.
    - Investigate and minimize tasks with processing times far from the median to improve **process** efficiency.
    """)

    st.markdown("### Delay Times Distribution")
    fig2 = px.histogram(data, x="Delay (minutes)", nbins=50, title="Delay Time Distribution")
    st.plotly_chart(fig2)
    st.write("""
    **Findings**: Delay times indicate potential bottlenecks or resource constraints.
    
    **Recommendations**:
    - Analyze high delay tasks to identify common causes.
    - Improve **resource planning** to reduce delays and optimize **system** availability.
    """)

with col2:
    st.markdown("### Resource Usage by Role")
    fig3 = px.box(data, x="Role", y="Duration (minutes)", color="Status", title="Duration by Role and Status")
    st.plotly_chart(fig3)
    st.write("""
    **Findings**: Roles with wide variations in duration can indicate training or workload balancing issues.
    
    **Recommendations**:
    - Standardize procedures and provide role-specific training to improve efficiency among **people**.
    - Redistribute tasks to ensure balance and minimize high durations for certain roles.
    """)

    st.markdown("### Cost Distribution Across Services")
    fig4 = px.box(data, x="Service_Type", y="Cost (USD)", color="Customer_Type", title="Cost by Service Type and Customer Type")
    st.plotly_chart(fig4)
    st.write("""
    **Findings**: This plot shows cost variations across service types and customer segments, highlighting cost inefficiencies.
    
    **Recommendations**:
    - Optimize service processes for high-cost areas to improve **service** efficiency.
    - Align cost structures with **customer** expectations for increased satisfaction and profitability.
    """)

# Inefficiency and Bottleneck Detection
st.subheader("Inefficiencies and Bottleneck Analysis")

# Highlight potential inefficiencies based on high delay times, rework flags, etc.
high_delay = data[data["Delay (minutes)"] > data["Delay (minutes)"].quantile(0.75)]
rework_tasks = data[data["Is_Rework"] == True]

col3, col4 = st.columns(2)

with col3:
    st.markdown("### High Delay Tasks")
    st.dataframe(high_delay[["Process_ID", "Task_Name", "Duration (minutes)", "Delay (minutes)", "Resource", "Role", "System_Used"]])
    st.write("""
    **Findings**: Tasks with high delay times can signal critical bottlenecks.
    
    **Recommendations**:
    - Conduct root cause analysis for high-delay tasks to address resource or **system** issues.
    - Implement a monitoring system to track and mitigate delays proactively.
    """)

    st.markdown("### Rework Analysis")
    rework_count = rework_tasks.groupby("Role").size().reset_index(name="Rework Count")
    fig5 = px.bar(rework_count, x="Role", y="Rework Count", title="Rework Count by Role")
    st.plotly_chart(fig5)
    st.write("""
    **Findings**: High rework counts suggest quality or training issues for certain roles.
    
    **Recommendations**:
    - Provide targeted training and quality checks for roles with high rework rates to improve **people** efficiency.
    - Investigate **product** quality standards and make necessary adjustments.
    """)

with col4:
    st.markdown("### Issue Flag Analysis")
    issue_flagged = data[data["Issue_Flag"] == "Yes"]
    issue_count = issue_flagged.groupby("Product_Category").size().reset_index(name="Issue Count")
    fig6 = px.bar(issue_count, x="Product_Category", y="Issue Count", title="Issues by Product Category")
    st.plotly_chart(fig6)
    st.write("""
    **Findings**: Products with high issue counts may indicate quality control gaps.
    
    **Recommendations**:
    - Strengthen quality control measures and adjust **product** specifications to reduce issues.
    - Regularly review and address customer feedback for products with recurring issues to enhance **customer** satisfaction.
    """)

    st.markdown("### Resource vs. Delay")
    fig7 = px.scatter(data, x="Duration (minutes)", y="Delay (minutes)", color="System_Used", size="Cost (USD)", hover_name="Task_Name", title="Duration vs Delay with Resource Usage")
    st.plotly_chart(fig7)
    st.write("""
    **Findings**: A positive correlation between duration and delay may point to resource limitations.
    
    **Recommendations**:
    - Optimize **resource** allocation to reduce delays for time-intensive tasks.
    - Regularly maintain and update **system** resources to ensure availability and efficiency.
    """)

# Industry Standard Comparison Section
st.subheader("Benchmarking Against Industry Standards")

# Sample standards (you may replace these with actual benchmarks)
industry_avg_processing_time = 150  # minutes
industry_avg_delay = 20  # minutes

st.write(f"**Industry Average Processing Time:** {industry_avg_processing_time} minutes")
st.write(f"**Industry Average Delay Time:** {industry_avg_delay} minutes")

current_avg_processing_time = data["Duration (minutes)"].mean()
current_avg_delay = data["Delay (minutes)"].mean()

st.metric(label="Current Average Processing Time", value=f"{current_avg_processing_time:.2f} minutes", delta=f"{current_avg_processing_time - industry_avg_processing_time:.2f}")
st.metric(label="Current Average Delay Time", value=f"{current_avg_delay:.2f} minutes", delta=f"{current_avg_delay - industry_avg_delay:.2f}")

st.write("""
**Recommendations Based on Benchmarking**:
- Identify and address discrepancies in processing time compared to industry averages to align with **process** standards.
- Implement time-tracking and analysis tools to continuously measure and meet industry benchmarks.
""")

# Concluding Insights
st.subheader("Summary Insights and Recommendations")
st.write("""
Based on the analysis, we recommend the following steps to enhance efficiency across various areas:
1. **People**: Standardize training and role assignments to minimize rework and reduce processing time variability.
2. **Process**: Investigate and streamline processes with the highest delays to remove bottlenecks.
3. **Data**: Leverage predictive analytics to identify and address inefficiencies in real time.
4. **System**: Ensure that systems are maintained regularly to avoid unnecessary downtime.
5. **Customer**: Tailor services and costs to meet customer expectations for improved satisfaction.
6. **Product**: Adjust quality standards and conduct regular reviews to minimize defect rates.
7. **Services**: Reduce cost variations across service types by aligning processes and optimizing resource allocation.
""")
