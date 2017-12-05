import json
import urllib.request
import urllib.parse
import http.client
from sys import stdin


def read_bing_key():
    """
    Reads the BING API key from a file called 'bing.key'.
    returns: a string which is either None, i.e. no key found, or with a key.
    Remember: put bing.key in your .gitignore file to avoid committing it!
    """

    bing_api_key = None

    try:
        with open('bing.key', 'r') as f:
            bing_api_key = f.readline()
    except IOError:
        print('file bing.key not found')

    return bing_api_key


# def run_query(search_terms):
#     """
#     Given a string containing search terms (query),
#     returns a list of results from the Bing search engine.
#     """
#
#     # bing_api_key = read_bing_key()
#     if not bing_api_key:
#         raise KeyError('Bing Key Not Found')
#
#     root_url = 'https://api.cognitive.microsoft.com/bing/v7.0/search/'
#     service = ''
#
#     # Specify how many results we wish to be returned per page.
#     # Offset specifies where in the results list to start from.
#     # With results_per_page = 10 and offset = 11, this would start from page 2.
#     results_per_page = 10
#     offset = 0
#
#     query = '"{0}"'.format(search_terms)
#     search_url = '{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}'.format(
#         root_url,
#         service,
#         results_per_page,
#         offset,
#         query
#     )
#
#     username = ''
#     password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
#     password_mgr.add_password(None, search_url, username, bing_api_key)
#
#     results = []
#
#     try:
#         handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
#         opener = urllib.request.build_opener(handler)
#         urllib.request.install_opener(opener)
#
#         response = urllib.request.urlopen(search_url).read()
#         response = response.decode('utf-8')
#
#         json_response = json.loads(response)
#
#         for result in json_response['d']['results']:
#             results.append({
#                 'title': result['Title'],
#                 'link': result['Link'],
#                 'summary': result['Summary']
#             })
#     except:
#         print('Error with query')
#
#     return results


def bing_web_search(search):
    """Performs a Bing Web search and returns the results."""

    host = "api.cognitive.microsoft.com"
    path = "/bing/v7.0/search"
    results = []
    bing_api_key = read_bing_key()

    try:
        key_header = {'Ocp-Apim-Subscription-Key': bing_api_key}
        conn = http.client.HTTPSConnection(host)
        query = urllib.parse.quote(search)
        conn.request("GET", path + "?q=" + query, headers=key_header)
        response = conn.getresponse()
        resp_headers = [k + ": " + v for (k, v) in response.getheaders()
                        if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
        response = response.read().decode("utf8")
        json_response = json.loads(response)
        for res in json_response['webPages']['value']:
            results.append({
                'name': res['name'],
                'url': res['url'],
                'summary': res['snippet']
            })
    except:
        print('Error')

    return results


# if __name__ == '__main__':
#     search_query = stdin.readline()
#
#     print('Searching the Web for: ', search_query)
#
#     result = bing_web_search(search_query)
#     # print("\nRelevant HTTP Headers:\n")
#     # print("\n".join(headers))
#     print("\nJSON Response:\n")
#     print(json.dumps(result, indent=4))
