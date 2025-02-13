class RepresentativeVote():
    def __init__(
        self,
        representative_id,
        congress,
        session,
        roll_call_number,
        vote
    ):
        self._representative_id = representative_id
        self._congress = congress
        self._session = session
        self._roll_call_number = roll_call_number
        self._vote = vote

    def __str__(self):
        return f"Representative Vote: {self._representative_id} voted on roll call vote {self._roll_call_number}"
    
    @staticmethod
    def get_parameter_names():
        parameters = [
            "representative_id",
            "congress",
            "session",
            "roll_call_number",
            "vote"
        ]
        return parameters

    def get_values_as_list(self):
        return [
            self._representative_id,
            self._congress,
            self._session,
            self._roll_call_number,
            self._vote
        ]

    def get_representative_id(self):
        return self._representative_id

    def get_congress(self):
        return self._congress

    def get_session(self):
        return self._session

    def get_vote(self):
        return self._vote