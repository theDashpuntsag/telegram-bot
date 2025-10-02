import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv



@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    host: str
    port: int
    dbname: str
    user: str
    password: str
    min_connections: int = 1
    max_connections: int = 10
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for psycopg2."""
        return {
            'host': self.host,
            'port': self.port,
            'dbname': self.dbname,
            'user': self.user,
            'password': self.password
        }

@dataclass
class LoggingConfig:
    """Logging configuration settings."""
    level: str = 'DEBUG'
    log_dir: str = 'logs'
    backup_count: int = 60
    max_file_size: str = '10MB'
    console_logging: bool = True
    file_logging: bool = True


@dataclass
class AWSConfig:
    """AWS configuration settings."""
    region: str = 'us-east-1'
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    dynamodb_table_prefix: str = ''


@dataclass
class AppConfig:
    """Main application configuration."""
    environment: str = 'development'
    debug: bool = False
    app_name: str = 'Python Template'
    version: str = '1.0.0'


class Config:
    """Configuration manager for the application."""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            env_file: Path to environment file. If None, looks for .env in project root.
        """
        self._load_environment(env_file)
        self.app = self._load_app_config()
        self.database = self._load_database_config()
        self.logging = self._load_logging_config()
        self.aws = self._load_aws_config()
    
    def _load_environment(self, env_file: Optional[str] = None):
        """Load environment variables from .env file if it exists."""
        try:            
            if env_file:
                env_path = Path(env_file)
            else:
                env_path = Path(__file__).parent / '.env'
            
            if env_path.exists():
                load_dotenv(env_path)
                print(f"Loaded environment from {env_path}")
            else:
                print("No .env file found, using system environment variables")
                
        except ImportError:
            print("python-dotenv not installed. Install it with: pip install python-dotenv")
            print("Using system environment variables only")
    
    def _load_app_config(self) -> AppConfig:
        """Load application configuration from environment variables."""
        return AppConfig(
            environment=os.getenv('ENVIRONMENT', 'development'),
            debug=os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes'),
            app_name=os.getenv('APP_NAME', 'Python Template'),
            version=os.getenv('APP_VERSION', '1.0.0')
        )
    
    def _load_database_config(self) -> DatabaseConfig:
        """Load database configuration from environment variables."""
        return DatabaseConfig(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '5432')),
            dbname=os.getenv('DB_NAME', 'template_db'),
            user=os.getenv('DB_USER', 'template_user'),
            password=os.getenv('DB_PASSWORD', ''),
            min_connections=int(os.getenv('DB_MIN_CONNECTIONS', '1')),
            max_connections=int(os.getenv('DB_MAX_CONNECTIONS', '10'))
        )
    
    def _load_logging_config(self) -> LoggingConfig:
        """Load logging configuration from environment variables."""
        return LoggingConfig(
            level=os.getenv('LOG_LEVEL', 'DEBUG').upper(),
            log_dir=os.getenv('LOG_DIR', 'logs'),
            backup_count=int(os.getenv('LOG_BACKUP_COUNT', '60')),
            max_file_size=os.getenv('LOG_MAX_FILE_SIZE', '10MB'),
            console_logging=os.getenv('LOG_CONSOLE', 'True').lower() in ('true', '1', 'yes'),
            file_logging=os.getenv('LOG_FILE', 'True').lower() in ('true', '1', 'yes')
        )
    
    def _load_aws_config(self) -> AWSConfig:
        """Load AWS configuration from environment variables."""
        return AWSConfig(
            region=os.getenv('AWS_REGION', 'us-east-1'),
            access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            dynamodb_table_prefix=os.getenv('DYNAMODB_TABLE_PREFIX', '')
        )
    
    def validate(self) -> bool:
        """
        Validate configuration settings.
        
        Returns:
            True if configuration is valid, False otherwise.
        """
        errors = []
        
        # Validate database config
        if not self.database.password and self.app.environment == 'production':
            errors.append("Database password is required in production")
        
        if not self.database.host:
            errors.append("Database host is required")
        
        # Validate logging config
        if self.logging.level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            errors.append(f"Invalid log level: {self.logging.level}")
        
        if errors:
            print("Configuration validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    def get_database_url(self) -> str:
        """Get database URL for connection."""
        return (
            f"postgresql://{self.database.user}:{self.database.password}"
            f"@{self.database.host}:{self.database.port}/{self.database.dbname}"
        )
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.app.environment.lower() == 'development'
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app.environment.lower() == 'production'


# Global configuration instance
config = Config()