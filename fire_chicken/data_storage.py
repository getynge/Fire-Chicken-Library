import os, json

from .mouse_position import MousePosition

class DirectoryRelativeException(Exception):
    pass

DEFAULT_MAX_BYTES = 50000000
class Storage:
    #Half a gigabyte
    def __init__(self, directory, *, max_bytes = DEFAULT_MAX_BYTES):
        if _directory_is_absolute_path(directory):
            self.directory = directory
        else:
            raise DirectoryRelativeException(directory)
        _create_directory_if_nonexistent(self.directory)
        self.max_bytes = max_bytes

    def get_position_file(self, name: str):
        return self.get_storage_file(name, MousePositionFile) 
    
    def get_integer_file(self, name: str):
        return self.get_storage_file(name, IntegerFile)
    
    def get_float_file(self, name: str):
        return self.get_storage_file(name, FloatFile)
    
    def get_string_file(self, name: str):
        return self.get_storage_file(name, StringFile)
    
    def get_boolean_file(self, name: str):
        return self.get_storage_file(name, BooleanFile)

    def get_json_file(self, name: str, from_json = None, *, default = None, cls = None, initial_value = None):
        return JSONFile(self.get_path(), name, from_json = from_json, default = default, cls = cls, 
        initial_value = initial_value)

    def get_storage_file(self, name: str, type):
        return type.create(self.get_path(), name, max_bytes = self.max_bytes)

    def get_path(self):
        return self.directory

def _create_directory_if_nonexistent(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def _directory_is_absolute_path(path):
    return os.path.isabs(path)

class RelativeStorage(Storage):
    def __init__(self, path, name = 'Fire Chicken Storage', *, max_bytes = DEFAULT_MAX_BYTES):
        target_directory = _compute_directory_at_path(path)
        dir = _join_path(target_directory, name)
        Storage.__init__(self, dir, max_bytes = max_bytes)

def _compute_directory_at_path(path):
    if os.path.isdir(path):
        return path
    else:
        return _compute_file_directory(path)

def _compute_file_directory(path):
    absolute_filepath = os.path.abspath(path)
    file_directory = os.path.dirname(absolute_filepath)
    return file_directory

def _join_path(directory, path):
    return os.path.join(directory, path)

#Parent class not meant to be instantiated
#Implement Python string method for storing object for storage
    #or override _convert_to_text
#Implement classmethod get_value_from_text for reading from the file
#Implement _get_initial_value for setting the initial value
class StorageFile:
    def __init__(self, directory: str, name: str, *, max_bytes: int = DEFAULT_MAX_BYTES):
        self.directory = directory
        self.name = name
        self.max_bytes = max_bytes
        self._initialize_file_if_nonexistent()
        self._load_value_from_file()
    @classmethod
    def create(cls, directory: str, name: str, *, max_bytes: int = DEFAULT_MAX_BYTES):
        return cls(directory, name, max_bytes = max_bytes)


    def get(self):
        return self.value
    
    def set(self, value):
        self.value = value
        self._store_value()
    
    def _store_value(self):
        with open(self.get_path(), 'w') as value_file:
            value_text = self._convert_to_text()
            value_file.write(value_text)
    
    def _convert_to_text(self) -> str:
        return str(self.value)

    def _load_value_from_file(self):
        if self._file_too_big():
            self._raise_file_too_big_exception()
        with open(self.get_path(), 'r') as position_file:
            value_text = position_file.read(self.max_bytes)
            self.value = self.get_value_from_text(value_text)

    def _file_too_big(self):
        file_size = os.path.getsize(self.get_path())
        return file_size > self.max_bytes

    def _raise_file_too_big_exception(self):
        raise InvalidFileSizeException(f'Storage file at path {self.get_path()} exceeded maximum size of'
        f'{self.max_bytes} bytes!'
        )

    def get_path(self):
        return os.path.join(self.directory, self.name)

    def _initialize_file_if_nonexistent(self):
        if self.exists():
            self.initialize()
    def exists(self):
        return not os.path.exists(self.get_path())
    def initialize(self):
        self._make_directory_if_nonexistent()
        initial_value = self._get_initial_value()
        self.set(initial_value)
    
    def _make_directory_if_nonexistent(self):
        _create_directory_if_nonexistent(self.directory)
    
    def delete(self):
        os.remove(self.get_path())

class JSONFile(StorageFile):
    def __init__(self, folder: str, name: str, *, max_bytes: int = DEFAULT_MAX_BYTES, initial_value = None, 
        default = None, cls = None, from_json = None):
        self.initial_value = initial_value
        self.converter = JSONConverter(from_json, to_json_function = default, to_json_class = cls)
        StorageFile.__init__(self, folder, name, max_bytes = max_bytes)

    def _convert_to_text(self) -> str:
        return self.converter.convert_object_to_json(self.value)
  
    def get_value_from_text(self, text: str):
        self.converter.convert_json_to_object(text)
    
    def _get_initial_value(self):
        return self.initial_value

class JSONConverter:
    def __init__(self, from_json, *, to_json_function = None, to_json_class = None):
        self.json_from_object_converter = JSONFromObjectConverter(to_json_function = to_json_function, to_json_class = to_json_class)
        self.object_from_json_converter = ObjectFromJSONConverter(from_json)

    def convert_object_to_json(self, value):
        return self.json_from_object_converter.convert_object(value)

    def convert_json_to_object(self, text):
        self.object_from_json_converter.convert_json(text)

class ObjectFromJSONConverter:
    def __init__(self, object_from_json):
        self.object_from_json = self._get_from_json_function(object_from_json)
    @classmethod
    def _get_from_json_function(cls, from_json):
        if cls._from_json_function_is_method(from_json):
            return cls._get_from_json_function_from_class(from_json)
        else:
            return from_json
    @classmethod
    def _get_from_json_function_from_class(cls, classname):
        return lambda value : classname.from_json(value)
    @classmethod
    def _from_json_function_is_method(cls, from_json):
        return cls._has_from_json_attribute(from_json) \
           and cls._has_callable_from_json_attribute(from_json)
    @classmethod
    def _has_from_json_attribute(cls, from_json):
        return hasattr(from_json, 'from_json')
    @classmethod
    def _has_callable_from_json_attribute(cls, from_json):
        return callable(from_json.from_json)

    def convert_json(self, text):
        json_value = self._convert_json_using_default_decoding(text)
        if _value_unavailable(self.object_from_json):
            return json_value
        return self.object_from_json(json_value)
    @classmethod
    def _convert_json_using_default_decoding(cls, text):
        return json.loads(text)

class JSONFromObjectConverter:
    def __init__(self, *, to_json_function, to_json_class):
        self.json_from_object = self._get_json_from_object_function(to_json_function, to_json_class)

    @classmethod
    def _get_json_from_object_function(cls, to_json_function, to_json_class):
        cls._raise_exception_if_invalid_json_from_object_argument_combination(to_json_function, to_json_class)
        if _value_provided(to_json_function):
            return cls._get_json_from_object_function_using_converter_function(to_json_function)
        if _value_provided(to_json_class):
            return cls._get_json_from_object_function_using_converter_class(to_json_class)
        return None
    @classmethod
    def _raise_exception_if_invalid_json_from_object_argument_combination(cls, to_json_function, to_json_class):
        if _values_provided(to_json_function, to_json_class):
            raise ValueError('JSONFile objects should not receive default and cls')
    @classmethod
    def _get_json_from_object_function_using_converter_function(cls, function):
        return lambda value : json.dumps(value, default = function)
    @classmethod
    def _get_json_from_object_function_using_converter_class(cls, converter_class):
        return lambda value : json.dumps(value, cls = converter_class)

    def convert_object(self, value) -> str:
        if _value_provided(self.json_from_object):
            return self.json_from_object(value)
        if self._value_has_encoder_method(value):
            return self._encode_using_encoder_method(value)
        return self._encode_using_json_default_encoding(value)
    @classmethod
    def _value_has_encoder_method(cls, value):
        return cls._value_has_to_json_attribute(value) \
           and cls._value_has_callable_to_json_attribute(value)
    @classmethod
    def _value_has_to_json_attribute(cls, value):
        return hasattr(value, 'to_json')
    @classmethod
    def _value_has_callable_to_json_attribute(cls, value):
        return callable(value.to_json)
    @classmethod
    def _encode_using_encoder_method(cls, value):
        json_object = value.to_json()
        return cls._encode_using_json_default_encoding(json_object)
    @classmethod
    def _encode_using_json_default_encoding(cls, value):
        return json.dumps(value)

def _value_provided(value):
    return value is not None
def _values_provided(*args):
    for value in args:
        if _value_unavailable(value):
            return False
    return True
def _value_unavailable(value):
    return value is None
    
class InvalidFileSizeException(Exception):
    pass

class MousePositionFile(StorageFile):
    def set_to_current_mouse_position(self):
        position = MousePosition.current()
        self.set(position)
    
    @classmethod
    def get_value_from_text(self, text: str):
        return MousePosition.from_text(text)
    
    def _get_initial_value(self):
        return MousePosition(0, 0)
    
class IntegerFile(StorageFile):
    @classmethod
    def get_value_from_text(self, text: str):
        return int(text)
    
    def _get_initial_value(self):
        return 0

class FloatFile(StorageFile):
    @classmethod
    def get_value_from_text(self, text: str):
        return float(text)
    
    def _get_initial_value(self):
        return 0.0
    
class StringFile(StorageFile):
    @classmethod
    def get_value_from_text(self, text: str):
        return text
    
    def _get_initial_value(self):
        return ''

class BooleanFile(StorageFile):
    @classmethod
    def get_value_from_text(self, text: str):
        return bool(text)
    
    def _get_initial_value(self):
        return False

    

    
