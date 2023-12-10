import pandas as pd 
import json

from src.classes.base_models import ModelProduct

class IntegrateApiDataBase:
    def __init__(self) -> None:
        self.dict_operators =  { 
        "eq" : "=", 
        "lt" : "<" ,
        "lte" : "<=", 
        "gt" : ">" ,
        "gte" : ">=" 
        }

    def params_to_dict(self, params):
        dict_params = vars(params)
        dict_params = {key: value for key, value in dict_params.items() if value is not None}
        dict_params = dict(dict_params)
        return dict_params
    
    def generate_consult_where(self, dict_params):
        ls_consults = []
        for key, value in dict_params.items():
            if not isinstance(value, dict):
                value_consult = f"'{value}'"
                consult_line  = f"{key} = {value_consult}"
            else:
                operator = list(value.keys())[0]
                operator = self.dict_operators.get(operator, '=')
                value_number = list(value.values())[0]
                value_consult = f"{operator} {value_number}"
                consult_line = f"{key} {value_consult}"
            ls_consults.append(consult_line)
        consult = ' and '.join(ls_consults)
        if len(consult) > 2:
            consult = f"where {consult}"
        return consult
    
    def generate_select(self, table_name, dict_params, page,  page_size):
        consult_start = f'select * from {table_name}'
        consult_where = self.generate_consult_where(dict_params)
        consult_limit = f"limit {page_size} OFFSET {((page -1) * page_size)}"
        consult_select = f"{consult_start} {consult_where} {consult_limit}"
        return consult_select 
    
    def generate_select_count(self, table_name, dict_params):
        consult_start = f"select count(*) from {table_name}"
        consult_where = self.generate_consult_where(dict_params)
        consult_count_select = f"{consult_start} {consult_where}"
        return consult_count_select
    
    def generate_delete(self, table_name, dict_params):
        consult_start = f"delete from {table_name}"
        consult_where = self.generate_consult_where(dict_params)
        consult_delete = f"{consult_start} {consult_where}"
        return consult_delete
    
    def generate_update_set(self, dict_params):
        ls_consults = []
        for key, value in dict_params.items():
            if not str(value).isnumeric():
                value_consult = f"'{value}'"
                consult_line  = f"{key} = {value_consult}"
            else:
                value_consult = f"{value}"
                consult_line  = f"{key} = {value_consult}"
            ls_consults.append(consult_line)
        consult = ' , '.join(ls_consults)
        if len(consult) > 2:
            consult = f"SET {consult}"
        return consult
    
    def generate_update(self, table_name, dict_new_register, query):
        consult_start = f"UPDATE {table_name}"
        consult_set = self.generate_update_set(dict_new_register)
        consult_where = self.generate_consult_where(query)
        consult_update = f"{consult_start} {consult_set} {consult_where}"
        return consult_update

    
    def generate_response_paginate(self, dataframe_response, page, page_size, number_registers):
        response = {}
        json_return = dataframe_response.to_json(orient="records")
        json_parsed = json.loads(json_return)

        response['items'] = json_parsed
        response['total pages'] = (number_registers // page_size) + 1
        response['page'] = page 
        response['size'] = page_size
        return response 
    
    def list_params_to_dict(self, ls_params):
        ls_treated_params = []
        for element in ls_params:
            ls_treated_params.append(self.params_to_dict(element))
        return ls_treated_params
    
    def convert_map_string(self, text_parameter):
        text_parameter = str(text_parameter)
        if text_parameter.isnumeric():
            return {'eq' : int(text_parameter)}  
        elif not text_parameter.isnumeric() and '.' in text_parameter:
            ls_param = text_parameter.split('.')
            operator = ls_param[0]
            value = ls_param[1]
            if value.isnumeric():
                operator_value = self.dict_operators.get(operator)
                if operator_value == None:
                    return {'eq' : int(value)}
                else:
                    return {operator : int(value)}
            else:
                return None
        else:
            return None
    
    def convert_get_params_to_format_dict(self, get_parameter):
        ls_map_fields = []
        for field, field_type in ModelProduct.__annotations__.items():
            if str(field_type) != "<class 'str'>":
                ls_map_fields.append(field)
        dict_result = {}
        for key, value in get_parameter.items():
            if value != key:
                if key in ls_map_fields:
                    value_converted = self.convert_map_string(value)
                    dict_result[key] = value_converted
                else:
                    dict_result[key] = value
        return dict_result
    
    
    
    
