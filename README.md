# PythonPublicPackages

## Description
This repository contains AstraZeneca public packages.

At the moment the following packages are added:

1) `claas` package contains:
* Configuration
* Logging

#### Creating a package

To create a package in dist/ directory, run:  
`python3 setup.py sdist bdist_wheel`


#### Installing a package from repository

To install a package set `egg=` and `&subdirectory=` parameters to package name:

```
# via https
pip install "git+https://github.com/AstraZeneca-NGS/PythonPublicPackages.git#egg=claas&subdirectory=claas"

# via ssh
pip install "git+ssh://git@github.com/AstraZeneca-NGS/PythonPublicPackages.git#egg=claas&subdirectory=claas"
```

Then you can import them as the following:

`from claas.src.config import Configurable`

#### Run tests

Just run shell script `run_tests.sh` in the package dir.


## Usage Examples

### Config

Direct inheritance from Configurable and creating an instance using dataclasses are described below.

#### Direct inheritance
One of possible ways is to create a config class and use it in your app:

    from claas.src.config import Configurable
    
    class Config(Configurable):
        def __init__(self, config_file: str = None):
            self.log_dir = None
            self.default_log = None
            self.exceptions = {}
            super().__init__(config_file)
            
        ... other methods you want to add
    
    config = Config(path_to_config)

All attributes to set from config file should be declared before super `__init__()` call. Otherwise if an attribute 
is missed in class definition (in `self.__dict__`) but exist in config file Exception will be raised.
 
You can also use `section` parameter of Configurable to set it from a specific section of a config file:

    class Config(Configurable):
        def __init__(self, config_file: str, section: str):
            self.log_dir = None
    
    config = Config(path_to_config, 'first_section')

#### Using dataclasses

If you have specific functionality and several configs that all must use this functionality, you can use
dataclasses:

    from dataclasses import dataclass
    @dataclass
    class Config(Configurable):
        filename: str = None
        section: str = None
    
        def __post_init__(self):
            super().__init__(self.filename, self.section)

        ... specific functionality methods here
        
Then inherit in your config classes:

    class AppConfig(Config):
        def __init__(self, app_config, config_file=None):
            self.project = None
            super().__init__(config_file)
            
All classes will have ability to run added functionality and also will have checks on 
attributes in `self.__dict__`.
    
### Logging

By default the logger outputs data to console log.
To enable output to file, use `redirect` parameter as shown below using path to file. 
This will create log file and also will rotate it each time it exceeds ~10Mb (up to 1000 files). 
If there will be more than 1000 files, old files will be overwritten.

Also you can enable options `is_debug` and `is_verbose` to set specific log levels 
(for example, from args).

You can create a helper Logger to operate in your app without need to set it in instances, like:

    from claas.src.log import Log
    class Logger:
        _logs = {}
    
        @classmethod
        def log(cls) -> Log:
            return cls._logs['Log']
    
        @classmethod
        def configure_logging(cls, args, log_dir, default_log):
            path = os.path.join(log_dir, default_log)
            if args.debug or args.test:
                log = Log(redirect=path, is_debug=True)
            elif args.verbose:
                log = Log(redirect=path, is_verbose=True)
            else:
                log = Log(redirect=path)
            cls._logs['Log'] = log
        

Then you can set a configuration once and then import it:

    # main module/config
    from your_app.logs import Logger
    Logger.configure_logging(args, app_config.log_dir, app_config.default_log)

    # other modules
    from your_app.logs import Logger
    Logger.log().debug('Message')
