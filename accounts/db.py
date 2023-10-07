from django.conf import settings
from django.db import connection, connections
from django.db.backends.postgresql.base import DatabaseWrapper

USER_MODEL = settings.AUTH_USER_MODEL
PG_USER_MODEL = USER_MODEL.replace(".", "_")


def prevent_permanent_users_update_trigger(sender, **kwargs):
    # Only trigger signal for Postresql
    if not isinstance(connections["default"], DatabaseWrapper):
        return

    trigger_sql = """
    -- Clean up any existing trigger
    DROP TRIGGER IF EXISTS prevent_permanent_users_update_trigger ON %(mdl)s;
    DROP FUNCTION IF EXISTS prevent_permanent_users_update() CASCADE;


    -- Create a function that checks the constraints
    CREATE OR REPLACE FUNCTION prevent_permanent_users_update()
    RETURNS TRIGGER AS $$
    BEGIN
        IF (OLD.username = 'watcher') or (OLD.username = 'deleted') THEN
            RAISE EXCEPTION 'Update of server users is prohibited.';
        END IF;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    -- Create a trigger that calls the function before update
    CREATE TRIGGER prevent_permanent_users_update_trigger
    BEFORE UPDATE ON %(mdl)s
    FOR EACH ROW
    EXECUTE FUNCTION prevent_permanent_users_update();
    """ % {
        "mdl": PG_USER_MODEL
    }

    with connection.cursor() as cursor:
        # Create the PostgreSQL function to enforce the constraint

        with connection.cursor() as cursor:
            cursor.execute(trigger_sql)


def prevent_permanent_users_deletion_trigger(sender, **kwargs):
    # Only trigger signal for Postresql
    if not isinstance(connections["default"], DatabaseWrapper):
        return

    trigger_sql = """
    -- Clean up any existing trigger
    DROP TRIGGER IF EXISTS prevent_permanent_users_deletion_trigger ON %(mdl)s;
    DROP FUNCTION IF EXISTS prevent_permanent_users_deletion() CASCADE;

    -- Create a function that checks the constraints
    CREATE OR REPLACE FUNCTION prevent_permanent_users_deletion()
    RETURNS TRIGGER AS $$
    BEGIN
        IF (OLD.username = 'watcher') or (OLD.username = 'deleted') THEN
            RAISE EXCEPTION 'Deletion of server users is prohibited.';
        END IF;
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

    -- Create a trigger that calls the function before deletion
    CREATE TRIGGER prevent_permanent_users_deletion_trigger
    BEFORE DELETE ON %(mdl)s
    FOR EACH ROW
    EXECUTE FUNCTION prevent_permanent_users_deletion();
    """ % {
        "mdl": PG_USER_MODEL
    }

    with connection.cursor() as cursor:
        # Create the PostgreSQL function to enforce the constraint

        with connection.cursor() as cursor:
            cursor.execute(trigger_sql)
