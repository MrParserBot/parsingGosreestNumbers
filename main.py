import requests
import settings

def get_request(number):
    # Делаем запрос к api
    try:
        params_req = {"get" : "num", "format" : "json", "num" : number}
        req = requests.get(settings.url_api, params=params_req)
        res = req.json()
        return res["0"]["operator"]
    except Exception as e:
        print(e)
        return "no data"
    
def get_data_from_file():
    # Получаем данные из файла с номерами
    with open(settings.name_file, encoding="utf-8") as f:
        list_data = []
        for elem in f.readlines():
            list_data.append([elem.split(',')[0], elem.split(',')[1].replace('\n','')])
        return list_data

def check_data(data):
    # Проверяем совпадает ли данные из базы с госреестром
    count_true_data = 0
    count_error_data = 0
    result_list = []
    for elem in data:
        res = get_request(elem[0])
        flag_position = 0        
        if res == elem[1]:
            count_true_data += 1
            flag_position = 1
        elif res == "no data":
            count_error_data += 1
            flag_position = 2
        result_list.append(",".join([elem[0], elem[1], res, str(flag_position)]))
    print(f"Checked phones: {len(data)} Is true: {count_true_data} Is false: {len(data) - count_true_data - count_error_data} Undefined: {count_error_data}")
    return result_list 

def main():
    data_from_file = get_data_from_file()
    result = check_data(data_from_file)
    with open('result.txt', 'a+', encoding="utf-8") as f:
        for elem in result:
            f.write(elem + '\n')

if __name__ == "__main__":
    main()