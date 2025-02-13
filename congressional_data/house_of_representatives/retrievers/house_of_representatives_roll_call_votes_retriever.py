from ..models import HouseOfRepresentativesRollCallVote
from bs4 import BeautifulSoup
from datetime import datetime

import re
import requests

class HouseOfRepresentativesRollCallVotesRetriever:
    def __init__(self, debug = False, debug_stagger = 5):
        self.base_url = "https://clerk.house.gov/Votes/MemberVotes"
        self.date_format = "%b %d, %Y, %I:%M %p"
        self.debug = debug
        self.debug_stagger = debug_stagger

    def get_votes_as_lists(self):
        votes_list = self.get_votes()
        return [vote.get_values_as_list() for vote in votes_list]

    def get_votes(self):
        try:
            r = requests.get(self.base_url)
            soup = BeautifulSoup(r.text, "html.parser")
            total_number_of_votes = int(soup.find("div", { "class": "pagination_info" }).text.split(" ")[4])
            session = soup.find("div", { "class": "first-row row-comment" }).text.split("|")[1].strip()
            session_split = session.split(",")
            congress = int(re.findall(r"[0-9.]+", session_split[0].strip())[0])
            session = int(re.findall(r"[0-9.]+", session_split[1].strip())[0])
            soup_votes = soup.find_all("div", { "class": "role-call-vote" })
            all_votes = self.__get_rest_of_votes(soup_votes, total_number_of_votes)
            votes_list = self.__process_votes(all_votes, congress, session)
            return votes_list
        except Exception as e:
            print(e)

    def __get_rest_of_votes(self, votes, total):
        if len(votes) >= total:
            return votes
        else:
            count = 2
            while True:
                url = "{}?page={}".format(self.base_url, count)
                r = requests.get(url)
                soup = BeautifulSoup(r.text, "html.parser")
                page_votes = soup.find_all("div", { "class": "role-call-vote" })
                votes.extend(page_votes)
                count += 1
                if len(votes) == total:
                    return votes

    def __no_bill_number(self, heading_split):
        return len(heading_split) == 1 or heading_split[1].strip() == "QUORUM"

    def __get_bill_type(self, abbreviation):
        match abbreviation:
            case "HR" :
                return "House of Representatives"
            case "HRES":
                return "House Resolution"
            case "S":
                return "Senate"
            case _:
                return None
    
    def __process_votes(self, votes, congress, session):
        votes_list = []
        for index, vote in enumerate(votes):     
            date_string = vote.find("div", { "class": "first-row row-comment" }).text.split("|")[0].strip()
            date = datetime.strptime(date_string, self.date_format)
            heading = vote.find("div", { "class": "heading" })
            bill_type = None
            bill_type_abbreviation = None
            bill_number = None
            bill_urls = heading.find_all("a")
            if len(bill_urls) == 2:
                split_url = bill_urls[-1]["href"].split("/")
                bill_type_abbreviation = split_url[-2].strip()
                bill_type = self.__get_bill_type(bill_type_abbreviation)
                bill_number = split_url[-1].strip()
            heading_split = heading.text.strip().split("|")
            roll_call_number = int(heading_split[0].split(":")[1].strip())
            description_element = vote.find("span", { "class": "billdesc" })
            description = None if description_element == None else description_element.text.strip()
            vote_question = vote.find("label", string=re.compile("Vote Question:")).parent.contents[1].strip()
            vote_type = vote.find("label", string=re.compile("Vote Type:")).parent.contents[1].strip()
            vote_status = vote.find("label", string=re.compile("Status:")).parent.contents[1].strip()
            roll_call_vote = HouseOfRepresentativesRollCallVote(
                date,
                congress,
                session,
                roll_call_number,
                bill_type,
                bill_type_abbreviation,
                bill_number,
                description,
                vote_question,
                vote_type,
                vote_status
            )
            votes_list.append(roll_call_vote)
            if self.debug == True:
                place = index + 1
                if place == 1 or place % self.debug_stagger == 0 or place == len(votes):
                    print(f'{index + 1} of {len(votes)} House of Representatives roll call votes retrieved')
        return votes_list