# Jay-Dhakan-

Python Overall Learning Test

All the mentioned endpoints are working as needed.
to run the app create a .env file with your environment variables and run
apps/app.py to run whole flask app.

Some additional features from my side::

1) added an extra endpoint to get all users.

2) added a privilege field while registering a user.
   with a simple function mention in privilege.py you can check a persons
   privilege. example: to get all users you must be logged in as a SUPER_ADMIN.

3) added pants mono-repo infrastructure:

   to use it you need just need to launch this two codes on your terminal:
   (make sure there is .env in root and it is not in .gitignore OR you will need
   to copy .env to anywhere you want to run pex)

   pants package apps:main (to convert whole flask app to one pex file)
   and
   ./root_to_pex_file/main.pex (./dist/apps/main.pex)

   pants takes care of everything you just need the same python version to run
   pex file which is 3.11 or greater in our case.

   there are many mare things that can be done with pants like running all test
   cases at once it can create docker image for us