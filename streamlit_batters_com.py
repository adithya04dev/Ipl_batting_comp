

from batsman import Batsman
from batters1_comp import Batter_comp
import streamlit as st
import datetime
import pickle

import seaborn as sns
import matplotlib.pyplot as plt




with open('batting_comp.pkl', 'rb') as f:
    batcomp = pickle.load(f)
    #result1=bat.calculate("RA Tripathi",[1,2,3],["Pace"],[2022])
    #print(result1['strike_rate'])

def main():
    # Title of the app
    st.title("IPL: Batters Comparision ")
    # Input for PlayerName
    
    phases = st.multiselect("Select Phases ", ["Powerplay", "Middle1","Middle2","Slog"])
    # Input for Bowling type (dropdown)
    b_types=['LAP','RAP','OB','LB','SLA','LWS']
    bowling_type = st.multiselect("Select Bowling Type(s)", b_types)
    # Input for Season (slider)
    start_year = 2016
    end_year = 2023
    selected_years = st.slider("Select Seasons", start_year, end_year, (start_year, end_year))
    min_balls = st.number_input("Minimum Balls", min_value=20, step=10, value=20)
    min_avg = st.slider("Minimum Average", min_value=0, max_value=50, value=20)
    min_str = st.slider("Minimum Strikerate Y", min_value=100, max_value=200, value=130)

    
    
    ph1={'Powerplay':1,'Middle1':2,'Middle2':3,'Slog':4}
    
    overs=[ph1[phases[i]] for i in range(len(phases))]
    bowling_type=[bowling_type[i] for i in range(len(bowling_type))]
    Season=[i for i in range(selected_years[0],selected_years[1]+1)]
    
    
    # Display the selected inputs
    
    if st.button('Submit'):
        
        
        #st.write("Selected Player Name:", player_name)
        #st.write("Selected Bowling Type:", type(bowling_type[0]))  # Corrected indentation
        #st.write("Selected Phases:", len(phases))          
        #st.write("Selected Seasons:", selected_years[0], "to", selected_years[1])
        result=batcomp.calculate(overs,bowling_type,Season,min_balls)
        result1=result[result['average_runs']>min_avg]
        result1=result[result['strike_rate']>min_str].sort_values(by='strike_rate')
        # Assuming df is your DataFrame containing the required columns
        sns.set(style="white")
        
        # Create the scatter plot
        plt.figure(figsize=(10, 6))
        scatter_plot = sns.scatterplot(x='average_runs', y='strike_rate', data=result1)
        
        # Annotate the points with player names
        for i, row in result1.iterrows():
            scatter_plot.text(row['average_runs'], row['strike_rate'], row['player_name'], fontsize=8, alpha=0.7)
        
        plt.title('Scatter Plot of Average Runs vs Strike Rate')
        plt.xlabel('Average Runs')
        plt.ylabel('Strike Rate')
       
        
        st.pyplot(plt)
        
        
        
        
        st.write("All batters stats")
        st.dataframe(result1)
        
        
    
    
if __name__=='__main__':
    main()
