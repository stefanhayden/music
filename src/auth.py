from pathlib import Path
import tidalapi

session = tidalapi.Session()

try:
    session.load_session_from_file(Path('../.authCache.txt'))
    if not session.check_login():
        raise Exception('no auth saved')
except Exception:
    session.login_oauth_simple()
    session.save_session_to_file(Path('../.authCache.txt'))
