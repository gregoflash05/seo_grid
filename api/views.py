from django.shortcuts import render
from serpapi import GoogleSearchResults
# Create your views here.


#class KeywordSearch(views.APIView):
@api_view(['GET'])
def search (request):
    """
        This endpoint (...v1/check_keyword) gives a ranking of the keyword given 
        and suggest other words with higher ranking, the only required output
        is the keyword in question.
    """

    word_search = request.data ["word_search"]

    params = {
        "engine": "google",
        "q": word_search,
        "api_key": os.getenv(API_KEY)
    }

    client = GoogleSearchResults(params)
    results = client.get_dict()
        






