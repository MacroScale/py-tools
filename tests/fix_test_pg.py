import datetime
from shared_utils.db import PGDB

def test_basic_statement():
    db = PGDB();
    result = db.execute("select * from \"beam-demo\".users")
    expected = [(1, 'steve', 'jobs', datetime.datetime(1989, 5, 2, 0, 0))]
    assert result == expected
