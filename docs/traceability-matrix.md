# Traceability Matrix

**Generated automatically from:**  
- `docs/test-specification.md`  
- `backend/tests/`  

### Epic EP-001: Authentication & User Management
---
| TC ID | Test Case | Test Function | Status |
|-------|-----------|---------------|--------|
| TC-001.1.1 | Successful registration of a new user | test_auth.py::test_register_user_success | 🟢 Covered |
| TC-001.1.2 | Registration with an already existing email | test_auth.py::test_register_duplicate_email | 🟢 Covered |
| TC-001.1.3 | Registration with an empty name | test_auth.py::test_register_empty_name | 🟢 Covered |
| TC-001.1.4 | Registration with an invalid email | test_auth.py::test_register_invalid_email | 🟢 Covered |
| TC-001.1.5 | Registration with a short password | — | 🟡 Test Missing |
| TC-001.1.6 | Registration without required fields | — | 🟡 Test Missing |
| TC-001.2.1 | Successful login with valid credentials | test_auth.py::test_login_success | 🟢 Covered |
| TC-001.2.2 | Login with an incorrect password | test_auth.py::test_login_wrong_password | 🟢 Covered |
| TC-001.2.3 | Login with a non-existent email | — | 🟡 Test Missing |
| TC-001.2.4 | Login with empty fields | — | 🟡 Test Missing |
| TC-001.3.1 | Retrieve profile of an authenticated user | test_profile.py::test_get_profile_success | 🟢 Covered |
| TC-001.3.2 | Retrieve profile without a token | test_profile.py::test_get_profile_no_token | 🟢 Covered |
| TC-001.3.3 | Update profile with valid data | test_profile.py::test_update_profile_success | 🟢 Covered |
| TC-001.3.4 | Update profile with an empty name | test_profile.py::test_update_profile_empty_name | 🟢 Covered |
| TC-001.6.1 | Successful logout | test_auth.py::test_logout_success | 🟢 Covered |
| TC-001.6.2 | Logout with an invalid token | — | 🟡 Test Missing |

### Epic EP-002: Notes CRUD Operations
---
| TC ID | Test Case | Test Function | Status |
|-------|-----------|---------------|--------|
| TC-002.1.1 | Successfully create a note with category Home | test_notes_crud.py::test_create_note_home | 🟢 Covered |
| TC-002.1.2 | Create a note with category Work | test_notes_crud.py::test_create_note_work | 🟢 Covered |
| TC-002.1.3 | Create a note with category Personal | test_notes_crud.py::test_create_note_personal | 🟢 Covered |
| TC-002.1.4 | Create a note without a title | test_notes_crud.py::test_create_note_empty_title | 🟢 Covered |
| TC-002.1.5 | Create a note without a description | — | 🟡 Test Missing |
| TC-002.1.6 | Create a note with an invalid category | test_notes_crud.py::test_create_note_invalid_category | 🟢 Covered |
| TC-002.1.7 | Create a note without a token | test_notes_crud.py::test_create_note_no_token | 🟢 Covered |
| TC-002.1.8 | Create a note with a very long title | — | 🟡 Test Missing |
| TC-002.2.1 | Retrieve notes list for an authenticated user | test_notes_crud.py::test_get_all_notes | 🟢 Covered |
| TC-002.2.2 | Retrieve notes list without a token | test_notes_crud.py::test_get_all_notes_no_token | 🟢 Covered |
| TC-002.2.3 | Retrieve notes list when no notes exist | — | 🟡 Test Missing |
| TC-002.3.1 | Retrieve an existing note by ID | test_notes_crud.py::test_get_note_by_id | 🟢 Covered |
| TC-002.3.2 | Retrieve a non-existent note | test_notes_crud.py::test_get_note_not_found | 🟢 Covered |
| TC-002.3.3 | Retrieve another user's note | — | 🟡 Test Missing |
| TC-002.3.4 | Retrieve a note without a token | test_notes_crud.py::test_get_note_by_id_no_token | 🟢 Covered |
| TC-002.4.1 | Successfully update all note fields | test_notes_crud.py::test_update_note_success | 🟢 Covered |
| TC-002.4.2 | Update a non-existent note | test_notes_crud.py::test_update_note_not_found | 🟢 Covered |
| TC-002.4.3 | Update a note without a token | test_notes_crud.py::test_update_note_no_token | 🟢 Covered |
| TC-002.4.4 | Update a note with an invalid category | — | 🟡 Test Missing |
| TC-002.4.5 | Update another user's note | — | 🟡 Test Missing |
| TC-002.5.1 | Successfully delete an existing note | test_notes_crud.py::test_delete_note_success | 🟢 Covered |
| TC-002.5.2 | Delete a non-existent note | test_notes_crud.py::test_delete_note_not_found | 🟢 Covered |
| TC-002.5.3 | Delete a note without a token | test_notes_crud.py::test_delete_note_no_token | 🟢 Covered |
| TC-002.5.4 | Delete another user's note | — | 🟡 Test Missing |
| TC-002.5.5 | Re-delete an already deleted note | — | 🟡 Test Missing |

### Epic EP-003: Note Status Management
---
| TC ID | Test Case | Test Function | Status |
|-------|-----------|---------------|--------|
| TC-003.1.1 | Set completed=true | test_notes_status.py::test_mark_note_completed | 🟢 Covered |
| TC-003.1.2 | Set completed=false | test_notes_status.py::test_mark_note_not_completed | 🟢 Covered |
| TC-003.1.3 | Update status of a non-existent note | test_notes_status.py::test_update_status_not_found | 🟢 Covered |
| TC-003.1.4 | Update status without a token | test_notes_status.py::test_update_status_no_token | 🟢 Covered |
| TC-003.1.5 | Update status of another user's note | — | 🟡 Test Missing |

### Epic EP-004: Validation & Error Handling
---
| TC ID | Test Case | Test Function | Status |
|-------|-----------|---------------|--------|
| TC-004.1.1 | Send a request with invalid JSON | — | 🟡 Test Missing |
| TC-004.1.2 | Send a request with an incorrect HTTP method | — | 🟡 Test Missing |
| TC-004.1.3 | Send a request to a non-existent endpoint | test_validation.py::test_nonexistent_endpoint | 🟢 Covered |
| TC-004.1.4 | Verify error response structure for 500 | — | 🟡 Test Missing |

### Epic EP-005: API Security
---
| TC ID | Test Case | Test Function | Status |
|-------|-----------|---------------|--------|
| TC-005.1.1 | Access protected endpoints with an expired token | test_auth.py::test_access_without_token | 🟢 Covered |
| TC-005.1.2 | Access protected endpoints with a fake token | test_security.py::test_fake_token_access | 🟢 Covered |
| TC-005.1.3 | Verify data isolation between users | test_security.py::test_note_isolation | 🟢 Covered |
| TC-005.1.4 | SQL injection in the title field | test_security.py::test_sql_injection_title | 🟢 Covered |

### Epic EP-006: Health Check
---
| TC ID | Test Case | Test Function | Status |
|-------|-----------|---------------|--------|
| TC-006.1.1 | Verify API health status | — | 🟡 Test Missing |
| TC-006.1.2 | Verify health-check response time | — | 🟡 Test Missing |

### Summary

- 🟢 **Covered**: 37 test cases have matching test functions
- 🟡 **Test Missing**: 19 test cases have no test function yet
- 🔵 **Case Missing**: 0 test functions have no test case in the spec

_Last generated: 2026-05-22 11:36:04 UTC_