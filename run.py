from src.routes import app
from src.schema_loader import SchemaLoader

# Load config to get system variables
loader = SchemaLoader()
config = loader.get_config()
sys_cfg = config.get('system', {})

if __name__ == "__main__":
    app.run(
        host=sys_cfg.get('host', '127.0.0.1'),
        port=sys_cfg.get('port', 5000),
        debug=sys_cfg.get('debug', False)
    )