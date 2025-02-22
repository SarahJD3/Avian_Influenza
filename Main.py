#!/usr/bin/env python3

from HPAI_maps import HPAI_map
import time
import plotly.io as pio

from Protein_Analysis.seq_frequency import multiple_sequence_welcome

"""
File name: Main.py
Author: Debra Pacheco
Created: 1/25/25
Version: 1.0
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

    while choice != "4":

        print("                    Please choose from the following options.\n")

        print("1. Generate Avian Influenza in Mammals Map")
        print("2. Generate Phylogenetic Tree")
        print("3. Generate Amino Acid Comparison")
        print("4. Exit\n")

        choice = input("Enter your choice: ")

        if choice == "1":  # Avian Influenza in Mammals Map
            fig = HPAI_map.generate_map()
            print("Map has been generated.\n")

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

        elif choice == "2":
            print("This is not currently available.\n")
            time.sleep(1)
        elif choice == "3":
            multiple_sequence_welcome()
            exit()

        elif choice == "4":
            print("Exiting program. Goodbye!")
        else:
            print("Invalid choice. Please try again.\n")
            time.sleep(1)


if __name__ == "__main__":
    main()
