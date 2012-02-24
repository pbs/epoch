Epoch! : PBS management tool for Righscale environments
=========================================

Features:

    * Register / Delete New Deployments
    * Register / Delete Single Server
        - Misc Servers Section
    * Register / Delete Single RDS
        - Misc RDS Section
    * Deployment operational hours
        - Server operational from time till time
        - Registered in UTC (for forms sake probably)
        - Web app time zone sensitive (or it may makes sense to hard wire to EST since its internal only)
    * Start Deployment Now
        - Auto Next Check Override
        - This is to insure servers are turned off too soon
    * Stop Deployment Now
        - Starts Normally Next Check
    * UUA Login
        - Groups or Deployment based assignments
        - this is some extended functionality.
        - simple UUA authentication is all thats needed


Some missing considerations:
    * RDS Slaves
        - do they need to register with HA Proxy
        - can this be automated
    * execution of backup script
        - Is there a way to do this as part of the (prior) stop command
        - Does it matter in the case of application servers?