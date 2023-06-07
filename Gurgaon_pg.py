# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 18:31:10 2023

@author: Plaksha
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import random
import pandas as pd

# Create empty lists to store the scraped data
rents = []
locations = []
property_urls = []
furnishing_statuses = []
areas = []
rents = []
property_types = []
property_type_details = []
available_fors = []
operating_sinces = []
total_beds_list = []
parking_availables = []
electricity_charges_includeds = []
notice_periods = []
food_charges_includeds = []
food_availables = []
available_pg_services_list = []
room_types = []
gate_closing_times = []
security_deposits = []
area_sq_feet_list = []
latitudes = []
longitudes = []

# Iterate over all the pages
for page in range(1, 11):  # Adjust the range as per the total number of pages you want to scrape
    # Define the URL for each page
    url = f"hidden for privacy purposes"
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the property buttons
    property_buttons = soup.find_all('button', class_='tlSrtlst shortlistcontainerlink1 DSE_Rental_D19')
    
    # Iterate over the property buttons on the current page
    for button in property_buttons:
        # Extract the required details from the button's attributes
        rent = button['data-rent']
        location = button['data-sublocalityname']
        property_url = button['data-url']
        furnishing_status = button['data-propstatus']
        area = button['data-area']
        rent = button['data-totalrent']
        property_type = button['data-propertytype']
        
        # Send a GET request to the property's individual page
        property_response = requests.get(property_url)
        property_soup = BeautifulSoup(property_response.text, 'html.parser')
        
        # Find the div containing the additional details
        project_info_box = property_soup.find('div', class_='projectInfoBoxUl')
        
        # Initialize the variables for additional details
        property_type_detail = ""
        available_for = ""
        operating_since = ""
        total_beds = ""
        parking_available = ""
        electricity_charges_included = ""
        notice_period = ""
        food_charges_included = ""
        food_available = ""
        available_pg_services = ""
        room_type = ""
        gate_closing_time = ""
        security_deposit = ""
        area_sq_feet = ""
        latitude = ""
        longitude = ""
        
        # Extract the additional details from the div
        for li in project_info_box.find_all('div', class_='projectInfoBoxLi'):
            li_data = li.find('div', class_='projectLiData')
            if li_data:
                text = li_data.text.strip()
                if text.startswith("Property Type"):
                    property_type_detail = text.split("Property Type")[-1].strip()
                elif text.startswith("Available For"):
                    available_for = text.split("Available For")[-1].strip()
                elif text.startswith("Operating Since"):
                    operating_since = text.split("Operating Since")[-1].strip()
                elif text.startswith("Total Number of Bed"):
                    total_beds = text.split("Total Number of Bed")[-1].strip()
                elif text.startswith("Parking available"):
                    parking_available = text.split("Parking available")[-1].strip()
                elif text.startswith("Electricity Charges Included"):
                    electricity_charges_included = text.split("Electricity Charges Included")[-1].strip()
                elif text.startswith("Notice Period"):
                    notice_period = text.split("Notice Period")[-1].strip()
                elif text.startswith("Food Charges Included"):
                    food_charges_included = text.split("Food Charges Included")[-1].strip()
                elif text.startswith("Food Available"):
                    food_available = text.split("Food Available")[-1].strip()
                elif text.startswith("Available PG Services"):
                    available_pg_services = text.split("Available PG Services")[-1].strip()
                elif text.startswith("Room Type"):
                    room_type = text.split("Room Type")[-1].strip()
                elif text.startswith("Gate Closing Time"):
                    gate_closing_time = text.split("Gate Closing Time")[-1].strip()
                elif text.startswith("Security Deposit"):
                    security_deposit = text.split("Security Deposit")[-1].strip()
                elif text.startswith("Area"):
                    area_match = re.findall(r'\d+', text)
                    area_sq_feet = area_match[0] if area_match else ""
        
        # Extract the latitude and longitude
        latitude = property_soup.find("input", id="hd_plat")["value"]
        longitude = property_soup.find("input", id="hd_plang")["value"]
        
        # Append the data to the respective lists
        rents.append(rent)
        locations.append(location)
        property_urls.append(property_url)
        furnishing_statuses.append(furnishing_status)
        areas.append(area)
        rents.append(rent)
        property_types.append(property_type)
        property_type_details.append(property_type_detail)
        available_fors.append(available_for)
        operating_sinces.append(operating_since)
        total_beds_list.append(total_beds)
        parking_availables.append(parking_available)
        electricity_charges_includeds.append(electricity_charges_included)
        notice_periods.append(notice_period)
        food_charges_includeds.append(food_charges_included)
        food_availables.append(food_available)
        available_pg_services_list.append(available_pg_services)
        room_types.append(room_type)
        gate_closing_times.append(gate_closing_time)
        security_deposits.append(security_deposit)
        area_sq_feet_list.append(area_sq_feet)
        latitudes.append(latitude)
        longitudes.append(longitude)
        
        # Generate a random delay between 3 and 6 seconds
        delay = random.uniform(3, 6)
        time.sleep(delay)

# Create a DataFrame from the scraped data
data = pd.DataFrame({
    'rent': rents,
    'Location': locations,
    
    'Furnishing Status': furnishing_statuses,
    'Area': areas,
    'Rent': rents,
    'Property Type': property_types,
    'Property Type Detail': property_type_details,
    'Available For': available_fors,
    'Operating Since': operating_sinces,
    'Total Number of Beds': total_beds_list,
    'Parking Available': parking_availables,
    'Electricity Charges Included': electricity_charges_includeds,
    'Notice Period': notice_periods,
    'Food Charges Included': food_charges_includeds,
    'Food Available': food_availables,
    'Available PG Services': available_pg_services_list,
    'Room Type': room_types,
    'Gate Closing Time': gate_closing_times,
    'Security Deposit': security_deposits,
    'Area (sq_feet)': area_sq_feet_list,
    'Latitude': latitudes,
    'Longitude': longitudes
})

# Save the DataFrame to a CSV file
data.to_csv('scraped_data.csv', index=False)
