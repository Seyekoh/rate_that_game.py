#!/usr/bin/env python3
"""
rate_that_game.py

Script that will calculate the rating of a game based on the ratings
of its components (graphics, sound, gameplay, etc.) and the weights
assigned to each component.

The user will be able to add additional components and their weights
as needed. The script will then calculate the overall rating of the game
and print it in the console.

Usage:
    python rate_that_game.py

Requirements:
- pandas

Author: Seyekoh
Date: 27-March-2025
"""
import sys
import pandas as panda

def calculate_rating(weights):
    # Calculates the overall rating based on the weights and criteria.
    print("Calculating overall rating...")
    total_weight = sum(weights.values())
    if total_weight == 0:
        print("Total weight is 0. Cannot calculate rating.")
        return
    overall_rating = sum(weight * (index + 1) for index, weight in enumerate(weights.values())) / total_weight
    print(f"\nOverall rating calculated: {overall_rating:.2f}/20.0")

def configure_weights(criteria_dict):
    # Prompts the user to configure weights/ratings for each criterion.
    # Returns a dictionary with criteria as keys and weights as values.
    weights = {}
    print("\nConfiguring ratings for each criterion...")
    for category, criterions in criteria_dict.items():
        print(f"\nCategory: {category}")
        for criterion in criterions:
            while True:
                try:
                    weight = int(input(f"Enter rating for '{criterion}' (0-10): ").strip())
                    if 0 <= weight <= 10:
                        weights[criterion] = weight
                        print(f"Rating for '{criterion}' set to {weight}.")
                        break
                    else:
                        print("Rating must be between 0 and 10. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")

    print("\nRatings configured successfully.")
    return weights


def prompt_user_for_additional_criteria(criteria_dict):
    # Prompts the user to add any additional criteria.
    # Returns the updated criteria dictionary.
    print("\nWould you like to add any additional criteria? (yes/no)")
    user_input = input().strip().lower()
    if user_input == 'yes' or user_input == 'y':
        while True:
            category = input("Enter the category (or type 'done' to finish): ").strip()
            if category.lower() == 'done':
                print("Finished adding criteria.")
                break
            criterion = input(f"Enter the criterion for '{category}': ").strip()
            if criterion.lower() == 'cancel':
                print("Cancelled adding criteria.")
                response = input("Would you like to add more criteria? (yes/no): ").strip().lower()
                if response == 'yes' or response == 'y':
                    continue
                else:
                    print("Exiting criteria addition.")
                    break
            if category not in criteria_dict:
                criteria_dict[category] = []
            criteria_dict[category].append(criterion)
            print(f"Added '{criterion}' to '{category}' category.")
    elif user_input != 'no' and user_input != 'n':
        print("Invalid input. Please enter 'yes' or 'no'.")
        criteria_dict = prompt_user_for_additional_criteria(criteria_dict)
    else:
        print("No additional criteria added.")
    return criteria_dict

def display_dict_to_user(criteria_dict):
    print("\nOrganized Criteria:")
    for category, criterions in criteria_dict.items():
        print(f"\t{category}: \n\t\t{'\n\t\t'.join(criterions)}")
    return

def load_criteria():
    # Loads the criteria from a parquet file and returns it as a DataFrame.
    try:
        criteria = panda.read_parquet(r"Resources\rating_criteria.parquet")
        print("Criteria loaded successfully.")
        return criteria
    except Exception as e:
        print(f"Error loading criteria: \n\t{e}")
        sys.exit(1)

def split_criteria(criteria):
    # Splits the criteria into categories and criterions.
    # Returns a dictionary with categories as keys and lists of criterions as values.
    split_criteria = {}
    for _, row in criteria.iterrows():
        category = row['Category']
        criterion = row['Criterion']
        if category not in split_criteria:
            split_criteria[category] = []
        split_criteria[category].append(criterion)
    print("Criteria split into categories successfully.")
    return split_criteria

def main():
    print("\nWelcome to Rate That Game!")

    # Load criteria from the parquet file
    print("\nLoading criteria...")
    rating_criteria = load_criteria()

    # Split the criteria into a dictionary for easier access
    print("Organizing criteria...")
    criteria_dict = split_criteria(rating_criteria)

    # Display the organized criteria to the user and
    # prompt them to add any additional components or weights if needed
    display_dict_to_user(criteria_dict)

    # Prompt user for additional components
    prompt_user_for_additional_criteria(criteria_dict)

    # Configure weights for each criterion
    weights = configure_weights(criteria_dict)

    # Calculate and display the overall rating based on the weights and criteria
    calculate_rating(weights)

if __name__ == "__main__":
    main()
