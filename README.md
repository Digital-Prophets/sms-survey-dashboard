# SMS SURVEY DASHBOARD

A service for monitoring sms survey as well as reporting.

Note that sms-survey-dashboard is under development and not yet feature complete.

The latest source code is available at
[https://github.com/Digital-Prophets/sms-survey-dashboard](https://github.com/Digital-Prophets/sms-survey-dashboard).

* **Developers:** See our [developer guide](README-dev.md)
* **For production:** See our [deployment guide](README-docker.md)



## Quick Installation Guide

For deployment we use [docker](http://docker.com) so you need to have docker
running on the host. sms-survey-dashboard is a django app so it will help if you have
some knowledge of running a django site.

```
git clone git://github.com/Digital-Prophets/sms-survey-dashboard.git
cd sms-survey-dashboard/deployment
cp btsync-db.env.EXAMPLE btsync-db.env
cp btsync-media.env.EXAMPLE btsync-media.env

make build
make permissions
make web
# Wait a few seconds for the DB to start before to running the next command
make migrate
make collectstatic

```

At this point the project should be up and running at http://127.0.0.1:8005

If you need backups, put btsync keys in these files. If you don't need backups,
you can let the default content.

So as to create your admin account:
```
make superuser
```

**intercom.io**

If you wish to make use of [intercom.io](https://www.intercom.io), include a
`private.py` file in `core.settings` with your `INTERCOM_APP_ID` as a string.
The necessary code snippet is already included in `project_base.html`.

**github authentication**

Create a developer key here:

https://github.com/settings/applications/new

Set the callback and site homepage url to the top of your site e.g.

http://localhost:61202

At http://localhost:61202/en/site-admin/socialaccount/socialapp/add/

Set the key and secret from the github key page.

**Backups**

If you wish to sync backups, you need to establish a read / write btsync
key on your production server and run one or more btsync clients
with a read only key.

```
cd deployment
cp btsync-media.env.EXAMPLE btsync-media.env
cp btsync-db.env.EXAMPLE btsync-db.env
```

Now edit the ``btsync-media.env`` and ``btsync-db.env`` files, including
relevant SECRET and DEVICE settings.

## Thank you

Thank you to the individual contributors who have helped to improve the sms survey dashboard application:

* Alison Mukoma (Lead developer): alison@digiprophets.com
* Chriford Siame: chriford@digiprophets.com
* Prince Musole: prince@digiprophets.com
* Joshua Chipile: joshua@digiprophets.com
* David Utibe-Abasi Okuku: david@digiprophets.com
