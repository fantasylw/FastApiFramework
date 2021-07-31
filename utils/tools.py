
# model转化为dict
def get_dict_for_model(model_data):
    """[根据model获取dict]

    Args:
        model_data ([mongodbModel]): [必须为model对象]

    Returns:
        [dict]: [字典]
    """    
    field_map = model_data._reverse_db_field_map
    model_dict = model_data.to_mongo().to_dict()
    data = {}
    for key in model_dict:
        data[field_map[key]] = model_dict[key]
    return data
