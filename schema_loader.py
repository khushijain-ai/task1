import yaml

class SchemaLoader:
    def __init__(self, path="config/config.yaml"):
        with open(path, 'r') as f:
            self.config = yaml.safe_load(f)

    def get_config(self, runtime_toggles=None):
        import copy
        
        cfg = copy.deepcopy(self.config)
        
        
        toggles = runtime_toggles if runtime_toggles else {}
        
        for key in cfg['categories']:
            
            val = toggles.get(key, cfg['categories'][key].get('include', True))
            cfg['categories'][key]['include'] = val
            
        return cfg