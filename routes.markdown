## backend routes

/login
/logout

/api/organizations
  - GET
    - returns a list of all the user's organizations
  - POST
    - creates a new organization associated with the user

/api/organizations/<id>
  - GET
    - returns the given organization
  - DELETE
    - deletes the given organization

/api/<organization_id>/members/
  - GET
    - returns a list of all the members associated with the given organization
  - POST
    - creates a new member associated with the given organization

/api/<organization_id>/members/<id>
  - GET
    - returns the given member associated with the given organization
  - DELETE
    - deletes the given member

/api/users
  - GET
    - shouldn't return anything in production, but for development purposes can return a list of users
  - POST
    - creates a new user

/api/mail
  - GET
    - shouldn't return anything
  - POST
    - sends a given email template to a given list of email addresses

## frontend routes

/
  - home route, where the user logs in and is presented with a list of their organizations

/<organization_id>
  - main page for an organization
    - option to send email
    - option to manage email lists
    - option to see a list of members

/<organization_id>/members
  - list of members
    - option to delete members
    - option to add members
    - option to inspect individual members

/<organization_id>/members/<member_id>
  - individual member information
    - option to send email to member
    - option to delete member

/<organization_id>/lists
  - list of email lists
    - option to create new lists
    - option to delete old lists

/<organization_id>/mail
  - draft an email and send it to a list of members

