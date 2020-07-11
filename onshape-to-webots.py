import json
import os
from shutil import which
import subprocess
import urdf2webots.importer as importer
from urdf_path_fixer import fix_urdf_path
from urllib.parse import urlparse


# Check if needed secrets are environment variables. If they're not prompt user for details and dump to file for reuse.
def generate_secrets():
    secrets = {}
    need_secrets = False

    if 'ONSHAPE_API' not in os.environ:
        secrets['onshape_api'] = 'https://cad.onshape.com'
        need_secrets = True
    else:
        secrets['onshape_api'] = os.getenv('ONSHAPE_API')

    if 'ONSHAPE_ACCESS_KEY' not in os.environ:
        print('OnShape access key not found please obtain from https://dev-portal.onshape.com/keys')
        secrets['onshape_access_key'] = input('OnShape Access Key:   ')
        need_secrets = True
    else:
        secrets['onshape_access_key'] = os.getenv('ONSHAPE_ACCESS_KEY')

    if 'ONSHAPE_SECRET_KEY' not in os.environ:
        print('OnShape secret key not found please obtain from https://dev-portal.onshape.com/keys')
        secrets['onshape_secret_key'] = input('OnShape Secret Key:   ')
        need_secrets = True
    else:
        secrets['onshape_secret_key'] = os.getenv('ONSHAPE_SECRET_KEY')

    if need_secrets:
        with open('secrets.json') as secrets_file:
            json.dump(secrets, secrets_file)

    return secrets


if __name__ == '__main__':
    # If a secrets.json exists, ask if we should use it. If shouldn't reuse or it doesn't exist run func
    if os.path.exists('secrets.json'):
        if input('Use pre-existing secrets.json? y/n').lower() == 'n':
            api_data = generate_secrets()
        else:
            api_data = json.loads('secrets.json')
    else:
        api_data = generate_secrets()

    # Get OnShape document ID and specific assembly name to fecth
    docId = urlparse(input('OnShape document URL:   ')).path.split('/')[2]
    assembly = input('Assembly name:  ')

    # Create folder to hold robot based on name of selected assembly
    if not os.path.isdir(assembly):
        os.mkdir(assembly)

    # Generate a temporary config.json file that includes secrets in case they're not environment variables.
    with open(assembly + '/config.json', 'w') as tmp_config:

        json.dump({'documentId': docId,
                   'assemblyName': assembly,
                   'onshape_api': api_data['onshape_api'],
                   'onshape_access_key': api_data['onshape_access_key'],
                   'onshape_secret_key': api_data['onshape_secret_key']}, tmp_config)
    tmp_config.close()
    print('Converting OnShape model to URDF... \n')

    python_string = 'python' if which('python') is not None else 'python3'

    # Run onshape-to-robot on the generated folder and config, this seems bad, consider refactor...
    log = subprocess.getoutput(python_string + ' invoke_onshape_to_robot.py ' + assembly)
    print(log)
    urdf_name = assembly + '/robot.urdf'
    print('Switching URDF mesh paths to aboslute...\n')
    fix_urdf_path(urdf_name)
    print('Converting URDF to PROTO...\n')
    importer.convert2urdf(urdf_name, assembly + '/' + assembly + '.proto')
