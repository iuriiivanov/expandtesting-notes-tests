# Notes API — Test Specification

## 1. Epics

| ID     | Epic                                        | Description                                                            |
| ------ | ------------------------------------------- | ---------------------------------------------------------------------- |
| EP-001 | **Authentication & User Management**        | Registration, login, profile, password reset/change, account deletion  |
| EP-002 | **Notes CRUD Operations**                   | Create, read, update, delete notes                                     |
| EP-003 | **Note Status Management**                  | Update `completed` flag (done / not done)                              |
| EP-004 | **Validation & Error Handling**             | Input validation, invalid request handling, error codes                |
| EP-005 | **API Security**                            | Token-based auth, access to other users' resources, endpoint protection  |
| EP-006 | **Health Check & Service Availability**     | Verify API is operational and responsive                               |

## 2. User Stories

### EP-001: Authentication & User Management

#### US-001.1
> **As a** new user  
**I want to** register an account with my name, email, and password  
**So that I can** access the Notes API and manage my personal notes

#### US-001.2
> **As a** registered user  
**I want to** log in with my email and password  
**So that I can** receive an authentication token and access protected endpoints

#### US-001.3
> **As a** logged-in user  
**I want to** view and update my profile information  
**So that I can** keep my personal data current

#### US-001.4
> **As a** logged-in user  
**I want to** change my password securely  
**So that I can** maintain account security

#### US-001.5
> **As a** user who forgot their password  
**I want to** request a password reset link via email  
**So that I can** regain access to my account

#### US-001.6
> **As a** logged-in user  
**I want to** log out and invalidate my token  
**So that I can** securely end my session

#### US-001.7
> **As a** logged-in user  
**I want to** delete my account permanently  
**So that I can** remove all my data from the system

### EP-002: Notes CRUD Operations

#### US-002.1
> **As a** logged-in user  
**I want to** create a new note with title, description, and category  
**So that I can** organize my tasks and ideas

#### US-002.2
> **As a** logged-in user  
**I want to** retrieve a list of all my notes  
**So that I can** review my tasks and their current status

#### US-002.3
> **As a** logged-in user  
**I want to** retrieve a specific note by its ID  
**So that I can** view its full details

#### US-002.4
> **As a** logged-in user  
**I want to** update an existing note's title, description, category, and completion status  
**So that I can** keep my notes accurate and up-to-date

#### US-002.5
> **As a** logged-in user  
**I want to** delete a note by its ID  
**So that I can** remove tasks that are no longer relevant

### EP-003: Note Status Management

#### US-003.1
> **As a** logged-in user  
**I want to** mark a note as completed or not completed  
**So that I can** track my progress on tasks

### EP-004: Validation & Error Handling

#### US-004.1
> **As an** API consumer  
**I want to** receive clear error messages with appropriate HTTP status codes when I send invalid data  
**So that I can** understand and fix my requests

#### US-004.2
> **As an** API consumer  
**I want to** be informed when a requested resource does not exist  
**So that I can** handle missing data gracefully in my application

### EP-005: API Security

#### US-005.1
> **As an** API consumer  
**I want to** be denied access to protected endpoints without a valid token  
**So that I can** ensure that only authenticated users access private data

#### US-005.2
> **As a** logged-in user  
**I want to** be unable to access or modify other users' notes  
**So that I can** trust that my data remains private

### EP-006: Health Check & Service Availability

#### US-006.1
> **As a** system administrator  
**I want to** check the health status of the API service  
**So that I can** verify the system is operational and responsive

## 3. Test Cases

### EP-001: Authentication & User Management

#### US-001.1: User Registration
| ID         | Name                                           | Preconditions                                    | Steps                                                                | Expected Result                                                              | Priority |
| ---------- | ---------------------------------------------- | ------------------------------------------------ | -------------------------------------------------------------------- | ---------------------------------------------------------------------------- | -------- |
| TC-001.1.1 | Successful registration of a new user            | API is available                                 | 1. Send POST /users/register with valid name, email, password        | Status 201, success=true, id, name, email are returned                       | High     |
| TC-001.1.2 | Registration with an already existing email    | A user with this email is already registered   | 1. Send POST /users/register with an existing email                  | Status 409, message: "An account already exists with the same email address" | High     |
| TC-001.1.3 | Registration with an empty name                | —                                                | 1. Send POST /users/register with name=""                            | Status 400, validation error                                               | Medium   |
| TC-001.1.4 | Registration with an invalid email               | —                                                | 1. Send POST /users/register with email="invalid-email"              | Status 400, email validation error                                           | Medium   |
| TC-001.1.5 | Registration with a short password             | —                                                | 1. Send POST /users/register with password="123"                     | Status 400, password validation error                                        | Medium   |
| TC-001.1.6 | Registration without required fields           | —                                                | 1. Send POST /users/register without the password field              | Status 400, error "Bad Request"                                              | High     |

#### US-001.2: User Login
| ID         | Name                                           | Preconditions                  | Steps                                                       | Expected Result                               | Priority |
| ---------- | ---------------------------------------------- | ------------------------------ | ----------------------------------------------------------- | --------------------------------------------- | -------- |
| TC-001.2.1 | Successful login with valid credentials        | User is registered             | 1. Send POST /users/login with valid email and password     | Status 200, success=true, token is returned     | High     |
| TC-001.2.2 | Login with an incorrect password               | User is registered             | 1. Send POST /users/login with an incorrect password        | Status 401, message "Unauthorized Request"  | High     |
| TC-001.2.3 | Login with a non-existent email                | —                              | 1. Send POST /users/login with a non-existent email         | Status 401, message "Unauthorized Request"  | High     |
| TC-001.2.4 | Login with empty fields                        | —                              | 1. Send POST /users/login with email="" and password=""     | Status 400, validation error                  | Medium   |

#### US-001.3: User Profile
| ID         | Name                                           | Preconditions                        | Steps                                                           | Expected Result                                                    | Priority |
| ---------- | ---------------------------------------------- | ------------------------------------ | --------------------------------------------------------------- | ------------------------------------------------------------------ | -------- |
| TC-001.3.1 | Retrieve profile of an authenticated user      | User is logged in, token is present    | 1. Send GET /users/profile with x-auth-token header             | Status 200, success=true, id, name, email, phone, company returned | High     |
| TC-001.3.2 | Retrieve profile without a token               | —                                    | 1. Send GET /users/profile without x-auth-token header          | Status 401, message "Unauthorized Request"                       | High     |
| TC-001.3.3 | Update profile with valid data                 | User is logged in                    | 1. Send PATCH /users/profile with new name, phone, company      | Status 200, success=true, data is updated                          | High     |
| TC-001.3.4 | Update profile with an empty name              | User is logged in                    | 1. Send PATCH /users/profile with name=""                       | Status 400, validation error                                         | Medium   |

#### US-001.6: User Logout
| ID         | Name                                           | Preconditions            | Steps                                                      | Expected Result                                | Priority |
| ---------- | ---------------------------------------------- | ------------------------ | ---------------------------------------------------------- | ---------------------------------------------- | -------- |
| TC-001.6.1 | Successful logout                              | User is logged in        | 1. Send DELETE /users/logout with a valid x-auth-token     | Status 200, success=true, token is invalidated | High     |
| TC-001.6.2 | Logout with an invalid token                   | —                        | 1. Send DELETE /users/logout with an invalid token         | Status 401, message "Unauthorized Request"   | Medium   |

### EP-002: Notes CRUD Operations

#### US-002.1: Create Note
| ID         | Name                                           | Preconditions            | Steps                                                           | Expected Result                                                              | Priority |
| ---------- | ---------------------------------------------- | ------------------------ | --------------------------------------------------------------- | ---------------------------------------------------------------------------- | -------- |
| TC-002.1.1 | Successfully create a note with category Home  | User is logged in        | 1. Send POST /notes with title, description, category="Home"    | Status 200, success=true, note object returned with id, completed=false      | High     |
| TC-002.1.2 | Create a note with category Work               | User is logged in        | 1. Send POST /notes with category="Work"                        | Status 200, success=true, category="Work"                                    | High     |
| TC-002.1.3 | Create a note with category Personal           | User is logged in        | 1. Send POST /notes with category="Personal"                    | Status 200, success=true, category="Personal"                                | High     |
| TC-002.1.4 | Create a note without a title                  | User is logged in        | 1. Send POST /notes with title=""                               | Status 400, validation error                                                 | High     |
| TC-002.1.5 | Create a note without a description            | User is logged in        | 1. Send POST /notes with description=""                         | Status 400, validation error                                                 | High     |
| TC-002.1.6 | Create a note with an invalid category         | User is logged in        | 1. Send POST /notes with category="Invalid"                     | Status 400, validation error (enum: Home, Work, Personal)                    | High     |
| TC-002.1.7 | Create a note without a token                  | —                        | 1. Send POST /notes without x-auth-token                        | Status 401, message "Unauthorized Request"                                   | High     |
| TC-002.1.8 | Create a note with a very long title           | User is logged in        | 1. Send POST /notes with title > 1000 characters                | Check system behavior (400 or 200)                                           | Low      |

#### US-002.2: Retrieve Notes List
| ID         | Name                                           | Preconditions                          | Steps                                            | Expected Result                                                | Priority |
| ---------- | ---------------------------------------------- | -------------------------------------- | ------------------------------------------------ | -------------------------------------------------------------- | -------- |
| TC-002.2.1 | Retrieve notes list for an authenticated user  | User is logged in, notes exist         | 1. Send GET /notes with a valid x-auth-token     | Status 200, success=true, array of user's notes is returned  | High     |
| TC-002.2.2 | Retrieve notes list without a token            | —                                      | 1. Send GET /notes without x-auth-token          | Status 401, message "Unauthorized Request"                     | High     |
| TC-002.2.3 | Retrieve notes list when no notes exist        | User is logged in, no notes            | 1. Send GET /notes                               | Status 200, success=true, data=\[] (empty array)               | Medium   |

#### US-002.3: Retrieve Note by ID
| ID         | Name                                           | Preconditions                                                  | Steps                                          | Expected Result                                      | Priority |
| ---------- | ---------------------------------------------- | -------------------------------------------------------------- | ---------------------------------------------- | ---------------------------------------------------- | -------- |
| TC-002.3.1 | Retrieve an existing note by ID                | User is logged in, note exists                                 | 1. Send GET /notes/{id} with a valid id        | Status 200, success=true, note object is returned    | High     |
| TC-002.3.2 | Retrieve a non-existent note                   | User is logged in                                              | 1. Send GET /notes/{invalid_id}                | Status 400 or 404, error message                     | High     |
| TC-002.3.3 | Retrieve another user's note                 | User A is logged in, note belongs to User B                    | 1. Send GET /notes/{user_B_note_id}             | Status 400 or 401/403 (verify actual behavior)       | High     |
| TC-002.3.4 | Retrieve a note without a token                | —                                                              | 1. Send GET /notes/{id} without x-auth-token   | Status 401, message "Unauthorized Request"           | High     |

#### US-002.4: Update Note
| ID         | Name                                           | Preconditions                                | Steps                                                                                      | Expected Result                                           | Priority |
| ---------- | ---------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------- | -------- |
| TC-002.4.1 | Successfully update all note fields            | User is logged in, note exists                 | 1. Send PUT /notes/{id} with new title, description, completed=true, category="Work"     | Status 200, success=true, fields updated, updated_at changed | High     |
| TC-002.4.2 | Update a non-existent note                     | User is logged in                              | 1. Send PUT /notes/{invalid_id}                                                            | Status 400, error message                                 | High     |
| TC-002.4.3 | Update a note without a token                  | —                                              | 1. Send PUT /notes/{id} without x-auth-token                                             | Status 401, message "Unauthorized Request"                | High     |
| TC-002.4.4 | Update a note with an invalid category         | User is logged in                              | 1. Send PUT /notes/{id} with category="Invalid"                                            | Status 400, validation error                              | Medium   |
| TC-002.4.5 | Update another user's note                     | User A is logged in                            | 1. Send PUT /notes/{user_B_note_id}                                                      | Status 400 or 401/403                                     | High     |

#### US-002.5: Delete Note
| ID         | Name                                           | Preconditions                                | Steps                                             | Expected Result                                      | Priority |
| ---------- | ---------------------------------------------- | ---------------------------------------------- | ------------------------------------------------- | ---------------------------------------------------- | -------- |
| TC-002.5.1 | Successfully delete an existing note           | User is logged in, note exists                 | 1. Send DELETE /notes/{id} with a valid id        | Status 200, success=true, message "Successful Request" | High     |
| TC-002.5.2 | Delete a non-existent note                     | User is logged in                              | 1. Send DELETE /notes/{invalid_id}                | Status 400, error message                            | High     |
| TC-002.5.3 | Delete a note without a token                  | —                                              | 1. Send DELETE /notes/{id} without x-auth-token   | Status 401, message "Unauthorized Request"           | High     |
| TC-002.5.4 | Delete another user's note                     | User A is logged in                            | 1. Send DELETE /notes/{user_B_note_id}            | Status 400 or 401/403                                | High     |
| TC-002.5.5 | Re-delete an already deleted note              | Note already deleted                           | 1. Send DELETE /notes/{id} again                  | Status 400, message "Bad Request"                    | Medium   |

### EP-003: Note Status Management

#### US-003.1: Update Completed Status
| ID         | Name                                           | Preconditions                                                 | Steps                                             | Expected Result                                           | Priority |
| ---------- | ---------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------- | --------------------------------------------------------- | -------- |
| TC-003.1.1 | Set completed=true                             | User is logged in, note exists, completed=false               | 1. Send PATCH /notes/{id} with completed=true     | Status 200, success=true, completed=true, updated_at changed | High     |
| TC-003.1.2 | Set completed=false                            | User is logged in, note exists, completed=true                | 1. Send PATCH /notes/{id} with completed=false    | Status 200, success=true, completed=false                 | High     |
| TC-003.1.3 | Update status of a non-existent note           | User is logged in                                             | 1. Send PATCH /notes/{invalid_id}                 | Status 400, error message                                 | High     |
| TC-003.1.4 | Update status without a token                  | —                                                             | 1. Send PATCH /notes/{id} without x-auth-token    | Status 401, message "Unauthorized Request"              | High     |
| TC-003.1.5 | Update status of another user's note           | User A is logged in                                           | 1. Send PATCH /notes/{user_B_note_id}             | Status 400 or 401/403                                     | High     |

### EP-004: Validation & Error Handling

| ID         | Name                                           | Preconditions | Steps                                                  | Expected Result                                        | Priority |
| ---------- | ---------------------------------------------- | ------------- | ------------------------------------------------------ | ------------------------------------------------------ | -------- |
| TC-004.1.1 | Send a request with invalid JSON               | —             | 1. Send POST /notes with an invalid request body       | Status 400, message "Bad Request"                    | Medium   |
| TC-004.1.2 | Send a request with an incorrect HTTP method   | —             | 1. Send GET /notes instead of POST /notes              | Status 405 Method Not Allowed (verify)                 | Low      |
| TC-004.1.3 | Send a request to a non-existent endpoint      | —             | 1. Send GET /nonexistent                               | Status 404 Not Found                                   | Low      |
| TC-004.1.4 | Verify error response structure for 500        | —             | 1. Trigger a scenario that causes 500 (if possible)  | Status 500, success=false, message="Internal Error Server" | Medium   |

### EP-005: API Security

| ID         | Name                                           | Preconditions                                           | Steps                                                                                       | Expected Result                                           | Priority |
| ---------- | ---------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------- | -------- |
| TC-005.1.1 | Access protected endpoints with an expired token | User was logged in, token has expired                   | 1. Send GET /notes with an expired token                                                   | Status 401, message "Unauthorized Request"                | High     |
| TC-005.1.2 | Access protected endpoints with a fake token   | —                                                       | 1. Send GET /notes with token "fake-token-123"                                             | Status 401, message "Unauthorized Request"                | High     |
| TC-005.1.3 | Verify data isolation between users          | Users A and B are logged in, each has notes             | 1. User A sends GET /notes 2. Verify that User B's notes are not visible                  | Response contains only User A's notes                     | High     |
| TC-005.1.4 | SQL injection in the title field               | —                                                       | 1. Send POST /notes with title="' OR '1'='1"                                               | Status 400 or 200, but no data leakage from other users   | Medium   |

### EP-006: Health Check

| ID         | Name                                           | Preconditions | Steps                                                     | Expected Result                                               | Priority |
| ---------- | ---------------------------------------------- | ------------- | --------------------------------------------------------- | -------------------------------------------------------------- | -------- |
| TC-006.1.1 | Verify API health status                       | —             | 1. Send GET /health-check                                 | Status 200, success=true, service availability message         | High     |
| TC-006.1.2 | Verify health-check response time              | —             | 1. Send GET /health-check 2. Measure response time        | Response time < 2 seconds                                      | Medium   |
