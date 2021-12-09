import yaml, os

CONFIG_PATH='/app/src/{}/config/'.format(os.getenv('BOTTLE_APP_NAME'))

def load_config():
    environment = os.getenv('BOTTLE_APP_ENVIRONMENT')
    if not environment:
        print('Environment variable not defined')
        return {}
    
    yaml_config_file = '{config_path}/{environment}.yml'.format(config_path=CONFIG_PATH,environment=environment)
    if not os.path.isfile(yaml_config_file):
        print('Config file {} does not exist'.format(yaml_config_file))
        return {}

    try:
        with open(yaml_config_file, 'r') as f:
            yaml_result = yaml.safe_load(f)
    except Exception as e:
        print(e)
        yaml_result = {}
    return yaml_result