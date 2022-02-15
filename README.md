Title:
API Service for CRUD

Description:
Consider a store which has an inventory of boxes which are all cuboid(which have length breadth and height). Each Cuboid has been added by a store employee who is associated as the creator of the box even if it is updated by any user later on.


Tasks:
0. Data Modelling

    Build minimal Models required for the such a store. You can use contrib modules for necessary models(for eg: users)

Build api for the following specifications:
1. Add Api:
    Adding a box with given dimensions(length breadth and height).
    Adding user should be automatically associated with the box and shall not be overridden

    Permissions:
          User should be logged in and should be staff to add the box

2. Update Api:
    Update dimensions of a box with a given id:

    Permissions:
          Any Staff user should be able to update any box. but shall not be able to update the creator or creation date

3. List all Api
    List all boxes available:
    Data For each box Required:
            1. Length
            2. width
            3. Height
            4. Area
            5. Volume
            6. Created By :  (This Key shall only be available if requesting user is staff)
            7. Last Updated :  (This Key shall only be available if requesting user is staff)

    Permissions:
            Any user shall be able to see boxes in the store

    Filters:
            1. Boxes with length_more_than or length_less_than
            2. Boxes with breadth_more_than or breadth_less_than
            3. Boxes with height_more_than or height_less_than
            4. Boxes with area_more_than or area_less_than
            5. Boxes with volume_more_than or volume_less_than
            6. Boxes created by a specific user by username
            7. Boxes created before or after a given date

4. List my boxes:

    List all boxes available created by me:

    Data For each box Required:

            1. Length

            2. width

            3. Height

            4. Area

            5. Volume

            6. Created By

            7. Last Updated

    Permissions:
            Only Staff user shall be able to see his/her created boxes in the store

    Filters:

            1. Boxes with length_more_than or length_less_than

            2. Boxes with breadth_more_than or breadth_less_than

            3. Boxes with height_more_than or height_less_than

            4. Boxes with area_more_than or area_less_than

            5. Boxes with volume_more_than or volume_less_than

4. Delete Api:

    Delete a box with a given id:

    Permissions:

         Only the creator of the box shall be able to delete the box.

Conditions to be fulfilled on each add/update/delete:

Average area of all added boxes should not exceed A1

Average volume of all boxes added by the current user shall not exceed V1

Total Boxes added in a week cannot be more than L1

Total Boxes added in a week by a user cannot be more than L2

Values A1, V1, L1 and L2 shall be configured externally. You can choose 100, 1000, 100, and 50 as their respective default values.


WORKING LINKS:

API ENDPOINTS

STAFF SIGNUP PAGE: http://127.0.0.1:8000/accounts/staff-signup/

LOGIN PAGE: http://127.0.0.1:8000/accounts/login/

LOGOUT PAGE: http://127.0.0.1:8000/accounts/logout/

LISTING ALL THE BOXES CREATED EVER BY ALL USERS: http://127.0.0.1:8000/boxes/list-all-boxes

CREATING A BOX: http://127.0.0.1:8000/boxes/create-box

UPDATING THE DIMENSIONS OF BOX: http://127.0.0.1:8000/boxes/update-box/uuid

LISTING ALL BOXES CREATED BY SIGNED IN USER: http://127.0.0.1:8000/boxes/list-my-boxes

DELETING A BOX: http://127.0.0.1:8000/boxes/delete-box/uuid


Authentication Details

I have implemented default token authentication available in the Django Rest Framework.

When the user logs in through http://127.0.0.1:8000/accounts/login/, the token is generated and stored in the database.

So, in order to access the API, you need to send a valid token in the Authorization header as follows:

For this we can use Mod Header Extension of GOOGLE

Authorization: Token <generated token>
Token


Task 0: Data Modelling
I have created a boxes model with one to many relationship with the users model, where user model is the parent and boxes model is the child.




Task 1: Add a Box
API Endpoint: POST http://127.0.0.1:8000/boxes/create-box
Only the Staff user is able to create a box and following is the required payload for the request.

{
    "height": value,
    "length": value,
    "breadth": value
}
Below is the example of the API:

Add API

If the request is invalid or provided with invalid body, the API will return error messages.

Conditions fulfilled:
The user should be a staff and logged in to create a box.
Average area of all added boxes should not exceed 100.
Average volume of all boxes added by the current user shall not exceed 1000.
Total Boxes added in a week cannot be more than 100.
Total Boxes added in a week by a user cannot be more than 50.

Task 2: Update API for a Box
API Endpoint: PUT/PATCH http://127.0.0.1:8000/boxes/update-box/uuid
You need to add the UUID of the box at the end of the URL to update the box.

Below is the example of the Update API through PUT method:
Update PUT API

Below is the example of the Update API through PATCH method:
Update PATCH API

Conditions fulfilled:
User should be logged in and should be a staff user to access the API.
Any staff user is able to update any box.
Editor cannot edit the creator, created_date or last_updated date of the box.

Task 3: List all Boxes
API Endpoint: GET http://127.0.0.1:8000/boxes/list-all-boxes
This API returns all the boxes in the database but the response is divided into 2 types:

If User is staff, they can see the creator and last_updated date of each box. Staff Boxes Response

But in case of the non staff user they cannot see the creator and last_updated date of each box.Non Staff Boxes Response


In this API you can also apply below filters:

length_more_than or length_less_than
height_more_than or height_less_than
breadth_more_than or breadth_less_than
volume_more_than or volume_less_than
area_more_than or area_less_than
created_after or created_before
username
Conditions fulfilled:
User should be logged-in and authenticated to access this API.

Task 4: List my boxes
API Endpoint: GET http://127.0.0.1:8000/boxes/list-my-boxes
This API returns all the boxes created by the logged-in staff user.

ListMyBoxesStaffUser

In this API you can also apply below filters:

length_more_than or length_less_than
height_more_than or height_less_than
breadth_more_than or breadth_less_than
volume_more_than or volume_less_than
area_more_than or area_less_than
Conditions fulfilled:
User should be staff, logged-in and authenticated to access this API.

Task 5: Delete a Box
API Endpoint: DELETE http://127.0.0.1:8000/boxes/delete-box/uuid
You need to add the UUID of the box to be deleted at the end of the URL, and only the creator of the box can delete it.

DeleteAPI

Conditions fulfilled:
User should be staff, logged-in and authenticated to access the API.
The box to delete should be created by the logged-in staff user.
