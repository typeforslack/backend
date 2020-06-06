# TypeForSlack - BACKEND

## Installation
1. Install Python and Postgres
2. Setup virutalenv if you want
3. Setup Postgres with user `sanjay`, password `typeit`, database `typeforslack` running in local.
4. Then run `pip install -r requirements.txt`
5. Then migrate if any changes `python manage.py migrate`
6. Run development server `python manage.py runserver`

## Contracts
**BASE-URL:** https://typeforslack.herokuapp.com

**ENDPOINTS:**

**- Registering new user:**

    API: /register
    Method: POST
    Request Format: { username: String, password: String, email: EmailFormat }
    Response: { success: Boolean, token: String }

**- Login:**

    API: /api-token-auth/
    Method: POST
    Request Format:{ username: String, password: String }
    Response: { token: String }

**- Logout:**

    API: /logout
    Method: GET
    Reponse : { success: Boolean }

**- Fetching and Storing Typing Details**

    API: /userlog
    Method: POST
    Request Format: {para: Integer, speed: Integer, taken_at: DatetimeFormat}
    Response: {success: Boolean}

    Method: GET
    Response: { avg: Integer, logs: [{para: String, speed: Integer, taken_at}]}

**- Creating and retriveing paragraphs:**

    API: /para
    Method: POST
    Request Format: { para: Integer, taken_from: String }
    Response: { success: Boolean}

    Method: GET
    Response: { id: Integer, para: String, taken_from: String}
