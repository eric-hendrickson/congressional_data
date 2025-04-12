from ..models import Representative
from bs4 import BeautifulSoup
from datetime import datetime
from nameparser import HumanName

import re
import requests
import us

class RepresentativesRetriever():
    def __init__(self, representative_ids=[], debug = False, debug_stagger = 25):
        self.date_format = "%b. %d, %Y"
        self.representative_ids = representative_ids
        self.house_members_list_url = "https://clerk.house.gov/Members/ViewMemberList"
        self.member_url = "https://clerk.house.gov/members/"
        self.member_pattern = r'[A-Z]\d{6}'
        self.representatives = []
        self.state_abbreviations = [state.abbr for state in us.states.STATES]
        self.debug = debug
        self.debug_stagger = debug_stagger

    def __convert_to_datetime(self, date_string):
        try:
            return datetime.strptime(date_string, self.date_format)
        except ValueError:
            return None

    def get_representatives(self):
        if self.representatives == []:
            self.__process_representatives()
        return self.representatives

    def __retrieve_from_members_list(self):
        r = requests.get(self.house_members_list_url)
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", { "class": "library-table" })
        table_rows = table.find("tbody").find_all("tr")
        for table_row in table_rows:
            columns = table_row.find_all("td")
            member = columns[0].find("a")
            representative_strings = re.findall(self.member_pattern, member["href"])
            representative_id = representative_strings[0] if len(representative_strings) == 1 else None
            if representative_id != None and representative_id not in self.representative_ids:
                self.representative_ids.append(representative_id)
    
    def __process_representatives(self):
        try:
            if self.representatives != []:
                return
            self.__retrieve_from_members_list()
            for index, representative_id in enumerate(self.representative_ids):
                url = self.member_url + representative_id
                r = requests.get(url)
                soup = BeautifulSoup(r.text, "html.parser")
                bio = soup.find("div", { "class": "about_bio" })
                img = bio.find("img")
                h1_text = bio.find("h1").text.strip()
                human_name = HumanName(h1_text.replace("[", "").replace("]", "")) if h1_text else "Unavailable"
                p_elements = bio.find_all("p")
                split_value = p_elements[0].text.strip().split("–")
                state_value = split_value[0].strip()
                split_by_parentheses = state_value.split("(")
                state_or_territory_full = split_by_parentheses[0].strip()
                state_or_territory_abbreviation = split_by_parentheses[1].replace(")", "").strip()
                office_party_value = split_value[1].strip()
                split_value = office_party_value.split(",")
                position_or_district = split_value[0].strip()
                district_number = re.findall(r'[0-9.]+', position_or_district)
                if len(district_number) > 0 and district_number[0].isnumeric():
                    position_or_district = int(district_number[0])
                party = split_value[1].strip()
                hometown_list = p_elements[1].text.strip().split(":") if p_elements[1] != None else None
                hometown = hometown_list[1].strip() if hometown_list != None and len(hometown_list) > 1 else None
                contact_table = soup.find("table", { "class": "contact-schedule-section" })
                member_div = contact_table.find("div", { "class": "member" })
                address_list = member_div.find_all("span")
                address1 = address_list[0].text.strip()
                address2 = address_list[1].text.strip()
                address3 = address_list[2].text.strip()
                phone_list = contact_table.find("span", { "class": "phone" }).text.strip().split(":")
                phone = phone_list[1]
                website = member_div.parent.find("a").href
                oath_list = p_elements[2].text.strip().split(":") if p_elements[2] != None else None
                date_last_oath_of_office = self.__convert_to_datetime(oath_list[1].strip()) if oath_list != None and len(oath_list) > 1 else None
                resigned_list = p_elements[3].text.strip().split(":") if len(p_elements) > 3 else None
                date_resigned = self.__convert_to_datetime(resigned_list[1].strip()) if resigned_list != None and len(resigned_list) > 1 else None
                is_voting_representative = True if state_or_territory_abbreviation in self.state_abbreviations else False
                representative = Representative(
                    representative_id,
                    human_name.first if human_name.first else None,
                    human_name.middle if human_name.middle else None,
                    human_name.last if human_name.last else None,
                    human_name.suffix if human_name.suffix else None,
                    state_or_territory_full,
                    state_or_territory_abbreviation,
                    position_or_district,
                    party,
                    hometown,
                    None,
                    None,
                    None,
                    None,
                    None,
                    date_last_oath_of_office,
                    date_resigned,
                    is_voting_representative
                )
                self.representatives.append(representative)
                if self.debug == True:
                    print(address1, address2, address3, phone, website)
                    place = index + 1
                    if place == 1 or place % self.debug_stagger == 0 or place == len(self.representative_ids):
                        print(f'{place} of {len(self.representative_ids)} Congressional representatives retrieved')
        except Exception as e:
            print(e)