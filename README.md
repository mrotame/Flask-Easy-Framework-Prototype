# Flask Easy Framework Prototype

### Description
This project has been used by me to build an agile Rest API framework by using Flask, SQLAlchemy, and Marshmallow.
The documentation of this project will be written after finishing the first stable version of the project

### Achieved so far:

* **Generic API View:** *The generic API View is an abstract/mixin Flask View class that has many features like automatic dispatch_request to choose the class method from the request HTTP method, besides having default CRUD options by simply defining the "serializer", "model" and the "field_lookup" attributes inside the class* 
* **Base Model** *The base DB-model uses the default SQLAlchemy Model class to specify some default configurations like some default fields, and self-saving, self-selecting, self-updating, and self-deleting (hard or soft deleting methods included)*
* **Base Serializers** * The base serializer class is an abstract factory class that generates and returns Marshmallow serializers schemas based. By defining specific schemas like PostMeta and PatchMeta that will have different Serializers for the POST and PATCH request methods or a general Meta class for all HTTP methods that don't have a specific Meta class
* **User Module**: *The base user model integrates the Authentication module, Serializer Module, and the Model Module among the Flask Globals and Werkzeug LocalProxy to validate and automatically integrate any authenticated request to the respective user, and can be used from the current_user across the entire application*
*  **Auth Module**: *The auth module control by generating and verifying user credentials and session tokens by many methods. (like default session models from database, or database-less JWT sessions)
