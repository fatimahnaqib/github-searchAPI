from django.shortcuts import render
from .helper import parse_response,handle_pagination,check_limit,save_to_model,get_exception, get_single_filtered_response,get_response_by_two_filter,get_response_by_three_filter,get_no_filtered_response
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
        if request.GET.get('title'):
            filtered_response = get_single_filtered_response(request.GET['title'],search_term,headers)
            filterBy = filtered_response['filterBy']
            response = filtered_response['response']
        
        if request.GET.get('body'):
            filtered_response = get_single_filtered_response(request.GET['body'],search_term,headers)
            filterBy = filtered_response['filterBy']
            response = filtered_response['response']
        
        if request.GET.get('comment'):
            filtered_response = get_single_filtered_response(request.GET['comment'],search_term,headers)
            filterBy = filtered_response['filterBy']
            response = filtered_response['response']
        
        if request.GET.get('title') and request.GET.get('body'):
            filtered_response = get_response_by_two_filter(request.GET['title'],request.GET['body'],search_term,headers)
            filterBy = filtered_response['filterBy']
            response = filtered_response['response']
        
        if request.GET.get('title') and request.GET.get('comment'):
            filtered_response = get_response_by_two_filter(request.GET['title'],request.GET['comment'],search_term,headers)
            filterBy = filtered_response['filterBy']
            response = filtered_response['response']
        
        if request.GET.get('body') and request.GET.get('comment'):
            filtered_response = get_response_by_two_filter(request.GET['body'],request.GET['comment'],search_term,headers)
            filterBy = filtered_response['filterBy']
            response = filtered_response['response']
        
        if request.GET.get('title') and request.GET.get('body') and request.GET.get('comment'):
            filtered_response = get_response_by_three_filter(request.GET['title'],request.GET['body'],request.GET['comment'],search_term,headers)
            filterBy = filtered_response['filterBy']
            response = filtered_response['response']
                
        if not request.GET.get('title') and not request.GET.get('body') and not request.GET.get('comment'):
            response = get_no_filtered_response(search_term,headers)

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
