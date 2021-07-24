"""app.utils.countries.py"""
import logging
import app.io

# Default country code.

# Mapping of country names to alpha-2 codes according to
# https://en.wikipedia.org/wiki/ISO_3166-1.
# As a reference see also https://github.com/TakahikoKawasaki/nv-i18n (in Java)
# fmt: off

# fmt: on

class CountryCodeUtil:
    
    LOGGER = logging.getLogger(__name__)
    DEFAULT_COUNTRY_CODE = "XX"
    COUNTRY_NAME__COUNTRY_CODE_PATH = "country_name_country_code_path.json" #put that giant map in data folder as json 

    def __init__(self):
        self.COUNTRY_NAME__COUNTRY_CODE = app.io.load(COUNTRY_NAME__COUNTRY_CODE_PATH)
    
    def get_country_code(self,country_name):
        code = self.COUNTRY_NAME__COUNTRY_CODE.get(value, DEFAULT_COUNTRY_CODE)
        if code == DEFAULT_COUNTRY_CODE:
            # log at sub DEBUG level
            LOGGER.log(5, f"No country code found for '{country_name}'. Using '{code}'!")
        return code
    
    def add_country_code(self,country_name,country_code):
        self.COUNTRY_NAME__COUNTRY_CODE[country_name] = country_code