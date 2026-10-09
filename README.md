# FORM / FITNESS

A database-backed strength training tracker built with Django, HTML, CSS, and vanilla JavaScript. It uses SQLite for local development and PostgreSQL when `DATABASE_URL` is set. The supplied exercise photos are optimized into `static/tracker/images/exercises/` and mapped to their matching movements in the exercise library, active workout, and workout summary. Four earlier UI mockups remain in the static assets but are not used as movement demonstrations.

## Requirements

- Python 3.10 or newer (developed with Python 3.12)
- Linux, macOS, or Windows
- Internet access for installing Python dependencies; the optional Manrope font has a system font fallback

## Setup on Linux

For an existing database, stop the server and back up `db.sqlite3` before applying new migrations. The account migration is additive and preserves legacy records, but the backup lets you restore the exact pre-migration file if needed. The local settings use SQLite unless `DATABASE_URL` is set.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_exercises
python manage.py runserver
```

Open http://127.0.0.1:8000. Register a regular account in the app; the username and password are stored with Django authentication and password hashing. To create an administrator for the separate Django Admin interface, run `python manage.py createsuperuser` and visit `/admin/`. Admin access does not replace the regular app account flow.

After migration, if this database has old workout data, register or choose the account that should own those records, then explicitly assign them to that account:

```bash
python manage.py assign_legacy_owner --username YOUR_USERNAME
```

Migration `0003` adds nullable ownership fields and preserves all existing workouts, preferences, and the old featured-exercise flag. Ownerless records stay hidden from normal accounts until assigned. The command only attaches unowned workouts; it attaches legacy preferences if the account has none, otherwise it leaves the old preference row untouched and reports that. Choose one account deliberately before assigning legacy rows.

Run the test suite with:

```bash
python manage.py test
```

## Exercise photos and static assets

Each provided movement photo is kept locally and mapped by `seed_exercises`; the website does not need an external image CDN for exercise photography. Re-run the seed command after adding or changing images so the catalog stores the corresponding relative static path. The rest timer sound is also local at `static/tracker/audio/can-we-get-much-higher-one-piece-meme.mp3`. Render's build runs `collectstatic`, and WhiteNoise serves these collected files with the deployed app.

## Deploy to Render with Neon PostgreSQL

The included `render.yaml` configures a free Render web service. Create a Neon PostgreSQL database, copy its connection string, and use it as `DATABASE_URL` when Render asks for the unsynced value. Use the pooled connection string from Neon if you expect multiple concurrent app connections. Do not commit the connection string or put it in this file. Render generates `DJANGO_SECRET_KEY`; the blueprint sets `DJANGO_DEBUG=false`. The app reads Render's `RENDER_EXTERNAL_HOSTNAME` automatically for allowed hosts and trusted CSRF origins.

The build command in `build.sh` installs requirements, collects static files, then runs additive Django migrations. The start command runs Gunicorn. Optional environment variables are comma-separated `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS`; the Render hostname is added automatically. When deploying outside Render, set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, `DATABASE_URL`, `DJANGO_ALLOWED_HOSTS`, and `DJANGO_CSRF_TRUSTED_ORIGINS` in the hosting provider's environment settings. Render's free web service sleeps after 15 minutes without traffic and its filesystem is ephemeral, so workout records must live in Neon rather than SQLite on Render. See [Render's free plan limits](https://render.com/docs/free).

### Move existing SQLite data safely

1. Stop the local server and make a separate backup copy of `db.sqlite3`. Keep the original file unchanged.
2. Make sure the SQLite database has the latest migrations. If it contains old ownerless workouts, register or choose the account that should own them and run `python manage.py assign_legacy_owner --username YOUR_USERNAME` before exporting. This is an explicit choice; deployment does not assign records automatically.
3. Make sure `DATABASE_URL` is unset in the local shell so Django selects SQLite, then export the data:

   ```bash
   python manage.py dumpdata --natural-foreign --natural-primary \
     --exclude=contenttypes --exclude=auth.permission --exclude=admin.logentry \
     --exclude=sessions --indent 2 > data-export.json
   ```

4. Set `DATABASE_URL` in the shell to the Neon connection string without saving it to source control. Then apply the schema to Neon and import the fixture:

   ```bash
   python manage.py migrate
   python manage.py loaddata data-export.json
   ```

5. Check the deployed users, workout history, preferences, and exercise images before removing the temporary `data-export.json`. It is ignored by Git because it contains personal records and password hashes. Retain the SQLite backup until the imported data is verified.

Do not delete `db.sqlite3` as part of deployment. Render's local service filesystem is not durable across all service operations, so PostgreSQL is the persistent production database; SQLite remains the local development default.

## Features

- Overview with database-backed workout totals, training time, streak, weekly sessions, and recent sessions.
- Start, pause, resume, finish, or cancel a session. The server stores authoritative timestamps; the browser derives elapsed time from them.
- Exercise selection, set logging, set completion, workout notes, and a browser-side rest timer with 30, 60, 90, and 120 second presets, using the supplied local MP3 alarm by default.
- Search and filter the exercise library by muscle group, equipment, and difficulty. Each movement card and workout breakdown uses its matching local photo; the seed command loads exercises across the eight required muscle groups.
- Completed workout history with date/muscle filters, detailed set summaries, volume totals, and POST-only deletion.
- Analytics for completed sets, weekly activity, duration, muscle distribution, and exercise volume.
- Account-scoped preferences and exercise favorites; all workouts, sets, history, and analytics are filtered to the logged-in account.
- Registration, login, and POST-only logout using Django’s built-in authentication and password hashing.
- Django admin for users, exercises, muscle groups, workouts, sets, and preferences.

Weight is consistently recorded per dumbbell. Every app page except login and registration requires authentication. Django Admin remains a separate staff interface. Session content and settings are stored in `db.sqlite3`.

## Project structure

```text
config/                 Django settings and root URL configuration
tracker/models.py        Muscle groups, exercises, workouts, sets, preferences, favorites
tracker/services.py      Workout state transitions and timing
tracker/views.py         Auth, ownership-scoped dashboard and feature views
tracker/management/      Seed exercise management command
tracker/migrations/      Django schema migrations
templates/               Django HTML templates
static/tracker/          CSS, JavaScript, and local image assets
pictures/                Original supplied images
```
