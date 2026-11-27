class User:  # User of ClubGUard so volunteer, admin, member, etc
    def __init__(self, name, club_id, role):
        self.name = name
        self.club_id = club_id
        self.role = role

# The one hard-coded demo user for the prototype as there is no login
demo_user = User("JJ", "westeros-rfc", "member")

def verify_user(): # Mocked: the demo user is always logged in
    return demo_user

def get_members(club_id):  # Would return every member of the club, needed by the alert service
    raise NotImplementedError("Club members are deferred in the prototype. That is for the target architecture.")