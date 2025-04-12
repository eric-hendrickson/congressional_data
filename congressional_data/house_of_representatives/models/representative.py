class Representative():
    def __init__(
        self,
        representative_id,
        first_name,
        middle_name,
        last_name,
        name_suffix,
        state_or_territory_full,
        state_or_territory_abbreviation,
        position_or_district,
        party,
        hometown,
        address1,
        address2,
        address3,
        phone,
        website,
        date_last_oath_of_office,
        date_resigned,
        is_voting_representative
    ):
        self._representative_id = representative_id
        self._first_name = first_name
        self._middle_name = middle_name
        self._last_name = last_name
        self._name_suffix = name_suffix
        self._state_or_territory_full = state_or_territory_full
        self._state_or_territory_abbreviation = state_or_territory_abbreviation
        self._position_or_district = position_or_district
        self._party = party
        self._hometown = hometown
        self._address1 = address1
        self._address2 = address2
        self._address3 = address3
        self._phone = phone
        self._website = website
        self._date_last_oath_of_office = date_last_oath_of_office
        self._date_resigned = date_resigned
        self._is_voting_representative = is_voting_representative

    def __str__(self):
        return f"Representative: {self._first_name} {self._last_name}"
    
    @staticmethod
    def get_parameter_names():
        parameters = [
            "representative_id",
            "first_name",
            "middle_name",
            "last_name",
            "name_suffix",
            "state_or_territory_full",
            "state_or_territory_abbreviation",
            "position_or_district",
            "party",
            "hometown",
            "address1",
            "address2",
            "address3",
            "phone",
            "website",
            "date_last_oath_of_office",
            "date_resigned",
            "is_voting_representative"
        ]
        return parameters

    def get_values_as_list(self):
        return [
            self._representative_id,
            self._first_name,
            self._middle_name,
            self._last_name,
            self._name_suffix,
            self._state_or_territory_full,
            self._state_or_territory_abbreviation,
            self._position_or_district,
            self._party,
            self._hometown,
            self._address1,
            self._address2,
            self._address3,
            self._phone,
            self._website,
            self._date_last_oath_of_office,
            self._date_resigned,
            self._is_voting_representative
        ]

    def get_representative_id(self):
        return self._representative_id

    def get_first_name(self):
        return self._first_name

    def get_middle_name(self):
        return self._middle_name

    def get_last_name(self):
        return self._last_name

    def get_name_suffix(self):
        return self._name_suffix

    def get_state_or_territory_full(self):
        return self._state_or_territory_full

    def get_state_or_territory_abbreviation(self):
        return self._state_or_territory_abbreviation

    def get_position_or_district(self):
        return self._position_or_district

    def get_party(self):
        return self._party

    def get_hometown(self):
        return self._hometown

    def get_address1(self):
        return self._address1
    
    def get_address2(self):
        return self._address2

    def get_address3(self):
        return self._address3

    def get_phone(self):
        return self._phone
    
    def get_website(self):
        return self._website

    def get_date_last_oath_of_office(self):
        return self._date_last_oath_of_office

    def get_date_resigned(self):
        return self._date_resigned

    def is_voting_representative(self):
        return self._is_voting_representative