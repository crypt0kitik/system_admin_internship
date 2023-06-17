import os
import shutil
import datetime
import logging
import configparser

# Read the configuration file
def read_config():
    config = configparser.ConfigParser()
    config.read('backup_config.conf')
    backup_dirs = config.get('BACKUP', 'Directories').split(',')
    backup_location = config.get('BACKUP', 'Location')
    max_backups = int(config.get('BACKUP', 'MaxBackups'))
    return backup_dirs, backup_location, max_backups

# Create backup directory with timestamp
def create_backup_directory(backup_location):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    backup_directory = os.path.join(backup_location, f'backup_{timestamp}')
    os.makedirs(backup_directory)
    return backup_directory

# Perform the backup
def perform_backup(backup_dirs, backup_directory):
    for dir in backup_dirs:
        shutil.copytree(dir, os.path.join(backup_directory, os.path.basename(dir)))

# Manage the number of backups
def manage_backups(backup_location, max_backups):
    backup_directories = sorted(os.listdir(backup_location), reverse=True)
    if len(backup_directories) > max_backups:
        for directory in backup_directories[max_backups:]:
            shutil.rmtree(os.path.join(backup_location, directory))

# Configure logging
def configure_logging():
    logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Main function
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
