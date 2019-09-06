import os
import logging
from configparser import ConfigParser

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
DB_CONFIG_PATH = os.path.join(THIS_DIR, 'db_config.ini')

def parse_config(config_path=DB_CONFIG_PATH, section='postgresql'):
    """Read DB_CONFIG_PATH & parse the section postgresql in that file then return db credentials.

    Keyword Arguments:
        config_path {[type]} -- [description] (default: {DB_CONFIG_PATH})
        section {str} -- [description] (default: {'postgresql'})

    Raises:
        Exception: [If there's no section 'postgresql' in DB_CONFIG_PATH, then raise error]

    Returns:
        [list] -- [credentials for the db]
    """
    # create a parser
    parser = ConfigParser()

    # read the configuration
    parser.read(config_path)

    # get the section
    obj = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            obj[param[0]] = param[1]

    else:
        raise ValueError('Section {0} not found in the {1} file'.format(section, config_path))
    return obj

def get_postgres_url(config_path=DB_CONFIG_PATH, **config_overrides):
    url_base = 'postgresql+psycopg2://{user}:{password}@{host}/{database}'
    try:
        postgres_config = parse_config(config_path=config_path, section='postgresql')
    except Exception as exc:
        logging.debug('Exception while parsing Postgres config. {}: {}'.format(type(exc).__name__, str(exc)))
        postgres_config = {
            'user': os.environ.get('POSTGRES_USER', 'postgres'),
            'password': os.environ.get('POSTGRES_PASSWORD', ''),
            'host': os.environ.get('POSTGRES_HOST', 'localhost'),
            'database': os.environ.get('POSTGRES_DATABASE', 'my_db'),
        }
        postgres_config.update(config_overrides)
    postgres_url = url_base.format(**postgres_config)
    print("this is postgres_url", postgres_url)
    return postgres_url