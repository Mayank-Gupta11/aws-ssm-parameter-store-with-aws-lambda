import json
import boto3
import configparser


client=boto3.client('ssm')
ssm_path='/prod/oracle/somedb'

ssm_full_path=ssm_path+'/write'

def lambda_handler(event, context):
    
    config=get_config(ssm_path)
    rds_host = config[ssm_full_path]['host']
    db_name = config[ssm_full_path]['dbname']
    name = config[ssm_full_path]['userid']
    password = config[ssm_full_path]['password']
    
    print(rds_host)
    print(db_name)
    print(name)
    print(password)
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
def get_config(path):
    configuration = configparser.ConfigParser()
    
    param_details=client.get_parameters_by_path(
        Path=path,
        Recursive=False,
        WithDecryption=True
    )
    
    print(param_details)
    
    print(param_details.get('Parameters'))
    
    if 'Parameters' in param_details and len(param_details.get('Parameters')) > 0:
        for param in param_details.get('Parameters'):
            section_name =  param.get('Name')
            config_values = json.loads(param.get('Value')) #converting json to dict..
            config_dict = {section_name: config_values}
            configuration.read_dict(config_dict) #passing dict..
    return configuration 
