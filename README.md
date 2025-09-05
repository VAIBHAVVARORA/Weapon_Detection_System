# Weapon-Detection-Web-App
How to setup ?
1) Clone this repo.
    ```bash
    git clone https://github.com/Spyrosigma/HackJnu3-Project.git
3) Install the required Libraries
    ```bash
    pip install -r requirements.txt
    ```
4) To run the web-app
    ```bash
    python manage.py runserver
    ```

## Some Modification that you have to make in Ultralytics  ( C:\users\hp\appdata\local\programs\python\python311\lib\site-packages\ultralytics\utils\__init__.py) --- around line 225
```bash
    
    from colorama import AnsiToWin32
    WINDOWS = True
    def set_logging(name=LOGGING_NAME, verbose=True):
        """Sets up logging for the given name with UTF-8 encoding support."""
        level = logging.INFO if verbose and RANK in {-1, 0} else logging.ERROR  # rank in world for Multi-GPU trainings
    
        # Configure the console (stdout) encoding to UTF-8
        formatter = logging.Formatter('%(message)s')  # Default formatter
        if isinstance(sys.stdout, AnsiToWin32):
            # Check if 'encoding' attribute exists before accessing it
            if hasattr(sys.stdout, 'encoding') and WINDOWS and sys.stdout.encoding != 'utf-8':
                try:
                    if hasattr(sys.stdout, 'reconfigure'):
                        sys.stdout.reconfigure(encoding='utf-8')
                    elif hasattr(sys.stdout, 'buffer'):
                        import io
                        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
                    else:
                        sys.stdout.encoding = 'utf-8'
                except Exception as e:
                    print(f'Creating custom formatter for non UTF-8 environments due to {e}')
    
                    class CustomFormatter(logging.Formatter):
    
                        def format(self, record):
                            return emojis(super().format(record))
    
                    formatter = CustomFormatter('%(message)s')  # Use CustomFormatter to eliminate UTF-8 output as last recourse
```


Contact me for any doubts.


## Labelled Images given to model
![val_batch0_labels](https://github.com/Spyrosigma/HackJnu3-Project/assets/111422209/ca6afd4d-9639-463c-9c73-6f0e5428686b)

## Detected By Model
![val_batch0_pred](https://github.com/Spyrosigma/HackJnu3-Project/assets/111422209/f87aba9c-ec3f-4db0-8d9c-a0e3ac900941)


