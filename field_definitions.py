import random
import string

# Define field generators


def generate_username(fake, config):
    """Generate a username based on configuration"""
    min_length = config.get("min_length", 6)
    max_length = config.get("max_length", 12)
    with_numbers = config.get("with_numbers", True)

    if with_numbers:
        return fake.user_name()
    else:
        return "".join(
            random.choice(string.ascii_lowercase)
            for _ in range(random.randint(min_length, max_length))
        )


def generate_password(fake, config):
    """Generate a password based on configuration"""
    length = config.get("length", 12)
    include_special = config.get("include_special", True)
    include_digits = config.get("include_digits", True)

    chars = string.ascii_letters
    if include_digits:
        chars += string.digits
    if include_special:
        chars += string.punctuation

    return "".join(random.choice(chars) for _ in range(length))


def generate_full_name(fake, config):
    """Generate a full name"""
    with_middle = config.get("with_middle", False)

    if with_middle:
        return f"{fake.first_name()} {fake.first_name()[0]}. {fake.last_name()}"
    else:
        return fake.name()


def generate_street_address(fake, config):
    """Generate a street address"""
    include_secondary = config.get("include_secondary", True)

    if include_secondary:
        return fake.street_address()
    else:
        return fake.building_number() + " " + fake.street_name()


def generate_credit_card(fake, config):
    """Generate a credit card number"""
    provider = config.get("provider", "any")

    if provider == "any":
        return fake.credit_card_number()
    elif provider == "visa":
        return fake.credit_card_number(card_type="visa")
    elif provider == "mastercard":
        return fake.credit_card_number(card_type="mastercard")
    else:
        return fake.credit_card_number()


def generate_date_of_birth(fake, config):
    """Generate a date of birth"""
    min_age = config.get("min_age", 18)
    max_age = config.get("max_age", 90)

    return fake.date_of_birth(minimum_age=min_age, maximum_age=max_age).strftime(
        "%Y-%m-%d"
    )


def generate_phone_number(fake, config):
    """Generate a phone number"""
    format_type = config.get("format", "standard")

    if format_type == "standard":
        return fake.phone_number()
    elif format_type == "international":
        return fake.phone_number()
    else:
        return fake.phone_number()


# Define all available fields with their configurations
field_definitions = {
    "username": {
        "display_name": "Benutzername",
        "generator": generate_username,
        "params": {
            "min_length": {
                "type": "int",
                "default": 6,
                "min": 3,
                "max": 20,
                "help": "Minimale Länge des Benutzernamens",
            },
            "max_length": {
                "type": "int",
                "default": 12,
                "min": 3,
                "max": 30,
                "help": "Maximale Länge des Benutzernamens",
            },
            "with_numbers": {
                "type": "bool",
                "default": True,
                "help": "Zahlen im Benutzernamen einschließen",
            },
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            },
        },
    },
    "email": {
        "display_name": "E-Mail",
        "generator": "email",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
    "password": {
        "display_name": "Passwort",
        "generator": generate_password,
        "params": {
            "length": {
                "type": "int",
                "default": 12,
                "min": 4,
                "max": 30,
                "help": "Länge des Passworts",
            },
            "include_special": {
                "type": "bool",
                "default": True,
                "help": "Sonderzeichen einschließen",
            },
            "include_digits": {
                "type": "bool",
                "default": True,
                "help": "Zahlen einschließen",
            },
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            },
        },
    },
    "full_name": {
        "display_name": "Vollständiger Name",
        "generator": generate_full_name,
        "params": {
            "with_middle": {
                "type": "bool",
                "default": False,
                "help": "Zweiten Vornamen einschließen",
            },
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            },
        },
    },
    "street_address": {
        "display_name": "Straßenadresse",
        "generator": generate_street_address,
        "params": {
            "include_secondary": {
                "type": "bool",
                "default": True,
                "help": "Wohnungsnummer einschließen",
            },
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            },
        },
    },
    "city": {
        "display_name": "Stadt",
        "generator": "city",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
    "state": {
        "display_name": "Bundesland",
        "generator": "state",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
    "zip_code": {
        "display_name": "Postleitzahl",
        "generator": "postcode",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
    "country": {
        "display_name": "Land",
        "generator": "country",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
    "phone_number": {
        "display_name": "Telefonnummer",
        "generator": generate_phone_number,
        "params": {
            "format": {
                "type": "select",
                "default": "standard",
                "options": ["standard", "international"],
                "label": "Format",
                "help": "Format der Telefonnummer",
            },
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            },
        },
    },
    "date_of_birth": {
        "display_name": "Geburtsdatum",
        "generator": generate_date_of_birth,
        "params": {
            "min_age": {
                "type": "int",
                "default": 18,
                "min": 1,
                "max": 100,
                "help": "Mindestalter in Jahren",
            },
            "max_age": {
                "type": "int",
                "default": 90,
                "min": 1,
                "max": 120,
                "help": "Maximalalter in Jahren",
            },
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            },
        },
    },
    "gender": {
        "display_name": "Geschlecht",
        "generator": "random_element",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
    "credit_card": {
        "display_name": "Kreditkarte",
        "generator": generate_credit_card,
        "params": {
            "provider": {
                "type": "select",
                "default": "any",
                "options": ["any", "visa", "mastercard"],
                "label": "Kartenanbieter",
                "help": "Kreditkartenanbieter",
            },
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            },
        },
    },
    "job_title": {
        "display_name": "Berufsbezeichnung",
        "generator": "job",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
    "company": {
        "display_name": "Unternehmen",
        "generator": "company",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
    "user_agent": {
        "display_name": "User-Agent",
        "generator": "user_agent",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
    "ipv4": {
        "display_name": "IPv4-Adresse",
        "generator": "ipv4",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
    "ipv6": {
        "display_name": "IPv6-Adresse",
        "generator": "ipv6",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
    "mac_address": {
        "display_name": "MAC-Adresse",
        "generator": "mac_address",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
    "uuid": {
        "display_name": "UUID",
        "generator": "uuid4",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
    "color": {
        "display_name": "Farbe",
        "generator": "color_name",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
    "currency_code": {
        "display_name": "Währungscode",
        "generator": "currency_code",
        "params": {
            "permutate": {
                "type": "bool",
                "default": False,
                "help": "Daten zufällig permutieren",
            }
        },
    },
}
