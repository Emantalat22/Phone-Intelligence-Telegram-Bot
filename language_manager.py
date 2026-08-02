user_languages = {}

def set_language(user_id, language):
    user_languages[user_id] = language


def get_language(user_id):
    return user_languages.get(user_id, "english")