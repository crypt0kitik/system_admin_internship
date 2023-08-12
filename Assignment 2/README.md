# User Account Creation Script Documentation

This documentation provides instructions on how to use the provided PowerShell script to create a new user account in Active Directory.

## Prerequisites

- Windows environment with PowerShell
- Active Directory module imported
- Proper permissions to create user accounts in Active Directory

## Running the Script

1. Open PowerShell:

   - Press `Win + X` and select "Windows PowerShell" or "Windows PowerShell (Admin)" from the menu.

2. Navigate to the directory containing the script:

    ```shell
    cd path\to\script\directory
    ```

3. Run the script with required parameters:

    ```shell
    .\CreateUserAccount.ps1 -UserName JohnDoe -EmailAddress johndoe@example.com -Department IT -JobTitle ITGuy
    ```

    Replace the values with appropriate user information.


## Important Notes

- Customize the script:
   - Replace placeholders like `yourdomain.com`, `IT Group`, and `smtp.yourdomain.com` with actual values.

- Logs:
   - The script logs actions to a centralized log file (`UserAccountCreationLog.txt`).
