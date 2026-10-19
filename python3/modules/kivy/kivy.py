import kivy
# kivy's new way of declaring propereties whin a class:
# before


class MyClass(object):
    def __init__(self):
        super(MyClass, self).__init__()
        self.numeric_var = 1


# new:


class MyClass(EventDispatcher):
    numeric_var = NumericProperty(1)


"""
These properties implement the Observer pattern. They help you to:
Easily manipulate widgets defined in the Kv language
Automatically observe any changes and dispatch functions/code accordingly
Check and validate values
Optimize memory management
To use them, you have to declare them at class level. That is, directly in the class, not in any method of the class. A property is a class attribute that will automatically create instance attributes. Each property by default provides an on_<propertyname> event that is called whenever the property’s state/value changes.
Kivy provides the following properties:
NumericProperty, StringProperty, ListProperty, ObjectProperty, BooleanProperty, BoundedNumericProperty, OptionProperty, ReferenceListProperty, AliasProperty, DictProperty, VariableListProperty, ConfigParserProperty, ColorProperty
For an in-depth explanation, take a look at Properties.
"""
