# Parameters
param (
    [string]$UserName,
    [string]$EmailAddress,
    [string]$Department,
    [string]$JobTitle
)

# Validate input parameters
if (-not $UserName -or -not $EmailAddress -or -not $Department -or -not $JobTitle) {
    Write-Host "Error: All parameters are required." -ForegroundColor Red
    Exit
}

# Check if the user account already exists
$existingUser = Get-ADUser -Filter { SamAccountName -eq $UserName } -ErrorAction SilentlyContinue
if ($existingUser) {
    Write-Host "Error: User account already exists." -ForegroundColor Red
    Exit
}

# Generate a random password
$Password = [System.Web.Security.Membership]::GeneratePassword(12, 3)

# Create the user account in Active Directory
New-ADUser -Name $UserName -SamAccountName $UserName -UserPrincipalName "$UserName@yourdomain.com" -EmailAddress $EmailAddress -Department $Department -Title $JobTitle -AccountPassword (ConvertTo-SecureString $Password -AsPlainText -Force) -Enabled $true

# Add user to appropriate groups based on department and job title
if ($Department -eq "IT") {
    Add-ADGroupMember -Identity "IT Group" -Members $UserName
}

# Send email with the generated password
$EmailSubject = "Your New User Account Details"
$EmailBody = "Hello $UserName," + "`r`n`r`n" +
    "Your new user account has been created with the following details:" + "`r`n" +
    "Username: $UserName" + "`r`n" +
    "Password: $Password" + "`r`n" +
    "Please change your password upon first login." + "`r`n`r`n" +
    "Regards," + "`r`n" +
    "Your IT Team"
Send-MailMessage -To $EmailAddress -Subject $EmailSubject -Body $EmailBody -SmtpServer "smtp.yourdomain.com"

# Log actions to a centralized log file
$LogMessage = "$(Get-Date) - User account created for $UserName with email $EmailAddress in department $Department."
$LogFilePath = "C:\Scripts\UserAccountCreationLog.txt"
$LogMessage | Out-File -Append -FilePath $LogFilePath

Write-Host "User account has been created successfully. Details have been emailed to $EmailAddress." -ForegroundColor Green
