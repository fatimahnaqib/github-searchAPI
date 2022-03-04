import requests
import unittest

class TestSearchIssuesApi(unittest.TestCase):
    def setUp(self):
        self.__api_base_url = "https://api.github.com"
        self.__header = {"Authorization": "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"}
        self.q = 'broken'
        self.search_issues = '/search/issues'
        self.filter_title = '&title=in%3Atitle'
        self.filter_body = '&body=in%3Abody'
        self.filter_comment = '&comment=in%3Acomment'
        
    def test_search_issues_by_title(self):
        response = requests.get(self.__api_base_url + self.search_issues + '?q=' + self.q +"type:issue"+'+'+self.filter_title+"&per_page=100", headers=self.__header)
        self.assertEqual(response.status_code,200)
    
    def test_search_issues_by_body(self):
        response = requests.get(self.__api_base_url + self.search_issues + '?q=' + self.q +"type:issue"+'+'+self.filter_body+"&per_page=100", headers=self.__header)
        self.assertEqual(response.status_code,200)
    
    def test_search_issues_by_comment(self):
        response = requests.get(self.__api_base_url + self.search_issues + '?q=' + self.q +"type:issue"+'+'+self.filter_comment+"&per_page=100", headers=self.__header)
        self.assertEqual(response.status_code,200)

    def test_search_issue_with_q(self):
        r = requests.get(self.__api_base_url + self.search_issues + '?q=' + self.q, headers=self.__header) 
        self.assertEqual(r.status_code, 200)