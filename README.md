This is a script that I've used to check for an available vaccination appointment.
After specifying the ID of the vaccination center, the script periodically retrieves a list of dates and numbers of available spots from the registration system of the National Health Information Centre of Slovak Republic.
Disclaimer: the registration system is not available anymore.

After a free spot is found, it notifies the user by sending an email and calling a specified number using Twilio.