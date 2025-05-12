import pytest
from faker import Faker
import string
import random
from field_definitions import (
    generate_username, generate_password, generate_full_name,
    generate_street_address, generate_credit_card, generate_date_of_birth,
    generate_phone_number, field_definitions
)

@pytest.fixture
def fake():
    """Create a Faker instance for testing."""
    return Faker('de_DE')

@pytest.fixture
def set_seed():
    """Set random seed for reproducible testing."""
    random.seed(42)
    yield
    # Reset seed after test
    random.seed(None)

def test_generate_username(fake, set_seed):
    """Test username generation."""
    # Test with default settings
    default_config = {"min_length": 6, "max_length": 12, "with_numbers": True}
    username = generate_username(fake, default_config)
    assert isinstance(username, str)
    
    # Test without numbers
    no_numbers_config = {"min_length": 6, "max_length": 12, "with_numbers": False}
    username = generate_username(fake, no_numbers_config)
    assert isinstance(username, str)
    assert all(char not in string.digits for char in username)
    assert 6 <= len(username) <= 12

def test_generate_password(fake, set_seed):
    """Test password generation."""
    # Test with default settings
    default_config = {"length": 12, "include_special": True, "include_digits": True}
    password = generate_password(fake, default_config)
    assert isinstance(password, str)
    assert len(password) == 12
    
    # Test without special characters
    no_special_config = {"length": 8, "include_special": False, "include_digits": True}
    password = generate_password(fake, no_special_config)
    assert isinstance(password, str)
    assert len(password) == 8
    assert all(char not in string.punctuation for char in password)
    
    # Test without digits
    no_digits_config = {"length": 10, "include_special": True, "include_digits": False}
    password = generate_password(fake, no_digits_config)
    assert isinstance(password, str)
    assert len(password) == 10
    assert all(char not in string.digits for char in password)

def test_generate_full_name(fake):
    """Test full name generation."""
    # Test without middle name
    no_middle_config = {"with_middle": False}
    name = generate_full_name(fake, no_middle_config)
    assert isinstance(name, str)
    
    # Test with middle name
    with_middle_config = {"with_middle": True}
    name = generate_full_name(fake, with_middle_config)
    assert isinstance(name, str)
    # Middle names typically have a period after an initial
    assert "." in name

def test_generate_street_address(fake):
    """Test street address generation."""
    # Test with secondary address
    with_secondary_config = {"include_secondary": True}
    address = generate_street_address(fake, with_secondary_config)
    assert isinstance(address, str)
    
    # Test without secondary address
    no_secondary_config = {"include_secondary": False}
    address = generate_street_address(fake, no_secondary_config)
    assert isinstance(address, str)

def test_generate_credit_card(fake):
    """Test credit card generation."""
    # Test with any provider
    any_provider_config = {"provider": "any"}
    cc = generate_credit_card(fake, any_provider_config)
    assert isinstance(cc, str)
    
    # Test with visa
    visa_config = {"provider": "visa"}
    cc = generate_credit_card(fake, visa_config)
    assert isinstance(cc, str)
    
    # Test with mastercard
    mc_config = {"provider": "mastercard"}
    cc = generate_credit_card(fake, mc_config)
    assert isinstance(cc, str)

def test_generate_date_of_birth(fake):
    """Test date of birth generation."""
    config = {"min_age": 18, "max_age": 90}
    dob = generate_date_of_birth(fake, config)
    assert isinstance(dob, str)
    
    # Test date format
    assert len(dob) == 10  # YYYY-MM-DD format
    year, month, day = dob.split('-')
    assert len(year) == 4
    assert len(month) == 2
    assert len(day) == 2
    
    # Test with different age range
    config = {"min_age": 25, "max_age": 35}
    dob = generate_date_of_birth(fake, config)
    assert isinstance(dob, str)

def test_generate_phone_number(fake):
    """Test phone number generation."""
    # Test standard format
    standard_config = {"format": "standard"}
    phone = generate_phone_number(fake, standard_config)
    assert isinstance(phone, str)
    
    # Test international format
    intl_config = {"format": "international"}
    phone = generate_phone_number(fake, intl_config)
    assert isinstance(phone, str)

def test_field_definitions_structure():
    """Test that field_definitions has the expected structure."""
    # Check that field_definitions is a dictionary
    assert isinstance(field_definitions, dict)
    
    # Check that it contains expected fields
    expected_fields = [
        "username", "email", "password", "full_name", "street_address", 
        "city", "state", "zip_code", "country", "phone_number", 
        "date_of_birth", "gender", "credit_card", "job_title", 
        "company", "user_agent", "ipv4", "ipv6", "mac_address", 
        "uuid", "color", "currency_code"
    ]
    
    for field in expected_fields:
        assert field in field_definitions
        
        # Check field structure
        field_def = field_definitions[field]
        assert "display_name" in field_def
        assert "generator" in field_def
        assert "params" in field_def
        
        # Check that params include permutate option
        assert "permutate" in field_def["params"]