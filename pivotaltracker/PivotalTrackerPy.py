import json  # parsing json data
from urllib.parse import urlencode
from urllib.request import urlopen, Request
cafile = None    
try:
    import certifi
    cafile = certifi.where()
except ImportError:
    pass

class Endpoints():
    PROJECTS = "https://www.pivotaltracker.com/services/v5/projects"
    
    @staticmethod
    def PROJECT(pid):
        return "https://www.pivotaltracker.com/services/v5/projects/%s" % pid

    @staticmethod
    def PROJECT_MEMBERSHIPS(pid):
        return "https://www.pivotaltracker.com/services/v5/projects/%s/memberships" % pid

    @staticmethod
    def PROJECT_ITERATIONS(pid):
        return "https://www.pivotaltracker.com/services/v5/projects/%s/iterations" % pid

    @staticmethod
    def EPICS(pid):
        return "https://www.pivotaltracker.com/services/v5/projects/%s/epics"%pid

    @staticmethod
    def EPIC(pid, eid):
        return "https://www.pivotaltracker.com/services/v5/projects/%s/epics/%s"%(pid,eid)

    @staticmethod
    def EPIC_COMMENTS(pid,eid):
        return "https://www.pivotaltracker.com/services/v5/projects/%s/epics/%s/comments"%(pid,eid)
    
    @staticmethod
    def EPIC_COMMENTS_ATTACHMENTS(pid, eid, cid, fid):
        return "https://www.pivotaltracker.com/services/v5/projects/%s/epics/%s/comments/%s/file_attachments/%s"%(pid, eid, cid, fid)

    @staticmethod
    def STORIES(pid):
        return "https://www.pivotaltracker.com/services/v5/projects/%s/stories"%pid

    @staticmethod
    def STORY(pid, sid):
        return "https://www.pivotaltracker.com/services/v5/projects/%s/stories/%s"%(pid,sid)

    @staticmethod
    def STORY_TASKS(pid, sid):
        return "https://www.pivotaltracker.com/services/v5/projects/%s/stories/%s/tasks"%(pid,sid)

    @staticmethod
    def STORY_BLOCKERS(pid, sid):
        return "https://www.pivotaltracker.com/services/v5/projects/%s/stories/%s/blockers"%(pid,sid)

    @staticmethod
    def COMMENTS(pid, sid):
        return "https://www.pivotaltracker.com/services/v5/projects/%s/stories/%s/comments"%(pid,sid)

    @staticmethod
    def COMMENTS_ATTACHMENTS(pid, sid,cid,fid):
        return "https://www.pivotaltracker.com/services/v5/projects/%s/stories/%s/comments/%s/file_attachments/%s"%(pid,sid,cid,fid)

    @staticmethod
    def FILE_ATTACHMENTS(fid):
        return "https://www.pivotaltracker.com/file_attachments/%s/download"%(fid)

class PivotalTracker:
    headers = {
        "Authorization": "",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "python/urllib",
    }

    # default API user agent value
    user_agent = "PivotalTrackerPy"

    def decodeJSON(self, jsonString):
        return json.JSONDecoder().decode(jsonString)

    def setAPIKey(self, APIKey):
        self.headers['X-TrackerToken'] = APIKey

    def setUserAgent(self, agent):
        '''set the User-Agent setting, by default it's set to TogglPy'''
        self.user_agent = agent

    def requestRaw(self, endpoint, parameters=None):
        '''make a request to the api at a certain endpoint and return the RAW page data (usually JSON)'''
        if parameters is None:
            return urlopen(Request(endpoint, headers=self.headers), cafile=cafile).read()
        else:
            # encode all of our data for a get request & modify the URL
            endpoint = endpoint + "?" + urlencode(parameters)
            # make request and read the response
            return urlopen(Request(endpoint, headers=self.headers), cafile=cafile).read()

    def request(self, endpoint, parameters=None):
        '''make a request to the api at a certain endpoint and return the page data as a parsed JSON dict'''
        return json.loads(self.requestRaw(endpoint, parameters).decode('utf-8'))

    def getProjects(self):
        return self.request(Endpoints.PROJECTS)

    def getProject(self, pid):
        return self.request(Endpoints.PROJECT(pid))

    def getProjectIterations(self,pid,page=0):
        
        if page > 0:
            return self.request(Endpoints.PROJECT_ITERATIONS(pid), parameters={'limit': 50, 'offset': 50*int(page),'envelope': 'true'})
        else:
            return self.request(Endpoints.PROJECT_ITERATIONS(pid), parameters={'limit': 50, 'envelope': 'true'})
    
    def getProjectMemberships(self,pid):
        return self.request(Endpoints.PROJECT_MEMBERSHIPS(pid))

    def getEpics(self, pid):
        return self.request(Endpoints.EPICS(pid))

    def getEpic(self, pid, eid):
        return self.request(Endpoints.EPIC(pid, eid))

    def getEpicComments(self, pid, eid):
        return self.request(Endpoints.EPIC_COMMENTS(pid,eid), parameters={'fields': ':default,file_attachment_ids'})

    def getEpicCommentsAttachment(self, pid, eid, cid, fid):
        return self.request(Endpoints.EPIC_COMMENTS_ATTACHMENTS(pid,eid,cid,fid))

    def getStories(self, pid, page = 0):
        if page > 0:
            return self.request(Endpoints.STORIES(pid), parameters={'fields': ':default,estimate,blocked_story_ids', 'limit': 500, 'offset': 500*int(page),'envelope': 'true'})
        else:
            return self.request(Endpoints.STORIES(pid), parameters={'fields': ':default,estimate,blocked_story_ids', 'limit': 500, 'envelope': 'true'})

    def getStory(self, pid, sid):
        return self.request(Endpoints.STORY(pid, sid))

    def getStoryTasks(self, pid, sid):
        return self.request(Endpoints.STORY_TASKS(pid, sid))

    def getStoryBlockers(self, pid, sid):
        return self.request(Endpoints.STORY_BLOCKERS(pid, sid))

    def getComments(self, pid, sid):
        return self.request(Endpoints.COMMENTS(pid,sid), parameters={'fields': ':default,file_attachment_ids'})

    def getCommentsAttachment(self, pid, sid, cid, fid):
        return self.request(Endpoints.COMMENTS_ATTACHMENTS(pid,sid,cid,fid))

    # def getFileAttachment(self,fid):
    #     return self.request(Endpoints.FILE_ATTACHMENTS(fid))