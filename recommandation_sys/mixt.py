# -*- coding: utf-8 -*-

import os
import pdfplumber
import pandas as pd
import re
import cv2
import numpy as np

def recommand(file):
    # Path to the PDF file
    pdf_path = "analysis/"+file
    # Get the base name of the PDF file
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Define the output folder
    output_folder = 'analysis/'

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Dictionaries to store the data
    data = {
        "category": [],
        "test_name": [],
        "value": [],
        "status": []
    }

    # Unified reference values for BILAN MINÉRAUX
    reference_values = {
        'BILAN MINÉRAUX': {
            'low': -25,
            'high': 25,
            'status_low': 'à corriger_Augmenter la valeur',
            'status_high': 'à corriger_Diminuer la valeur',
            'status': 'zone idéale'
        },
        'RATIOS': {
            'low': -33,
            'high': 33,
            'status_low': 'à corriger_Augmenter la valeur',
            'status_high': 'à corriger_Diminuer la valeur',
            'status': 'zone idéale'
        },
        'BILAN MÉTAUX LOURDS': {
            'low': 0,
            'high': 33,
            'status_low': 'à corriger_Augmenter la valeur',
            'status_high': 'à corriger_Diminuer la valeur',
            'status': 'zone idéale'
        },
        'VITAMINES': {
            'low': 66,
            'high': 100,
            'status_low': 'à corriger_Augmenter la valeur',
            'status_high': 'à corriger_Diminuer la valeur',
            'status': 'zone idéale'
        }
    }

    # Function to preprocess image for better OCR results
    def preprocess_image_for_ocr(image):
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return binary_image

    # Function to extract textual values
    def extract_textual_values(text, section_title):
        found_sections = set()
        start = False
        for line in text.split('\n'):
            if section_title in line:
                start = True
                continue
            if start:
                if "zone idéale" in line or not line.strip():
                    break
                match = re.match(r"(.*?)\s+(-?\d+%?)\s*([\w\s]*)", line.strip())
                if match:
                    test_name, value, status_text = match.groups()
                    if test_name not in found_sections:  # Ensure unique entries
                        status = get_status(section_title, value.strip('%'))
                        data["category"].append(section_title)
                        data["test_name"].append(test_name.strip())
                        data["value"].append(value.strip('%'))
                        data["status"].append(status)
                        found_sections.add(test_name)

    # Function to determine the status based on reference values
    def get_status(section_title, value):
        value = float(value)
        if section_title in reference_values:
            ref = reference_values[section_title]
            if value < ref['low']:
                return ref['status_low']
            elif value > ref['high']:
                return ref['status_high']
            else:
                return ref['status']
        return 'unknown'

    # Read the PDF file and extract text
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Extract textual values
                extract_textual_values(text, "BILAN MINÉRAUX")
                extract_textual_values(text, "RATIOS")
                extract_textual_values(text, "BILAN MÉTAUX LOURDS")
                extract_textual_values(text, "VITAMINES")

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # List of required test names
    required_tests = [
        "Calcium Ca", "Cuivre Cu", "Fer Fe", "Iode I", "Manganèse Mn",
        "Phosphore P", "Potassium K", "Sélénium Se", "Sodium Na", "Zinc Zn",
        "Vitamine E", "Vitamine C", "Vitamine B6", "Vitamine B9", "Vitamine B12"
    ]

    # Filter the DataFrame to keep only the required test names
    df_filtered = df[df['test_name'].isin(required_tests)]

    # Further filter the data based on status criteria
    filtered_data = df_filtered[(df_filtered['status'] == 'à corriger_Augmenter la valeur') |
                                (df_filtered['status'] == 'à corriger_Diminuer la valeur')]

    # Load the meals data
    meals_df = pd.read_csv('recommandation_sys/allplates.csv')

    # Ensure columns are stripped of any extra spaces
    filtered_data.columns = filtered_data.columns.str.strip()
    meals_df.columns = meals_df.columns.str.strip()

    # Check if the test names in filtered_data are present in the columns of meals_df
    comparison_results_increase = []
    comparison_results_decrease = []

    for index, row in filtered_data.iterrows():
        test_name = row['test_name']
        value = row['value']
        status = row['status']
        if test_name in meals_df.columns:
            for idx, meal_row in meals_df.iterrows():
                ssgrp_nom = meal_row['ssgrp_nom'] if 'ssgrp_nom' in meal_row else None
                meal_name = meal_row['Food name']
                meal_value = meal_row[test_name]
                result = {
                    'ssgrp_nom': ssgrp_nom,
                    'meal_name': meal_name,
                    'test_name': test_name,
                    'test_value': value,
                    'meal_value': meal_value
                }
                if status == 'à corriger_Augmenter la valeur':
                    comparison_results_increase.append(result)
                elif status == 'à corriger_Diminuer la valeur':
                    comparison_results_decrease.append(result)

    # Convert the comparison results to DataFrames
    comparison_df_increase = pd.DataFrame(comparison_results_increase)
    comparison_df_decrease = pd.DataFrame(comparison_results_decrease)

    # Save the comparison results to new CSV files
    comparison_df_increase.to_csv(os.path.join(output_folder, f'{base_name}_comparison_increase.csv'), index=False)
    comparison_df_decrease.to_csv(os.path.join(output_folder, f'{base_name}_comparison_decrease.csv'), index=False)

    print("Comparison complete. Results saved to 'comparison_increase.csv' and 'comparison_decrease.csv'.")


