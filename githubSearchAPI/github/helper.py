import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from .models import Issue

def parse_response(response,issues_list):
    
    resp_json = response.json()
    issues=resp_json['items']
    issues_list.extend(issues)

    return issues_list

def handle_pagination(issues,request,result_no):
    paginator = Paginator(issues, result_no) 
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        issues = paginator.page(page)
    except PageNotAnInteger:
        issues = paginator.page(1)
    except EmptyPage:
        issues = paginator.page(paginator.num_pages)
   
    return issues

def get_no_filtered_response(search_term,headers):
    return requests.request('GET', 'https://api.github.com/search/issues?q='+search_term+"type:issue"+"&per_page=100", headers=headers)

def get_single_filtered_response(filteredOption,search_term,headers):
    filtered_response = {}

    if filteredOption == 'in:title':
        response = requests.get('https://api.github.com/search/issues?q='+search_term+"type:issue"+'+'+filteredOption+"&per_page=100", headers=headers)
        filterBy = "&title=in%3Atitle"
        filtered_response.update({'response':response,'filterBy':filterBy})
    
    if filteredOption == 'in:body':
        response = requests.request('GET', 'https://api.github.com/search/issues?q='+search_term+"type:issue"+'+'+filteredOption+"&per_page=100", headers=headers)
        filterBy = "&body=in%3Abody"
        filtered_response.update({'response':response,'filterBy':filterBy})
    
    if filteredOption == 'in:comment':
        response = requests.request('GET', 'https://api.github.com/search/issues?q='+search_term+"type:issue"+'+'+filteredOption+"&per_page=100", headers=headers)
        filterBy = "&comment=in%3Acomment"
        filtered_response.update({'response':response,'filterBy':filterBy})
    
    return filtered_response

def get_response_by_two_filter(filterOption1,filterOption2,search_term,headers):
    filtered_response = {}

    if filterOption1 == 'in:title' and filterOption2 == 'in:body':
        response = requests.request('GET', 'https://api.github.com/search/issues?q='+search_term+"type:issue"+'+'+filterOption1+'+'+filterOption2+"&per_page=100", headers=headers)
        filterBy = "&title=in%3Atitle&body=in%3Abody"
        filtered_response.update({'response':response,'filterBy':filterBy})
    
    if filterOption1 == 'in:title' and filterOption2 == 'in:comment':
        response = requests.request('GET', 'https://api.github.com/search/issues?q='+search_term+"type:issue"+'+'+filterOption1+'+'+filterOption2+"&per_page=100", headers=headers)
        filterBy = "&title=in%3Atitle&comment=in%3Acomment"
        filtered_response.update({'response':response,'filterBy':filterBy})
    
    if filterOption1 == 'in:body' and filterOption2 == 'in:comment':
        response = requests.request('GET', 'https://api.github.com/search/issues?q='+search_term+"type:issue"+'+'+filterOption1+'+'+filterOption2+"&per_page=100", headers=headers)
        filterBy = "&body=in%3Abody&comment=in%3Acomment"
        filtered_response.update({'response':response,'filterBy':filterBy})
    
    return filtered_response

def get_response_by_three_filter(filterOption1,filterOption2,filterOption3,search_term,headers):
    filtered_response = {}

    if filterOption1 == 'in:title' and filterOption2 == 'in:body' and filterOption3 == 'in:comment':
        response = requests.request('GET', 'https://api.github.com/search/issues?q='+search_term+"type:issue"+'+'+filterOption1+'+'+filterOption2+filterOption3+"&per_page=100", headers=headers)
        filterBy = "&title=in%3Atitle&body=in%3Abody"
        filtered_response.update({'response':response,'filterBy':filterBy})
    
    return filtered_response

def check_limit(response):
    remaining_requests = int(response.headers['X-RateLimit-Remaining'])

    if remaining_requests == 0:
        time.sleep(60)

def save_to_model(issues):
    for issue in issues:
        if (not Issue.objects.filter(issue_id=issue['id']).exists()):
            query=Issue(issue_id=issue['id'],avatar_url=issue['user']['avatar_url'],title= issue['title'],html_url=issue['html_url'],descrip=issue['body'],score=issue['score'])
            query.save()
        else:
            query=Issue.objects.get(issue_id=issue['id'])
            query.avatar_url=issue['user']['avatar_url']
            query.html_url=issue['html_url']
            query.descrip=issue['body']
            query.score=issue['score']
            query.score=issue['title']
            query.save()

def get_exception(response):
    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
