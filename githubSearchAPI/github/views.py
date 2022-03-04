from django.shortcuts import render
from .helper import parse_response,handle_pagination, get_filtered_response,check_limit,save_to_model,get_exception
import requests
from .models import Issue

git_token = "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"
headers={"Authorization": git_token}

def search(request):
    issues=None
    search_term=""
    length=0
    issueslist=[]
    filterBy = ''
    if request.GET.get('search_term'):
        search_term=request.GET['search_term']

        # Get filtered Response
        filtered_response = get_filtered_response(request,search_term,headers)
        filterBy = filtered_response['filterBy']
        response = filtered_response['response']
       
        #Raise exception that is not a success
        get_exception(response)
        
        # Parse response content and extend to a list
        issueslist = parse_response(response,issueslist)

        # Traverse through page and extend already existing list with response pages content
        while 'next' in response.links.keys():
            response=requests.request('GET',response.links['next']['url'], headers=headers)
            get_exception(response)
            issueslist = parse_response(response,issueslist)

            # Wait for one minute when there is no more remaining request.
            check_limit(response)

        # Get number of issues returned
        length=len(issueslist)

        #Save to model Issues
        save_to_model(issueslist)
       
    #Handle pagination
    issueslist = handle_pagination(issueslist,request,100)

    return render(request, 'github/search.html',
        {
		    'issues':issueslist,
		    'length':length,
		    'search_term':search_term,
            'filterBy':filterBy
		})

def saved(request):
    
    issues=Issue.objects.all()
    length=len(issues)

    issues = handle_pagination(issues,request,100)
	
    return render(request, 'github/listIssues.html',
		{
		'issues':issues,
		'length':length,
		})
