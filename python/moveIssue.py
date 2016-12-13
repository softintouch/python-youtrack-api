import sys
from youtrack import Issue
from youtrack.connection import Connection

PREDEFINED_FIELDS = ["summary", "description", "created", "updated", "updaterName", "resolved", "reporterName",
                     "assigneeName", "priority", "state"]

def main():
    try:
        source_url, source_login, source_password, target_url, target_login, target_password = sys.argv[1:7]
        source_id, target_project = sys.argv[7:]
    except:
        print "Usage: moveIssue source_url source_login source_password target_url target_login target_password source_id target_project"
        return
    doMove(source_url, source_login, source_password, target_url, target_login, target_password, source_id, target_project)

def check_user(user_login, source, target) :
    if (user_login == "guest") or (user_login is None):
        return
    try :
        target.getUser(user_login)
    except :
        source_user = source.getUser(user_login)
        if not("email" in source_user) :
            source_user.email = "no_email"
        print target.importUsers([source_user])
        print "User %s was created" % user_login
        return user_login

def get_new_issue_id(project_id, target) :
    max_id = 1
    max_number = 100
    while (True) :
        issues = target.getIssues(project_id, "", max_id, max_number)
        if (len(issues) == 0) :
            return max_id
        for issue in issues :
            issue_id = int(issue.numberInProject)
            if (issue_id >= max_id) :
                max_id = issue_id + 1


def doMove(source_url, source_login, source_password, target_url, target_login, target_password, source_issue_id, target_project_id) :
    print "source_url       : " + source_url
    print "source_login     : " + source_login
    print "source_password  : " + source_password
    print "target_url       : " + target_url
    print "target_login     : " + target_login
    print "target_password  : " + target_password
    print "source_id        : " + source_issue_id
    print "target_project   : " + target_project_id

    # connecting
    try :
        target = Connection(target_url, target_login, target_password)
        print "Connected to target url [%s]" % target_url
    except Exception, ex:
        print "Failed to connect to target url [%s] with login/password [%s/%s]" % (target_url, target_login, target_password)
        raise ex

    try :
        source = Connection(source_url, source_login, source_password)
        print "Connected to source url [%s]" % source_url
    except Exception, ex :
        print "Failed to connect to source url [%s] with login/password [%s/%s]" % (source_url, source_login, source_password)
        raise ex

    try :
        target.getProject(target_project_id)
    except Exception, ex:
        print "Can't connect to target project [%s]" % target_project_id
        raise ex

    #twin issues
    try :
        source_issue = source.getIssue(source_issue_id)
    except Exception, ex :
        print "Failed to get issue [%s]" % source_issue_id
        raise ex

    target_issue = Issue()

    #import users if needed
    name_fields = ["reporeterName", "assigneeName", "updaterName"]
    for field in name_fields :
        if (field in source_issue) :
            check_user(source_issue[field], source, target)

    target_issue.numberInProject = str(get_new_issue_id(target_project_id, target))

    #check subsystem
    target_subsystem = None
    try :
        target.getSubsystem(target_project_id, source_issue.subsystem)
        target_subsystem = source_issue.subsystem
    except :
        pass
    target_issue.subsystem = target_subsystem
    for field in PREDEFINED_FIELDS :
        if (field in source_issue) :
            target_issue[field] = source_issue[field]

    if ("Type" in source_issue) :
        target_issue.type = source_issue["Type"]
    elif ("type" in source_issue) :
        target_issue.type = source_issue["type"]
    else :
        target_issue.type = "Bug"

    #convert custom field
    target_cfs = target.getProjectCustomFields(target_project_id)
    for cf in target_cfs :
        cf_name = cf.name
        if (cf_name in source_issue) :
            target_issue[cf_name] = source_issue[cf_name]

    # comments
    target_issue.comments = source_issue.getComments()
    for comment in target_issue.comments :
        check_user(comment.author, source, target)

    # attachments
    print target.importIssues(target_project_id, target.getProjectAssigneeGroups(target_project_id)[0].name, [target_issue])
    for attachment in source_issue.getAttachments() :
        check_user(attachment.author_login, source, target)
        #attachment.authorLogin = target_login
        print target.createAttachmentFromAttachment("%s-%s" % (target_project_id, target_issue.numberInProject), attachment)

if __name__ == "__main__":
    main()
  