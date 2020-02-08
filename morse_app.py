"""
Morse Code Translator Web App.

This app provides a REST API for morse encoding/decoding.
"""

import os
import sys

import click
import pytest


# Integrating code coverage in the app script presents a problem.
# By the time the test command is executed with the test() function,
# it isalready too late to enable coverage metrics; by that time all
# the code in the global scope has already executed.
# So, to get accurate metrics, the script recursively restarts itself
# after setting the FLASK_COVERAGE environment variable. In the second
# run, the top of the script finds that the environment variable is set
# and turns on coverage from the start, even before all the application
# imports.
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True,
                            include=['src/meli/morse/domain/*',
                                     'src/meli/morse/app/*'])
    COV.start()


from meli.morse.app import create_app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.cli.command()
def test():
    """Run the unit tests."""
    if not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    pytest.main(["-x", "tests"])

    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@app.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
              help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    # Needed to call app.run() outside if __name__ == '__main__' guard
    os.environ["FLASK_RUN_FROM_CLI"] = "false"
    app.run(debug=False)
