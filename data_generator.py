import pandas as pd
import numpy as np
from faker import Faker
import random
from field_definitions import field_definitions


def generate_data(selected_fields, num_records=10, locale="de_DE", seed=None):
    """
    Generate synthetic data based on selected fields and their configurations.

    Args:
        selected_fields (dict): Dictionary mapping field names to their configurations
        num_records (int): Number of records to generate
        locale (str): Locale to use for generation
        seed (int, optional): Random seed for reproducibility

    Returns:
        pandas.DataFrame: DataFrame containing the generated data
    """
    # Set seed if provided
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # Initialize faker with the selected locale
    fake = Faker(locale)
    if seed is not None:
        Faker.seed(seed)

    # Initialize empty dataframe
    df = pd.DataFrame()

    # Generate data for each selected field
    for field_name, field_config in selected_fields.items():
        if field_name not in field_definitions:
            continue

        # Get the field definition
        definition = field_definitions[field_name]

        # Generate the data based on the generator function
        generator_function = definition["generator"]

        # Generate the column
        if callable(generator_function):
            column_data = [
                generator_function(fake, field_config) for _ in range(num_records)
            ]
        else:
            # Use the field name as the faker method
            try:
                if generator_function == "state":
                    # Handle state generation differently based on locale
                    if locale == "en_US":
                        column_data = [fake.state() for _ in range(num_records)]
                    elif locale == "de_DE":
                        # German states
                        german_states = [
                            "Baden-Württemberg",
                            "Bayern",
                            "Berlin",
                            "Brandenburg",
                            "Bremen",
                            "Hamburg",
                            "Hessen",
                            "Mecklenburg-Vorpommern",
                            "Niedersachsen",
                            "Nordrhein-Westfalen",
                            "Rheinland-Pfalz",
                            "Saarland",
                            "Sachsen",
                            "Sachsen-Anhalt",
                            "Schleswig-Holstein",
                            "Thüringen",
                        ]
                        column_data = [
                            random.choice(german_states) for _ in range(num_records)
                        ]
                    else:
                        # For other locales, use a generic approach
                        column_data = [f"Region {i+1}" for i in range(num_records)]
                elif generator_function == "random_element" and field_name == "gender":
                    # Handle gender field
                    if locale.startswith("de"):
                        column_data = [
                            random.choice(["männlich", "weiblich", "divers"])
                            for _ in range(num_records)
                        ]
                    else:
                        column_data = [
                            random.choice(["male", "female", "other"])
                            for _ in range(num_records)
                        ]
                else:
                    # Standard case for other fields
                    faker_method = getattr(fake, generator_function)
                    column_data = [faker_method() for _ in range(num_records)]
            except AttributeError as e:
                # Fallback for methods not supported in this Faker version
                print(f"Attribute error for {generator_function}: {str(e)}")
                column_data = [
                    f"[Generator '{generator_function}' nicht verfügbar]"
                    for _ in range(num_records)
                ]

        # Add the column to the dataframe
        df[definition.get("display_name", field_name)] = column_data

    # Apply permutations if needed
    # This is a simplified version - you might need to adjust based on your requirements
    for field_name, field_config in selected_fields.items():
        if field_name not in field_definitions:
            continue

        # Check if permutation is enabled for this field
        if field_config.get("permutate", False):
            column_name = field_definitions[field_name].get("display_name", field_name)
            if column_name in df.columns:
                # Shuffle the column data
                shuffled = df[column_name].values.copy()
                np.random.shuffle(shuffled)
                df[column_name] = shuffled

    return df
