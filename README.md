# Setup the application
Tested with Python 3.11.7
```
pip install -r requirements
pip install -e .
```

# Run the application

```
unbabel_cli --input_file "events.json" --window_size 10
```

# Run tests

In the project root folder run:
```
pytest .
```