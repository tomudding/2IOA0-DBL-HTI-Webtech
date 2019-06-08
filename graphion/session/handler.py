"""
Author(s): Tom Udding
Created: 2019-06-08
Edited: 2019-06-08
"""

"""
Graphion Session Handler
"""
from graphion import server
from itsdangerous import Signer, BadSignature, want_bytes
from os import getcwd
from os.path import join
from werkzeug.contrib.cache import FileSystemCache

class GraphionSessionHandler:
    """
    Create GraphionSessionHandler with a given SID (session identifier)
    """
    def __init__(self, sid):
        self.cache = FileSystemCache(join(getcwd(), 'flask_session'))
        self.key_prefix = "session:"
        self.identifier = Signer(server.config['SECRET_KEY'], salt='flask-session', key_derivation='hmac').unsign(sid).decode()

    """
    Helper function to get SessionCache contents.
    Returns contents or None.
    """
    def _getCacheContents(self):
        return self.cache.get(self.key_prefix + self.identifier)

    """
    Retrieve a value from the SessionCache using a given key.
    Returns contents at given key or None.
    """
    def get(self, key):
        contents = self._getCacheContents()
        if contents is not None:
            return contents.get(key, None)
        return None

    """
    Check if a key exists without returning actual data.
    Returns True if data exists at key, False if it does not.
    """
    def has(self, key):
        return key in self._getCacheContents()

    """
    Set a value in the SessionCache using a given key.
    Returns boolean or pickle.PickleError. True is value has been updated
    False if a backend error has occurred. And pickle.PickleError when
    pickling fails.
    """
    def set(self, key, value):
        contents = self._getCacheContents()
        contents.update({key: value})
        return self.cache.set(self.key_prefix + self.identifier, contents)