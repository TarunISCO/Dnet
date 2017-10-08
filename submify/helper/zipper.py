import shutil


def zipper(submission_id, arg, dir_name):
    """Helper function for zipping file in a upload directory
    :param submission_id : ID of the submission
    :param arg : File type argument
    :param dir_name : directory name where files are present
    """
    try:
        if arg == 'zip':
            shutil.make_archive(submission_id, arg, dir_name)
        elif arg == 'tar':
            shutil.make_archive(submission_id, arg, dir_name)
        else:
            shutil.make_archive(submission_id, 'zip', dir_name)
        return True
    except Exception:
        print 'Exception occured while zipping file'
        return False
