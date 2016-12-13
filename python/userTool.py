from sync.users import UserImporter
from youtrack.connection import Connection

def _import_all_users(source, target):
    print 'Starting user importing'
    user_importer = UserImporter(source, target, caching_users=False)
    start = 0
    imported_number = 0
    users_to_import = source.getUsersTen(start)
    while len(users_to_import):
        refined_users = [source.getUser(user.login) for user in users_to_import]
        imported_number += user_importer.importUsersRecursively(refined_users)
        start += 10
        users_to_import = source.getUsersTen(start)
        if imported_number % 500 == 0: print 'Imported ' + str(imported_number) + ' users'
    print 'Finished. Total number of imported users: ' + str(imported_number)

def _delete_all_users_except_root_and_guest(target):
    print 'Starting user deleting'
    excluded = ['root', 'guest']
    deleted_number = 0
    users_to_delete = target.getUsersTen(0)
    while len(users_to_delete) > 2:
        for user in users_to_delete:
            if _check_login(user.login, excluded):
                target.deleteUser(user.login)
                deleted_number += 1
        users_to_delete = target.getUsersTen(0)
        if deleted_number % 50 == 0: print 'Deleted ' + str(deleted_number) + ' users'
    print 'Finished. Total number of deleted users: ' + str(deleted_number)

def _delete_all_groups_except_initial(target):
    print 'Starting group deleting'
    excluded = ['All Users', 'New Users', 'Reporters']
    deleted_number = 0
    groups_to_delete = target.getGroups()
    for group in groups_to_delete:
        if group.name not in excluded:
            target.deleteGroup(group.name)
            deleted_number += 1
            print 'Deleted ' + str(group.name) + ' users'
    print 'Finished. Total number of deleted groups: ' + str(deleted_number)

def _import_one_user_with_groups(source, target, login):
    print 'Starting user importing'
    user_importer = UserImporter(source, target, caching_users=False)
    users_to_import = [source.getUser(login)]
    if _check_login(login):
        user_importer.importUsersRecursively(users_to_import)
        print 'User was successfully imported'
    else:
        print 'User login ' + str(login) + ' contains prohibited chars'

def _check_login(login, excluded=None):
    if not excluded: excluded = []
    return login not in excluded and '/' not in login

def import_users(source_url, source_login, source_password, target_url, target_login, target_password):

    source = Connection(source_url, source_login, source_password)
    target = Connection(target_url, target_login, target_password)

    _import_all_users(source, target)
#    _delete_all_users_except_root_and_guest(target)
#    _delete_all_groups_except_initial(target)
#    _import_one_user_with_groups(source, target, 'batman')


def main():
    source_url = "http://localhost:8080"
    source_login = "root"
    source_password = "root"
    target_url = "http://localhost:8081"
    target_login = "root"
    target_password = "root"
    import_users(source_url, source_login, source_password, target_url, target_login, target_password)

if __name__ == "__main__":
    main()

