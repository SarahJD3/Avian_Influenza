#!/usr/bin/env python3
from HPAI_maps.HPAI_Animal_map import generate_animal_map
from HPAI_maps.scrape_fluview import scrape_fluview_data  # Import the scraping function
from HPAI_maps.HPAI_Human_map import generate_human_map
from Phylogenetics.Print_tree import show_file_content
import time
import plotly.io as pio
import os


"""
File name: Main.py
Author: Debra Pacheco, Victoria, Janessa, Sarah Schoem
Created: 1/25/25
Edited: 2/13/25
Version: 1.1
Description:
    This script will run the Avian Influenza Genomics and Phylogenetics Comparison Tool and will allow the user to
    choose what analysis to run as well as input data if required.

License: MIT License
"""
def main():
    print("     Welcome to the Avian Influenza Genomics and Phylogenetics Comparison Tool!!")
    print("        *******************************************************************        ")
    print("  This program is under construction and has limited capabilities. Please be patient.")
    print("        *******************************************************************        ")

    choice = 0

    # Define the states to fetch data for (no year dropdown anymore)
    states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
        "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NC", "ND", "OH",
        "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "FL"
    ]

    while choice != "7":

        print("                    Please choose from the following options.\n")

        print("1. Generate Avian Influenza in Mammals Map")
        print("2. Generate Human H5 Cases Map")
        print("3. Generate Phylogenetic Tree")
        print("4. Generate Nucleotide Comparison")
        print("5. Generate Protein Comparison")
        print("6. Exit\n")

        choice = input("Enter your choice: ")

        if choice == "1":   # Avian Influenza in Mammals Map
            fig = HPAI_Animal_map.generate_animal_map()
            print("Animal Map has been generated.\n")


# Feature disabled
# Needs kaleido package - also no option to choose which year to print
            # Option to save map
#            answer = "0"
#            while answer != "N":
#                answer = input("Would you like to save the map to file? Y/N ")
#                if answer.upper() == "Y":
#                    image = pio.to_image(fig, format="jpeg")
#                    with open("HPAI_mammals.jpeg", "wb") as file:
#                        file.write(image)
#                if answer.upper() == "N":
#                    print("Map not saved. Showing map image.\n")
#                else:
#                    print("Invalid choice.\nWould you like to save the map? Please choose Y for yes or N for no.\n")



            # Map is automatically shown on screen
            fig.show()

        elif choice == "2":  # Generate Human H5 Cases Map
            print("Fetching FluView data...\n")

            # Fetch FluView data (no year selection now)
            fluview_data = scrape_fluview_data()

            # Check if human data was fetched
            if fluview_data.empty:
                print("No human data retrieved.")
            else:
                fig = generate_human_map()  # Call without passing fluview_data

                # Check if the figure was successfully created
                if fig is not None:
                    print("Human Map has been generated.\n")
                    fig.show()  # Only call show() if fig is not None
                else:
                    print("Failed to generate the human map due to missing or invalid 'Year' data.")

        elif choice == "3":  # Print Phylogenetic Tree on Screen
            print("Fetching Phylogenetic Tree")
            from Phylogenetics.Print_tree import show_file_content  # Import the function to show tree
            show_file_content("tree_analysis_output.txt")  # Call the function to show the tree


        elif choice in {"4", "5"}:
            print("This feature is not currently available.\n")
            time.sleep(1)

        elif choice == "6":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.\n")
            time.sleep(1)

if __name__ == "__main__":
    main()
