from ServiceGenerator import ServiceGenerator

service_generator = ServiceGenerator("config_exemple.yml")

if __name__ == "__main__":
    service_generator.parse_config_dictionary()
