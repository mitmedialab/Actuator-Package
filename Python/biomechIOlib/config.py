import yaml

# def load(filepath, modeltype, datatype1, datatype2):
#     with open(filepath, "r") as file_descriptor:
#         data = yaml.load(file_descriptor)
#
#     model_cfg = data.get(modeltype)
#     data_cfg2 = data.get(datatype2)
#     data_cfg1 = data.get(datatype1)
#
#     return model_cfg, data_cfg1, data_cfg2


def load_config(filepath, dtype):
    with open(filepath, "r") as file_descriptor:
        data = yaml.load(file_descriptor)

    data = data.get(dtype)
    # data_cfg2 = data.get(datatype2)
    # data_cfg1 = data.get(datatype1)

    return data
