class HouseOfRepresentativesRollCallVote():
    def __init__(
        self,
        date,
        congress,
        session,
        roll_call_number,
        bill_type,
        bill_type_abbreviation,
        bill_number,
        title,
        vote_question,
        vote_type,
        vote_status
    ):
        self._date = date
        self._congress = congress
        self._session = session
        self._roll_call_number = roll_call_number
        self._bill_type = bill_type
        self._bill_type_abbreviation = bill_type_abbreviation
        self._bill_number = bill_number
        self._title = title
        self._vote_question = vote_question
        self._vote_type = vote_type
        self._vote_status = vote_status

    def __str__(self):
        return f"Roll Call Vote: {self._roll_call_number} on {self._date}"

    @staticmethod
    def get_parameter_names():
        parameters = [
            "date",
            "congress",
            "session",
            "roll_call_number",
            "bill_type",
            "bill_type_abbreviation",
            "bill_number",
            "title",
            "vote_question",
            "vote_type",
            "vote_status"
        ]
        return parameters

    def get_values_as_list(self):
        return [
            self._date,
            self._congress,
            self._session,
            self._roll_call_number,
            self._bill_type,
            self._bill_type_abbreviation,
            self._bill_number,
            self._title,
            self._vote_question,
            self._vote_type,
            self._vote_status
        ]
    
    def get_date(self):
        return self._date
        
    def get_congress(self):
        return self._congress
    
    def get_session(self):
        return self._session

    def get_roll_call_number(self):
        return self._roll_call_number

    def get_bill_type(self):
        return self._bill_type
    
    def get_bill_type_abbreviation(self):
        return self._bill_type_abbreviation
    
    def get_bill_number(self):
        return self._bill_number
    
    def get_title(self):
        return self._title
    
    def get_vote_question(self):
        return self._vote_question
    
    def get_vote_type(self):
        return self._vote_type
    
    def get_vote_status(self):
        return self._vote_status