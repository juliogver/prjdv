import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
from io import StringIO
@st.cache_data()
def load_data():
    api_url = "https://www.data.gouv.fr/fr/datasets/r/e32f7675-913b-4e01-b8c8-0a29733e4407"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        try:
            parking_data = pd.read_csv(StringIO(response.text), low_memory = False)
            return parking_data
        except pd.errors.ParserError as e:
            st.error(f"Failed to parse data. Parser error: {str(e)}")
            return None
    else:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")
        return None
    
parking_data = load_data()    

department_coordinates = {
    '69': (45.75, 4.85),   # Lyon, Rhône
    '75': (48.86, 2.35),   # Paris
    '33': (44.84, -0.58),  # Bordeaux, Gironde
    '44': (47.22, -1.55),  # Nantes, Loire-Atlantique
    '38': (45.19, 5.73),   # Grenoble, Isère
    '92': (48.89, 2.24),   # Hauts-de-Seine
    '34': (43.61, 3.87),   # Montpellier, Hérault
    '59': (50.63, 3.06),   # Lille, Nord
    '67': (48.58, 7.75),   # Strasbourg, Bas-Rhin
    '60': (49.42, 2.82),   # Oise
    '57': (49.12, 6.18),   # Moselle
    '49': (47.47, -0.55),  # Angers, Maine-et-Loire
    '73': (45.54, 5.93),   # Savoie
    '17': (45.65, -1.03),  # La Rochelle, Charente-Maritime
    '90': (47.64, 6.87),   # Territoire de Belfort
    '86': (46.58, 0.34),   # Vienne
    '87': (45.83, 1.26),   # Haute-Vienne
    '83': (43.47, 6.77),   # Var
    '61': (48.43, -0.1),   # Orne
    '40': (43.98, -1.54),  # Landes
    '74': (46.05, 6.36),   # Haute-Savoie
    '94': (48.78, 2.41),   # Val-de-Marne
    '01': (46.2, 5.22),   # Ain
    '02': (49.57, 3.62),  # Aisne
    '03': (46.12, 3.42),  # Allier
    '04': (44.1, 6.24),   # Alpes-de-Haute-Provence
    '05': (44.57, 6.08),  # Hautes-Alpes
    '06': (43.7, 7.26),   # Alpes-Maritimes
    '07': (44.68, 4.63),  # Ardèche
    '08': (49.77, 4.72),  # Ardennes
    '09': (42.93, 1.62),  # Ariège
    '10': (48.3, 4.08),   # Aube
    '11': (43.22, 2.35),  # Aude
    '12': (44.38, 2.58),  # Aveyron
    '13': (43.47, 5.42),  # Bouches-du-Rhône
    '14': (49.18, -0.37),  # Calvados
    '15': (45.03, 2.77),  # Cantal
    '16': (45.65, 0.15),  # Charente
    '18': (47.08, 2.5),   # Cher
    '19': (45.13, 1.52),  # Corrèze
    '20': (41.89, 8.74),  # Corse
    '21': (47.33, 4.83),  # Côte-d'Or
    '22': (48.52, -2.77),  # Côtes-d'Armor
    '23': (45.82, 1.73),  # Creuse
    '24': (45.18, 0.72),  # Dordogne
    '25': (47.25, 6.03),  # Doubs
    '26': (44.63, 4.87),  # Drôme
    '27': (49.1, 1.1),   # Eure
    '28': (48.45, 1.38),  # Eure-et-Loir
    '29': (48.17, -4.3),  # Finistère
    '2A': (41.92, 8.73),  # Corse-du-Sud
    '2B': (42.23, 9.1),  # Haute-Corse
    '30': (43.83, 4.36),  # Gard
    '31': (43.6, 1.44),  # Haute-Garonne
    '32': (43.7, 0.62),  # Gers
    '35': (48.12, -1.65),  # Ille-et-Vilaine
    '36': (46.78, 1.62),  # Indre
    '37': (47.33, 0.72),  # Indre-et-Loire
    '38': (45.19, 5.73),  # Isère
    '39': (46.78, 5.65),  # Jura
    '41': (47.33, 1.15),  # Loir-et-Cher
    '42': (45.43, 4.39),  # Loire
    '43': (45.08, 3.89),  # Haute-Loire
    '45': (47.9, 2.17),   # Loiret
    '46': (44.45, 1.44),  # Lot
    '47': (44.5, 0.66),   # Lot-et-Garonne
    '48': (44.52, 3.51),  # Lozère
    '51': (49.25, 4.03),  # Marne
    '52': (48.03, 4.9),   # Haute-Marne
    '53': (48.08, -0.77),  # Mayenne
    '54': (48.68, 6.17),  # Meurthe-et-Moselle
    '55': (49.55, 5.8),   # Meuse
    '56': (47.83, -3.43),  # Morbihan
    '58': (47.08, 3.34),  # Nièvre
    '62': (50.63, 2.28),  # Pas-de-Calais
    '63': (45.65, 3.12),  # Puy-de-Dôme
    '64': (43.35, -0.7),  # Pyrénées-Atlantiques
    '65': (43.23, 0.07),  # Hautes-Pyrénées
    '66': (42.6, 2.67),   # Pyrénées-Orientales
    '68': (48.08, 7.36),  # Haut-Rhin
    '70': (47.62, 6.16),  # Haute-Saône
    '71': (46.8, 4.47),   # Saône-et-Loire
    '72': (47.98, 0.13),  # Sarthe
    '76': (49.67, 0.98),  # Seine-Maritime
    '77': (48.85, 2.77),  # Seine-et-Marne
    '78': (48.82, 1.97),  # Yvelines
    '79': (46.32, -0.49),  # Deux-Sèvres
    '80': (49.9, 2.3),   # Somme
    '81': (43.93, 1.9),   # Tarn
    '82': (44.0, 1.35),   # Tarn-et-Garonne
    '84': (43.95, 5.15),  # Vaucluse
    '85': (46.72, -1.43),  # Vendée
    '88': (48.18, 6.43),  # Vosges
    '89': (47.8, 3.57),   # Yonne
    '91': (48.47, 2.17),  # Essonne
}

st.title("P-Finder")
st.subheader("Find a parking spot !")
selected_department = st.text_input("Enter Department Number (e.g., 69):")
@st.cache_data()
def map(selected_department):
    # Create a text input for the department number

    if selected_department:
        if selected_department in department_coordinates:
            # Get the coordinates for the selected department
            latitude, longitude = department_coordinates[selected_department]
            # Create Pydeck map for location
            location_scatterplot = pdk.Layer(
                "ScatterplotLayer",
                data=parking_data,
                get_position=["Xlong", "Ylat"],
                get_radius=100,
                get_fill_color=[255, 0, 0, 200],
                pickable=True,
            )

            location_view_state = pdk.ViewState(
                latitude=latitude,
                longitude=longitude,
                zoom=10,
            )

            location_pydeck_map = pdk.Deck(
                layers=[location_scatterplot],
                initial_view_state=location_view_state,
            )

            # Streamlit app

            st.pydeck_chart(location_pydeck_map)
map(selected_department)

# Convert the 'insee' column to strings
parking_data['Department'] = parking_data['insee'].astype(str)

# Group departments by the first two digits of 'insee' and count the number of parking spots
parking_counts_by_group = parking_data['Department'].str[:2].value_counts().reset_index()
parking_counts_by_group.columns = ['Department', 'Number of Parking Spots']

# Filter and group by department for free parking spots
free_parking_data = parking_data[parking_data['gratuit'] == 1]
free_parking_counts_by_department = free_parking_data['Department'].str[:2].value_counts().reset_index()
free_parking_counts_by_department.columns = ['Department', 'Number of Free Parking Spots']


# Create a list of unique departments with free parking spots
departments_with_free_parking = free_parking_data['Department'].str[:2].unique()



# Filter free parking data for the selected department
selected_department_free_parking_data = free_parking_data[free_parking_data['Department'].str[:2] == selected_department]

# Display the names of free parking spots for the selected department
if not selected_department_free_parking_data.empty:
    st.subheader(f"Free Parking Spots in Department {selected_department}")
    st.table(selected_department_free_parking_data[['nom', 'adresse','nb_places','type_ouvrage','info']])
else:
    st.write(f"No Free Parking Spots found in Department {selected_department}")
st.subheader("-------------------------------------------------------------------------------")

st.header("Where to find a free parking ?")


# Display a bar chart for the number of free parking spots by department
st.subheader("Free Parking Spots by Department")
st.bar_chart(free_parking_counts_by_department.set_index('Department'))
st.subheader("-------------------------------------------------------------------------------")
st.header("Cheapest Parking Spots")
# Create a selectbox to choose the parking tariff duration
selected_tariff_duration = st.selectbox("Select Tariff Duration", ['tarif_1h', 'tarif_2h', 'tarif_3h', 'tarif_4h', 'tarif_24h'])

# Filter parking data for the selected department
selected_department_parking_data = parking_data[parking_data['Department'].str[:2] == selected_department]

# Exclude the free parking spots from the selected department
selected_department_parking_data = selected_department_parking_data[~selected_department_parking_data['nom'].isin(selected_department_free_parking_data['nom'])]

# Filter parking spots with tariffs greater than zero for the selected duration
selected_department_parking_data = selected_department_parking_data[selected_department_parking_data[selected_tariff_duration] > 0]

# Sort the parking data by the selected tariff duration in ascending order
selected_department_parking_data = selected_department_parking_data.sort_values(by=selected_tariff_duration, ascending=True)

# Display the names and tariffs of the 10 cheapest parking spots
if not selected_department_parking_data.empty:
    # Format the tariff column to include the euro symbol
    selected_department_parking_data[selected_tariff_duration] = selected_department_parking_data[selected_tariff_duration].apply(lambda x: f"{x:.2f} €")
    st.table(selected_department_parking_data[['nom','adresse',selected_tariff_duration,'nb_places','hauteur_max','info']].head(5))
else:
    st.write(f"No Parking Spots found in Department {selected_department}")
st.subheader("-------------------------------------------------------------------------------")
# Create a selectbox to choose the vehicle type
selected_vehicle_type = st.selectbox("Select Vehicle Type", ['moto', 'voiture', 'camionette', 'camion'])

st.header("Parking Spots for Selected Vehicle Type")
# Filter parking data for the selected department
selected_department_parking_data = parking_data[parking_data['Department'].str[:2] == selected_department]

# Filter parking data based on vehicle type and height restrictions
if selected_vehicle_type == 'camionette':
    selected_department_parking_data = selected_department_parking_data[selected_department_parking_data['hauteur_max'] > 170]
elif selected_vehicle_type == 'camion':
    selected_department_parking_data = selected_department_parking_data[selected_department_parking_data['hauteur_max'] > 380]

# Check if the parking spots have a "type_ouvrage" of "enclos_en_surface" and no height restrictions
if selected_vehicle_type == 'moto' or selected_vehicle_type == 'voiture':
    selected_department_parking_data = selected_department_parking_data[(selected_department_parking_data['type_ouvrage'] == 'enclos_en_surface') | (selected_department_parking_data['hauteur_max'].isna())]

# Sort the parking data by the selected tariff duration in ascending order
selected_department_parking_data = selected_department_parking_data.sort_values(by=selected_tariff_duration, ascending=True)

# Display the parking spots
if not selected_department_parking_data.empty:
    st.write(f"Parking Spots for {selected_vehicle_type}s :")
    
    # Display the height restriction only for camionette and camion
    if selected_vehicle_type == 'camionette' or selected_vehicle_type == 'camion' or selected_vehicle_type == 'moto' or selected_vehicle_type == 'voiture':
        st.table(selected_department_parking_data[['nom', 'adresse', 'hauteur_max', 'nb_places', 'info']].head(5))
    else:
        st.table(selected_department_parking_data[['nom', 'adresse', 'nb_places', 'info']].head(5))
else:
    st.write(f"No Parking Spots found for {selected_vehicle_type} in Department {selected_department}")

st.subheader("-------------------------------------------------------------------------------")

import altair as alt
import folium
from streamlit_folium import folium_static

def map_elec():
    # Create a Folium map centered on an initial location (e.g., Paris)
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

    # Filter parking data for electric vehicles
    ev_parking_data = parking_data[parking_data['nb_voitures_electriques'] > 0]

    # Add markers for each parking with electric vehicles
    for index, row in ev_parking_data.iterrows():
        folium.Marker(
            location=[row['Ylat'], row['Xlong']],
            popup=row['nom'],
        ).add_to(m)

    # Display the Folium map in Streamlit
    st.subheader("If you have an electric vehicle!")
    folium_static(m)

map_elec()

def ratio_electrique():
    # Create a new column "Electric Ratios" for the number of electric vehicle spaces relative to total spaces
    parking_data['Electric Ratios'] = parking_data['nb_voitures_electriques'] / parking_data['nb_places']

    # Create an Altair histogram for the electric vehicle ratios
    histogram_ratios_electriques = alt.Chart(parking_data).mark_bar().encode(
        alt.X('Electric Ratios:Q', bin=True, title='Electric Ratios / Total'),
        alt.Y('count()', title='Number of parkings'),
        color=alt.value('green')
    ).properties(
        width=400,
        height=300,
        title="Histogram of Ratios (Electric / Total) per parking"
    )

    histogram_ratios_electriques

ratio_electrique()

def map_velo():
    # Create a Folium map centered on an initial location (e.g., Paris)
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

    # Filter parking data for bicycle facilities
    bike_parking_data = parking_data[parking_data['nb_velo'] > 0]

    # Add markers for each bike parking facility
    for index, row in bike_parking_data.iterrows():
        folium.Marker(
            location=[row['Ylat'], row['Xlong']],
            popup=row['nom'],
        ).add_to(m)

    # Display the Folium map in Streamlit
    st.subheader("If you're a cyclist!")
    folium_static(m)


map_velo()

def ratio_velo():
    # Calculate the ratios
    parking_data['Bicycle Ratios'] = parking_data['nb_velo'] / parking_data['nb_places']

    # Create a scatter plot of the bicycle ratios relative to the total number of parkings
    scatter_ratio_velo = alt.Chart(parking_data).mark_circle().encode(
        x=alt.X('Bicycle Ratios:Q', title='Ratio (Bicycles / Total)'),
        y=alt.Y('nb_places:Q', title='Number of parkings'),
        tooltip=['nom:N'],
        color=alt.value('blue')
    ).properties(
        width=400,
        height=400,
        title="Scatter Plot of Ratio (Bicycles / Total) per parking"
    )

    scatter_ratio_velo

ratio_velo()

def sidebar():
    # Sidebar for links LinkedIn and GitHub
    st.sidebar.subheader("Mes liens")
    linkedin_link = "https://www.linkedin.com/in/jules-gravier-4806941b7/"
    github_link = "https://github.com/juliogver"

    st.sidebar.subheader("GRAVIER JULES")

    st.sidebar.markdown(f"[LinkedIn]({linkedin_link})")
    st.sidebar.markdown(f"[Github]({github_link})")

sidebar()











