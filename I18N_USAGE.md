# Multi-Language Support Usage

The Beijing Subway Navigator now supports multiple languages using the standard GNU gettext system.

## Supported Languages

- English (en)
- Chinese (zh)

## How to Change Language

### Method 1: Environment Variable (Recommended)

Set the `LANGUAGE` environment variable before running the application:

```bash
# Use English
LANGUAGE=en python subway_navigation.py

# Use Chinese
LANGUAGE=zh python subway_navigation.py

# Or using uv run
LANGUAGE=zh uv run python subway_navigation.py
```

### Method 2: System Locale

The application will automatically detect your system's locale and use the appropriate language if available.

```bash
# On Linux/macOS, set locale in your shell profile (.bashrc, .zshrc, etc.)
export LANG=zh_CN.UTF-8

# Then run normally
python subway_navigation.py
```

### Method 3: Programming API

You can programmatically set the language in your code:

```python
from subway_navigation import BeijingSubwaySystem

system = BeijingSubwaySystem()
system.i18n.set_language('zh')  # Switch to Chinese
# or
system.i18n.set_language('en')  # Switch to English
system.run_interactive()
```

## Adding New Languages

### Step 1: Create Locale Directory

```bash
mkdir -p locale/<lang_code>/LC_MESSAGES
```

### Step 2: Initialize Translation File

```bash
pybabel init -i locale/messages.pot -d locale -l <lang_code>
```

Example:
```bash
pybabel init -i locale/messages.pot -d locale -l fr
```

### Step 3: Translate

Edit the newly created `.po` file at `locale/<lang_code>/LC_MESSAGES/messages.po`:

```po
msgid "Beijing Subway Graph Navigation System"
msgstr "French translation here..."
```

### Step 4: Compile

```bash
pybabel compile -d locale
```

## Updating Translations

If you modify the source code and add new translatable strings:

### Step 1: Extract New Strings

```bash
pybabel extract -F babel.cfg -o locale/messages.pot .
```

### Step 2: Update Existing Translations

```bash
pybabel update -i locale/messages.pot -d locale
```

This will merge new strings into existing `.po` files without overwriting your translations.

### Step 3: Translate New Strings

Edit the `.po` files to translate the new strings.

### Step 4: Recompile

```bash
pybabel compile -d locale
```

## File Structure

```
Beijing-Subway-Navigator/
├── babel.cfg                    # Babel configuration for string extraction
├── subway_navigation.py         # Main application with I18nManager class
└── locale/                       # Translation directory
    ├── messages.pot              # Portable object template (source strings)
    ├── en/                      # English translations
    │   └── LC_MESSAGES/
    │       ├── messages.po       # Editable translation file
    │       └── messages.mo       # Compiled binary file
    └── zh/                      # Chinese translations
        └── LC_MESSAGES/
            ├── messages.po
            └── messages.mo
```

## Technical Details

- **Library**: Python's built-in `gettext` module
- **Tooling**: Babel 2.17.0 for extraction and compilation
- **Format**: GNU gettext Portable Object (`.po`) and Machine Object (`.mo`) files
- **Encoding**: UTF-8 for all files
- **API**: Class-based (not global `gettext.install()`)

## Troubleshooting

### Language Not Loading

1. Check that the `.mo` file exists: `ls locale/<lang>/LC_MESSAGES/`
2. Verify the language code: use `en`, `zh`, not `en_US` or `zh_CN`
3. Check environment variable: `echo $LANGUAGE`
4. Try setting explicitly in code: `system.i18n.set_language('<lang_code>')`

### Garbled Text

If you see garbled characters, ensure your terminal is using UTF-8:

```bash
export LANG=en_US.UTF-8
# Or
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
```

### Adding New Translations Not Working

Make sure to:
1. Run `pybabel extract` after code changes
2. Run `pybabel update` (not `init`) for existing languages
3. Run `pybabel compile` to create `.mo` files
