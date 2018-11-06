import yaml
import os


class ServiceGenerator(object):

    def __init__(self, path_to_config_file):
        self.path_to_config_file = path_to_config_file
        self.destination_main_directory = ""
        self.micro_service_name = ""
        self.current_destination_path = ""

    def generate_config_dictionary(self):
        """
        This function will create the config dictionary issue of a yaml file
        then return the dictionary
        :return: dic
        """
        config_file = open(self.path_to_config_file, "r", encoding="utf-8")
        config_dictionary = yaml.load(config_file.read())
        return config_dictionary

    def parse_config_dictionary(self):
        """
        This function get the config from yml file
        Then get the key in dic and start parse dic_config
        A function to create a dictionary or a file will be call, depend on type find
        :return:
        """
        # get config from yml file
        config_dictionary = self.generate_config_dictionary()
        # get all principal keys
        keys_list_from_dic_config = config_dictionary.keys()
        # generate the main directory
        self.generate_main_directory(config_dictionary)
        for key in keys_list_from_dic_config:
            print(key)
            if key == "microservicename":
                continue

            elif config_dictionary[key]["type"] == "file":
                self.current_destination_path = ""
                self.create_file(config_dictionary, key)

            elif config_dictionary[key]["type"] == "directory":
                self.create_directory(config_dictionary, key)

            else:
                print("LOG NOT A GOOD PARAMETER=>"+key)

    def generate_main_directory(self, config_dictionary):
        """
        This function generate the main directory
        :param config_dictionary: dic
        :return:
        """
        # stock the microservice's name in var
        self.micro_service_name = config_dictionary["microservicename"]
        # create the path to our main directory
        self.destination_main_directory = "./" + self.micro_service_name + "/"
        # generate main directory
        self.generate_directory("", self.destination_main_directory)

    @staticmethod
    def generate_directory(directory_name, destination_path):
        """
        This function will create a directory
        :param directory_name: str
        :param destination_path: str
        :return:
        """
        os.makedirs(destination_path+directory_name)

    @staticmethod
    def generate_file(file_name, destination_path):
        """
        This function will create a file
        :param file_name: str
        :param destination_path: str
        :return:
        """
        open(destination_path+file_name, "w+")

    def create_file(self, dic_config_file, file_name):
        """
        This function treat parameters before generate a file and call the function who will write in file
        :param file_name: str
        :param dic_config_file: dic
        :return:
        """
        file_name_and_extenstion = file_name + "." + dic_config_file[file_name]["extention"]
        if "contenu" in dic_config_file[file_name].keys():
            file_contents = dic_config_file[file_name]["contenu"]

        else:
            file_contents = ""

        if self.current_destination_path:
            self.generate_file(file_name_and_extenstion, self.current_destination_path)
            self.write_in_file(file_name_and_extenstion, self.current_destination_path, file_contents)

        else:
            self.generate_file(file_name_and_extenstion, self.destination_main_directory)
            self.write_in_file(file_name_and_extenstion, self.destination_main_directory, file_contents)

    def create_directory(self, dic_config_directory, directory_name):
        """
        This function will call the function to create a directory and the function to create the files in the directory
        :param dic_config_directory: dic
        :param directory_name: str
        :return:
        """
        self.generate_directory(directory_name, self.destination_main_directory)
        if "file" in dic_config_directory[directory_name]:
            # pass the directory path in var current_destination, this will be use in create file if need
            self.current_destination_path = self.destination_main_directory + directory_name + "/"
            for new_file in dic_config_directory[directory_name]["file"]:
                self.create_file(dic_config_directory[directory_name]["file"], new_file)

    def write_in_file(self, file_name, file_path, file_contents):
        """
        This function will write in a file
        :param file_name: str
        :param file_path: str
        :param file_contents: dic
        :return:
        """
        # hear we will treat the specific files exemple requirements, init, models
        # then all file pass in the "else"
        if "requirements" in file_name:
            if "dependances" in file_contents:
                self.requirements_writer(file_name, file_path, file_contents)

        elif "init" in file_name:
            if "export" in file_contents:
                self.init_writer(file_name, file_path, file_contents)

        elif "models" in file_name:
            self.models_writer(file_name, file_path, file_contents)

        else:
            if "import" in file_contents:
                self.import_writer(file_name, file_path, file_contents)

            if "main" in file_name:
                self.main_file_writer(file_name, file_path, file_contents)

            # create case for simple file
            # TODO delete list in import technique, list and dictionnary
            if "simple" in file_contents:
                self.simple_line_writer(file_name, file_path, file_contents)

            if "function" in file_contents:
                self.function_writer(file_name, file_path, file_contents)

    @staticmethod
    def requirements_writer(file_name, file_path, file_contents):
        """
        This function will write in requirements txt dependances
        :param file_name: str
        :param file_path: str
        :param file_contents: dic
        :return:
        """
        destination = file_path + file_name
        requirement_file = open(destination, "w")

        for dependance in file_contents["dependances"]:
            requirement_file.write(dependance + "\n")

    @staticmethod
    def init_writer(file_name, file_path, file_contents):
        """
        This function will write the init file
        :param file_name: str
        :param file_path: str
        :param file_contents: dic
        :return:
        """
        destination = file_path + file_name
        init_file = open(destination, "w")

        for dic_export in file_contents["export"]:
            for file_name_export, class_name_export in dic_export.items():
                init_file.write("from ." + file_name_export + " import " + class_name_export + "\n")

    @staticmethod
    def simple_line_writer(file_name, file_path, file_contents):
        """
        This function will write simply the line in a file
        :param file_name: str
        :param file_path: str
        :param file_contents: dic
        :return:
        """
        destination = file_path + file_name
        classic_file = open(destination, "a")

        for var, value in file_contents["simple"].items():
            # if we just want to write a line just put simple in key
            # elif we will write the line with key = value
            if var == "simply":
                classic_file.write(value + "\n")

            else:
                classic_file.write(var + " = " + value + "\n")

    @staticmethod
    def import_writer(file_name, file_path, file_contents):
        """
        This function will write all the import, a file require
        :param file_name: str
        :param file_path: str
        :param file_contents: dic
        :return:
        """
        destination = file_path + file_name
        current_file = open(destination, "w")
        for dic_import in file_contents["import"]:
            for module_name, class_name_import in dic_import.items():
                if module_name == "import":
                    current_file.write("import " + class_name_import + "\n")

                else:
                    current_file.write("from " + module_name + " import " + class_name_import + "\n")

    @staticmethod
    def function_writer(file_name, file_path, file_contents):
        """
        This function will write the class method inside the file
        :param file_name: str
        :param file_path: str
        :param file_contents: dic
        :return:
        """
        destination = file_path + file_name
        current_file = open(destination, "a")
        current_file.write("\nclass " + file_name[:-3] + "(object):\n")
        for function_name, function_dic in file_contents["function"].items():
            current_file.write(
                "\n    def " + function_name + "(self, " + ", ".join(function_dic["attributs"]) + "):" + "\n")
            current_file.write("        \"\"\"\n        " + function_dic["docstrings"] + "\n        \"\"\" \n")
            current_file.write("        pass\n")

    @staticmethod
    def models_writer(file_name, file_path, file_contents):
        """
        This function come to write in model file
        :param file_name: str
        :param file_path: str
        :param file_contents: dic
        :return:
        """
        destination = file_path + file_name
        current_file = open(destination, "a")
        # here we write in the file the basic import in a models.py file
        current_file.write("from config import Base, engine\n")
        current_file.write("from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table\n")
        current_file.write("from sqlalchemy.orm import relationship\n")

        for model in file_contents.values():
            for class_name, class_attr in model.items():
                # create the class name and his tablename
                current_file.write("\nclass " + class_name + "(Base):")
                current_file.write("\n    __tablename__ = '" + class_name.lower() + "'")

                # here we will parse the attributes of the class and create attributes line
                # for exemple if line = id we will create it after the classname
                # and add his parameters, unique, nullable
                for attr_name, attr_parameters in class_attr["attributs"].items():
                    list_parameters_builder = [attr_name+" = Column("]
                    if "attr_type" in attr_parameters.keys():
                        if attr_parameters["attr_type"] == "integer":
                            list_parameters_builder.append("Integer")

                        elif "str" in attr_parameters["attr_type"]:
                            str_length = attr_parameters["attr_type"].replace("str", "")
                            list_parameters_builder.append("String(" + str_length + ")")

                        elif attr_parameters["attr_type"] == "date":
                            list_parameters_builder.append("DateTime, default=datetime.datetime.utcnow()")

                    if "unique" in attr_parameters.keys():
                        if attr_parameters["unique"] == "true":
                            list_parameters_builder.append(", unique=True")

                        else:
                            list_parameters_builder.append(", unique=False")

                    if "nullable" in attr_parameters.keys():
                        if attr_parameters["nullable"] == "true":
                            list_parameters_builder.append(", nullable=True")

                        else:
                            list_parameters_builder.append(", nullable=False")

                    current_file.write("\n    " + "".join(list_parameters_builder) + ")")

        # here we write at the end of the file basic line who will create all the model in our database
        current_file.write("\nBase.metadata.create_all(engine)\n")

    @staticmethod
    def main_file_writer(file_name, file_path, file_contents):
        """
        This function will write in the main file of our service
        :param file_name: str
        :param file_path: str
        :param file_contents: dic
        :return:
        """
        destination = file_path + file_name
        current_file = open(destination, "a")

        # add necessary import for the project
        current_file.write("from flask import Flask\n")
        current_file.write("from flask_restful import api\n")
        current_file.write("from settings import *\n")
        current_file.write("from config import session\n")

        # add classic line for flask restful api project
        current_file.write("\napp = Flask(__name__)\n" +
                           "app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI\n" +
                           "api = Api(app)\n")

        # create managers in current app
        for manager in file_contents["managers"]:
            new_manager = (manager.replace("Manager", "")).lower()
            current_file.write("app." + new_manager + "_manager = " + manager + "(session)\n")

        # Create routes
        for route in file_contents["routes"]:
            current_file.write("api.add_resource(" + route["controller"] + ", '" + route["url"]+"')\n")

        # Write the classic at the end of the main file
        current_file.write("\nif __name__ == '__main__':\n    app.run(host='0.0.0.0', port=5000, debug=True)")
