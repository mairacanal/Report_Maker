import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import folium as fl
from time import sleep
import selenium.webdriver
import os

# --------------------------------------------------------------------------------------------

# Uses the 1.5xIQR method to identify outliers and substitute them with a NaN

def outliers_clean (data, sorted_data):

    Q1 = np.percentile(sorted_data, 25)
    Q3 = np.percentile(sorted_data, 75)
    IQR = Q3 - Q1
    lower_range = Q1 - (1.5 * IQR)
    upper_range = Q3 + (1.5 * IQR)

    for c, sample in enumerate(data):
        if sample > upper_range or sample < lower_range:
            data[c] = np.NaN

    return (data)

# --------------------------------------------------------------------------------------------

# Generic function to generate line plot graphics of a dataType in function of the another dataType
# Examples: Temperature x Time; Pressure x Time

def generate_data_x_data (data, data2, dataType, dataType2, path):
    # print(dataType, len(data),dataType2, len(data2))
    if pd.Series(data).is_unique == True and False:
        pass
    #     return -1                            

    else:
        # Cleaning outliers
        # data  = outliers_clean (data , np.sort(data))
        # data2 = outliers_clean (data2, np.sort(data2))

        df = pd.DataFrame(list(zip(data, data2)), columns= [f'{dataType}', f'{dataType2}'])
        
        # Set a graph design
        plt.style.use(u'seaborn-pastel')

        # Create graph
        plt.plot(df[f'{dataType2}'], df[f'{dataType}'], marker='', color='blue', linewidth=1, alpha=0.7)

        # Add titles
        plt.title(f"{dataType} x {dataType2}", loc='left', fontsize=12, fontweight=0, color='black')
        plt.xlabel(f'{dataType2}')
        plt.ylabel(f"{dataType}")

        # Save graph
        if (os.path.isdir(path + "/IMAGES") == False):
            os.makedirs(path + "/IMAGES")
        plt.savefig(f'{path}/IMAGES/graph_{dataType}_x_{dataType2}.png', dpi=4*96, bbox_inches='tight')
        plt.clf()
        return 1

# ----------------------------------------------------------------------------------------------

# Generic function to generate line plot graphics comparing 3 dataType, which are correlated through time
# Examples: Compare temp_int, temp_ext and temp_geral through time

def generate_compare_graph (data1, data2, data3, time, dataType1, dataType2, dataType3, comparing_data, path):
    # # Cleaning outliers
    # data  = outliers_clean (data , np.sort(data))
    # data2 = outliers_clean (data2, np.sort(data2))
    # data3 = outliers_clean (data3, np.sort(data3))

    df = pd.DataFrame(list(zip(data1, data2, data3, time)), columns= [f'{dataType1}', f'{dataType2}', f'{dataType3}', 'Time'])

    # Set a graph design
    plt.style.use(u'seaborn-pastel')

    # Create graph
    plt.plot(df['Time'], df[f'{dataType1}'], marker='', color='red', linewidth=1.5, alpha=0.7, label= f'{dataType1}')
    plt.plot(df['Time'], df[f'{dataType2}'], marker='', color='blue', linewidth=1.5, alpha=0.7, label= f'{dataType2}')
    plt.plot(df['Time'], df[f'{dataType3}'], marker='', color='green', linewidth=1.5, alpha=0.7, label= f'{dataType3}')

    # Add legend (Acertar)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    # Add titles
    plt.title(f"Comparing {comparing_data}", loc='left', fontsize=12, fontweight=0, color='black')
    plt.xlabel("Time (s)")                              # Podemos entrar como parâmetro as unidades de medida
    plt.ylabel(f"{comparing_data}")

    # Save graph
    if (os.path.isdir(path + "/IMAGES") == False):
        os.makedirs(path + "/IMAGES")
    plt.savefig(f'{path}/IMAGES/graph_compare_{comparing_data}.png', dpi=4*96, bbox_inches='tight')
    plt.clf()

# ----------------------------------------------------------------------------------------------

# Generates a map using latitude and longitude data

def generate_map (latitude, longitude, path):

    df = pd.DataFrame(list(zip(latitude, longitude)), columns= ['Latitude', 'Longitude'])

    # Create a map
    map = fl.Map(location=[-21.9808416, -47.7506511], tiles="OpenStreetMap", zoom_start=9)

    # Mark all coordinates
    for row in range(0,len(df)):
        fl.CircleMarker((df.loc[row, 'Latitude'], df.loc[row, 'Longitude']), radius=7, weight=5, color='red', fill_color='red', fill_opacity=.5).add_to(map)

    # Save the map as an html 
    if (os.path.isdir(path + "/IMAGES") == False):
        os.makedirs(path + "/IMAGES")   
    map.save(f'{path}/IMAGES/Map.html')

    # Open a browser window to display the html file and screenshot the map

    driver = selenium.webdriver.Chrome(os.path.join(os.path.dirname(__file__), "DEPENDENCES/chromedriver.exe"))
    driver.set_window_size(4000, 3000) 
    driver.get(f'{path}/IMAGES/Map.html')
    sleep(5)

    driver.save_screenshot(f'{path}/IMAGES/map.png')
    driver.quit()

# ----------------------------------------------------------------------------------------------

def generate_scatter_plot (data, data2, dataType, dataType2):

    df = pd.DataFrame(list(zip(data, data2)), columns= [f'{dataType}', f'{dataType2}'])

    sns.regplot(x=df[f'{dataType2}'], y=df[f'{dataType}'], line_kws={"color":"r","alpha":0.5,"lw":4}, scatter_kws={"color":"blue","alpha":0.3, "s":10})

    # Add titles
    plt.title(f"{dataType} x {dataType2}", loc='left', fontsize=12, fontweight=0, color='black')
    plt.xlabel(f'{dataType2}')
    plt.ylabel(f"{dataType}")

    # Save graph
    plt.savefig(f'scatterplot_{dataType}_x_{dataType2}.png', dpi=96, bbox_inches='tight')
    plt.clf()

# ----------------------------------------------------------------------------------------------

