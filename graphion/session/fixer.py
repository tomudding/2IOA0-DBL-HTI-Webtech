"""
Author(s): Tom Udding
Created: 2019-06-08
Edited: 2019-06-08
"""

"""
Graphion Session Handler
"""
class GraphionSessionHandler():
    """
    Create GraphionSessionHandler with a given SID (session identifier)
    """
    def __init__(self, sid):
        from werkzeug.contrib.cache import FileSystemCache
        from os import getcwd
        from os.path import join

        self.cache = FileSystemCache(join(getcwd(), 'flask_session'))
        self.key_prefix = "session:"
        self.sid = sid

    """
    Retrieve a value from the SessionCache using a given key.
    Returns contents at given key or None.
    """
    def get(key):
        return self.cache.get(self.key_prefix + self.sid + key)

    """
    Set a value in the SessionCache using a given key.
    Returns boolean or pickle.PickleError. True is value has been updated
    False if a backend error has occurred. And pickle.PickleError when
    pickling fails.
    """
    def set(key, value):
        return self.cache.set(self.key_prefix + self.sid + key, value, calculateLifetime(app.permanent_session_lifetime))

    """
    Calculate the lifetime of a SessionCache in seconds
    """
    def calculateLifetime(td):
        return td.days * 60 * 60 * 24 + td.seconds