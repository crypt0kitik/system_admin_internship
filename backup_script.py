import os
import shutil
from datetime import datetime
import logging
import configparser

# read the configuration file
def read_config():
    config = configparser.ConfigParser()
    config.read('backup_config.conf')
    backup_dirs = config.get('BACKUP', 'Directories').split(',')
    backup_location = config.get('BACKUP', 'Location')
    max_backups = int(config.get('BACKUP', 'MaxBackups'))
    return backup_dirs, backup_location, max_backups

# create backup directory
def create_backup_directory(backup_location):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_directory = os.path.join(backup_location, f"backup_{timestamp}")
    os.makedirs(backup_directory)
    return backup_directory

# perform the backup
def perform_backup(backup_dirs, backup_directory):
    for directory in backup_dirs:
        shutil.copytree(directory, os.path.join(backup_directory, os.path.basename(directory)))

# manage
def manage_backups(backup_location, max_backups):
    backups = os.listdir(backup_location)
    backups = [backup for backup in backups if os.path.isdir(os.path.join(backup_location, backup))]
    backups.sort(reverse=True)

    if len(backups) >= max_backups:
        for directory in backups[max_backups:]:
            directory_path = os.path.join(backup_location, directory)
            try:
                shutil.rmtree(directory_path)
            except NotADirectoryError:
                os.remove(directory_path)

def backup_files(backup_dirs, backup_location):
    backup_directory = create_backup_directory(backup_location)

    for directory in backup_dirs:
        try:
            shutil.copytree(directory, os.path.join(backup_directory, os.path.basename(directory)))
        except Exception as e:
            print(f"An error occurred during the backup process: {e}")

# configure logging
def configure_logging():
    logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# main function
def main():
    # Read configuration
    backup_dirs, backup_location, max_backups = read_config()

    # Create backup directory
    backup_directory = create_backup_directory(backup_location)

    # Perform backup
    try:
        perform_backup(backup_dirs, backup_directory)
        logging.info('Backup process completed successfully.')
    except Exception as e:
        logging.error(f'An error occurred during the backup process: {str(e)}')

    # Manage backups
    manage_backups(backup_location, max_backups)

if __name__ == '__main__':
    configure_logging()
    main()