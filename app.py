import streamlit as st
import pandas as pd
import plotly.express as px
from data import get_rations_data

def main():
    st.set_page_config(layout="wide", page_icon="favicon.ico")
    
    # Header with logo and title using columns
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("logo.png", width=150)
    with col2:
        st.title("Rations Optimizer - First Strike Ration Menus 2012")
        st.subheader("Filter available MREs to Maximize Calories While Minimizing Weight for Optimal Field Energy")
    st.markdown("---")
    df = get_rations_data()
    
    st.sidebar.title("Filters")    

    # Calories Filter
    min_calories, max_calories = int(df["Calories"].min()), int(df["Calories"].max())
    selected_calories = st.sidebar.slider("Calories", min_calories, max_calories, (min_calories, max_calories))

    # Grams Filter
    min_grams, max_grams = int(df["Grams"].min()), int(df["Grams"].max())
    selected_grams = st.sidebar.slider("Grams", min_grams, max_grams, (min_grams, max_grams))
    # Type Filter
    types = sorted(df["Type"].unique())
    selected_types = st.sidebar.multiselect("Type of Item", types, default=types)

    # About section in sidebar (at bottom)
    with st.sidebar.expander("About App"):
        st.write("""
        **What This App Does:**
        
        This application helps you analyze and optimize military First Strike Ration (FSR) data from 2012 menus. It provides interactive filtering and visualization tools to compare the caloric density (calories per gram) of different food items.
        
        **Why It's Useful:**
        
        - **Weight Optimization**: Essential for military personnel, hikers, and outdoor enthusiasts who need to minimize pack weight while maximizing nutrition
        - **Caloric Efficiency**: Identify foods that provide the most energy per unit of weight
        - **Informed Decisions**: Make data-driven choices when selecting rations for missions, expeditions, or emergency preparedness
        - **Nutritional Planning**: Balance different food types while staying within weight constraints
        
        **Key Metrics:**
        - *Calories per Gram*: The primary optimization metric - higher values mean more energy per unit weight
        - *Total Calories*: Overall energy content of each item
        - *Weight in Grams*: Physical weight considerations for transport
        
        Use the filters to explore different scenarios and find the optimal combination of nutrition and portability for your specific needs.
        
        ---
        
        **Sponsored by Eric Boehlke, https://truevis.com**
        """)

    # Filtering dataframe
    df_filtered = df[
        df["Type"].isin(selected_types) &
        (df["Calories"] >= selected_calories[0]) &
        (df["Calories"] <= selected_calories[1]) &
        (df["Grams"] >= selected_grams[0]) &
        (df["Grams"] <= selected_grams[1])
    ]

    st.header("Weight in Grams vs. Calories")
    if not df_filtered.empty:
        fig = px.scatter(df_filtered, 
                        x="Grams", 
                        y="Calories", 
                        color="Type",
                        hover_data={"Item": True, "Menu": False, "Grams": True, "Calories": True, "Type": False},
                        hover_name="Item",
                        title="Weight in Grams vs. Calories")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.header("Item's Calories")
        if not df_filtered.empty:
            st.bar_chart(df_filtered.set_index("Item")["Calories"])

    with col2:
        st.header("Item's Weight in Grams")
        if not df_filtered.empty:
            st.bar_chart(df_filtered.set_index("Item")["Grams"])

    st.header("Calories per Gram")
    if not df_filtered.empty:
        st.bar_chart(df_filtered.set_index("Item")["Calories per Gram"])

    st.header("Filtered Data")
    st.dataframe(df_filtered)


if __name__ == "__main__":
    main()
