import webhoseio


def read_webhoseio_key():
    """
    Reads the WebHose.io API key from a file called 'search.key'.
    returns: a string which is either None, i.e. no key found, or with a key.
    Remember: put search.key in your .gitignore file to avoid committing it!
    """

    webhoseio_api_key = None

    try:
        with open('search.key', 'r') as f:
            webhoseio_api_key = f.readline()
    except IOError:
        print('file search.key not found')

    return webhoseio_api_key


def webhoseio_search(query):

    key = read_webhoseio_key()
    results = []

    webhoseio.config(token=key)
    query_params = {
        'q': query + ' language:english',
        'sort': 'relevancy'
    }
    output = webhoseio.query('filterWebContent', query_params)

    for result in output['posts']:
        results.append({
            'name': result['title'],
            'url': result['url'],
            'summary': result['published']
        })

    return results[:10]


# if __name__ == '__main__':
#     webhoseio_search('ice')
