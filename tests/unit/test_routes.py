def test_no_posts(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries' in rv.data
