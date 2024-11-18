from pathlib import Path

import click
from django.conf import settings
from django_kt_template_by_k_tech.config.environ import env

from django_kt_template_by_k_tech.cli import global_options
from django_kt_template_by_k_tech.signals import (django_kt_template_by_k_tech_version_upgraded,
                               cli_django_kt_template_by_k_tech_execute_command,
                               cli_django_kt_template_by_k_tech_upgrade_templates,)
from django_kt_template_by_k_tech.utils.reflect import fqn


def configure_master_app():
    from django.conf import settings

    pass


def configure_django_kt_template_by_k_tech_app():
    from django.conf import settings

    pass


def configure_beat():
    pass
    from django_celery_beat.models import (CrontabSchedule,
                                           IntervalSchedule, PeriodicTask,)

    from django_kt_template_by_k_tech.engine.tasks.periodic import (
                                                 check_monitors, clearsessions,
                                                 consolidate, healthcheck,
                                                 loadavg,
                                                 sync_gauges,)
    hourly, __ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.HOURS
    )

    midnight, __ = CrontabSchedule.objects.get_or_create(
        minute=0,
        hour=0,
        timezone=settings.TIME_ZONE
    )

    minute, __ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES
    )

    # Create Periodic tasks here


def configure_dirs(prompt, verbose):
    from django_kt_template_by_k_tech.config.environ import env
    for _dir in ('MEDIA_ROOT', 'STATIC_ROOT'):
        target = Path(env.str(_dir))
        if not target.exists():
            if prompt:
                ok = click.prompt(f"{_dir} set to '{target}' but it does not exists. Create it now?")
            else:
                ok = True
            if ok:
                if verbose > 0:
                    click.echo(f"Create {_dir} '{target}'")
                target.mkdir(parents=True)


@click.command()  # noqa: C901
@global_options
@click.option('--prompt/--no-input', default=True, is_flag=True,
              help='Do not prompt for parameters')
@click.option('--migrate/--no-migrate', default=True, is_flag=True,
              help='Run database migrations')
@click.option('--emails/--no-emails', default=True, is_flag=True,
              help='Load email templates')
@click.option('--documents/--no-documents', default=True, is_flag=True,
              help='Load documents templates')
@click.option('--static/--no-static', default=False, is_flag=True,
              help='Collect static assets')
@click.option('--reindex/--no-reindex', default=False, is_flag=True,
              help='Run Database full reindex')
@click.option('--check/--no-check', 'run_check', default=True, is_flag=True,
              help='Run check framework')
@click.option('--traceback', '-tb', default=False, is_flag=True,
              help='Raise on exceptions')
@click.option('--admin-email', '-ae', default=env.str('ADMIN_EMAIL'), help='Do not prompt for parameters')
@click.option('--admin-username', '-au', default=env.str('ADMIN_USERNAME'), help='Do not prompt for parameters')
@click.option('--admin-password', '-ap', default=env.str('ADMIN_PASSWORD'), help='Do not prompt for parameters')
@click.pass_context
def upgrade(ctx, prompt, migrate, static, verbose, run_check,  # noqa: C901
            emails, traceback, documents, admin_username, admin_email, admin_password, **kwargs):
    """Perform any pending database migrations and upgrades."""
    import django
    from django.core.management import call_command
    from django.db.transaction import atomic

    from django_kt_template_by_k_tech.sentry import capture_exception
    from django_kt_template_by_k_tech.system import state
    state.upgrade = True
    try:

        extra = {'no_input': prompt,
                 'verbosity': verbose - 1}

        configure_dirs(prompt, verbose)
        django.setup()

        from django_kt_template_by_k_tech import get_full_version
        from django_kt_template_by_k_tech.models import SysLogEntry
        from django_kt_template_by_k_tech.system import core

        with atomic():

            if static:
                if verbose == 1:
                    click.echo('Run collectstatic')
                call_command('collectstatic', **extra)

            if migrate:
                if verbose >= 1:
                    click.echo('Run migrations')
                call_command('migrate', **extra)

                configure_django_kt_template_by_k_tech_app()
                configure_master_app()

            if documents:
                if verbose >= 1:
                    click.echo('Populate default documents')
                from django_kt_template_by_k_tech.web.views.terms import Document
                Document.objects.populate()

            if emails:
                from django_kt_template_by_k_tech.models import EmailTemplate, SystemEmailTemplate
                SystemEmailTemplate.objects.populate()

                from django_kt_template_by_k_tech.models import Content, Organization
                if verbose == 1:
                    click.echo('Populate default Email Templates')
                    click.echo('Populate default Content Pages')

            cli_django_kt_template_by_k_tech_upgrade_templates.send(sender=core, verbosity=verbose, context=ctx)

            if run_check:
                from .check import check
                ctx.invoke(check, verbose=verbose, **kwargs)

            if verbose >= 1:
                click.echo('Configure default Celery Beat period tasks')
            configure_beat()

            if admin_email:
                try:
                    email = admin_email.strip()
                    validate_email(email)
                except ValidationError as e:
                    ctx.fail('\n'.join(e.messages))

                admin_password = admin_password.strip()
                if not admin_password:
                    ctx.fail('You must provide a password')
                try:
                    user = User.objects.create_superuser(admin_username, admin_email, admin_password)
                    if verbosity > 0:
                        click.echo(f'Created superuser {user.username}')
                except IntegrityError as e:
                    click.secho(f'Unable to create superuser: {e}', fg='yellow')

        cli_django_kt_template_by_k_tech_execute_command.send(sender=upgrade, context=ctx)

        last_record = SysLogEntry.objects.filter(organization__is_core=True,
                                                 extra__updated=True).first()
        current_version = get_full_version()
        if not last_record or last_record.extra.get('version', '') != current_version:
            django_kt_template_by_k_tech_version_upgraded.send(sender=core, version=current_version)
            core.logger.info('django_kt_template_by_k_tech has been updated to %s' % current_version,
                             extra={'version': current_version,
                                    'updated': True,
                                    })
    except Exception as e:
        if traceback:
            raise
        capture_exception(e)
        click.echo(str(e))
        ctx.abort()
