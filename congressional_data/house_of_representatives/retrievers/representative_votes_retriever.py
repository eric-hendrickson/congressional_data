from ..models import HouseOfRepresentativesRollCallVote, RepresentativeVote
from bs4 import BeautifulSoup

import re
import requests

class RepresentativeVotesRetriever:
    def __init__(self, debug = False, debug_stagger = 5):
        self.base_url = "https://clerk.house.gov/Votes/"
        self.member_pattern = r'[A-Z]\d{6}'
        self.representative_votes_list = []
        self.debug = debug
        self.debug_stagger = debug_stagger

    def clear(self):
        self.representative_votes_list = []

    def get_representative_votes(self, total_votes):
        if self.representative_votes_list == []:
            self.__process_votes(total_votes)
        return self.representative_votes_list

    def __process_speaker_row(self, soup, congress, session, roll_call_number):
        speaker_votes_list = []
        container = soup.find("div", { "class": "all-votes" })
        speaker = container.find_all("h2")[1].text.strip()
        table_rows = container.find("tbody").find_all("tr")
        for table_row in table_rows:
            found_h2 = table_row.find("h2")
            if found_h2 != None:
                speaker = found_h2.text.strip()
            else:
                member = table_row.find("a")
                representative_strings = re.findall(self.member_pattern, member["href"])
                representative_id = representative_strings[0] if len(representative_strings) == 1 else None
                representative_name = member.text.strip()
                party = table_row.find_all("td")[2].text.strip()
                state_name = table_row.find_all("td")[3].text.strip()
                state_abbreviation = table_row.find_all("td")[4].text.strip()
                representative_vote = RepresentativeVote(
                    representative_id,
                    congress,
                    session,
                    roll_call_number,
                    speaker
                )
                speaker_votes_list.append(representative_vote)
        return speaker_votes_list

    def __process_regular_row(self, soup, congress, session, roll_call_number):
        votes_list = []
        table = soup.find("table", { "class": "allvotes-table" })
        if table != None:
            table_rows = table.find("tbody").find_all("tr")
            for table_row in table_rows:
                if table_row.text.strip() != "No data found":
                    member = table_row.find("a")
                    representative_strings = re.findall(self.member_pattern, member["href"])
                    representative_id = representative_strings[0] if len(representative_strings) == 1 else None
                    vote = table_row.find("td", { "data-label": "vote" }).text.strip()
                    representative_vote = RepresentativeVote(
                        representative_id,
                        congress,
                        session,
                        roll_call_number,
                        vote
                    )
                    votes_list.append(representative_vote)
        return votes_list
    
    def __process_votes(self, total_votes):
        try:
            representative_votes_list = []
            for index, vote in enumerate(total_votes):
                date = vote.get_date()
                r = requests.get(
                    "{}{}{}".format(self.base_url, date.year, vote.get_roll_call_number())
                )
                soup = BeautifulSoup(r.text, "html.parser")
                if vote.get_vote_question() == "Election of the Speaker":
                    speaker_votes_list = self.__process_speaker_row(
                        soup, vote.get_congress(), vote.get_session(), vote.get_roll_call_number()
                    )
                    representative_votes_list.extend(speaker_votes_list)
                else:
                    regular_votes_list = self.__process_regular_row(
                        soup, vote.get_congress(), vote.get_session(), vote.get_roll_call_number()
                    )
                    representative_votes_list.extend(regular_votes_list)
                if self.debug == True:
                    place = index + 1
                    if place == 1 or place % self.debug_stagger == 0 or place == len(total_votes):
                        print(f'Representative votes for {index + 1} of {len(total_votes)} roll call votes retrieved')
            self.representative_votes_list = representative_votes_list
        except Exception as e:
            print(e)