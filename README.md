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

    API: /auth/register
    Method: POST
    Request Format: { username: String, password: String, email: EmailFormat }
    Response: { success: Boolean, token: String }

    API: /validate-username
    Method: GET
    Params: username <String>
    Response: { istaken: Boolean , error: String }

**- Login:**

    API: /auth/api-token-auth/
    Method: POST
    Request Format:{ username: String, password: String }
    Response: { token: String }

**- Registering google users:**

    API: /auth/google/login
    Method: POST
    Sign Up:
    Request Format:{ username: String, token: hash }
    Response: { success: Boolean, token: String }
    Sign in:
    Request Format:{ token: hash }
    Response: { token: String }

**- Logout:**

    API: /auth/logout
    Method: GET
    Reponse : { success: Boolean }

**- Fetching and Storing Typing Details**

    API: /userlog
    Method: POST
    Request Format: { para: Integer, wpm: Integer, taken_at: DatetimeFormat, correct_words: Integer, wrong_words: Integer, total_words: Integer, accuracy: Float }
    Response: {success: Boolean}

    API: /getuserlog/last=INT:logDataForLastNDates/
    Method: GET
    Response: { date: [ wpm: Integer, taken_at: DatetimeFormat, correct_words: Integer, wrong_words: Integer, total_words: Integer, accuracy: Float ] }

**- Creating and retriveing paragraphs:**

    API: /para
    Method: POST
    Request Format: { para: Integer, taken_from: String }
    Response: { success: Boolean}

    Method: GET
    Response: { id: Integer, para: String, taken_from: String}
