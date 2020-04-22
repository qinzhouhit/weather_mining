import requests
import demjson
import csv
import collections


def weather_mine():
    '''
    city names and related ID can be obtained by visiting:
    http://tianqi.2345.com/wea_history/54511.htm
    By clicking different city names, you can find the ID in the URL.
    :return: a csv with header
    '''
    # city2code = {'nj': '58238','wx': '58354','cs': '57687','sz': '59493',
    #              'bj':'54511','wh':'57494','cd':'56294','sh':'58362'
    #             }
    city2code = {'nj': '58238','wx': '58354','cs': '57687','sz': '59493'}
    for city in city2code:
        for year in [2017]: # target year
            months = ["%d%02d"%(year, m+1) for m in range(12)]
            todo_urls = [f"http://tianqi.2345.com/t/wea_history/js/{month}/"+city2code[city]+f"_{month}.js" \
                         for month in months]
            # print (todo_urls)

            # get the data
            datas = []
            for url in todo_urls:
                r = requests.get(url)
                if r.status_code != 200:
                    raise Exception()
                data_tmp = r.text.lstrip("var weather_str=").rstrip(";")
                datas.append(data_tmp)

            # parse the data
            all_data = []
            for data in datas:
                tqInfos = demjson.decode(data)["tqInfo"]
                all_data.extend([x for x in tqInfos if len(x) > 0])

            # store the data to csv
            with open(city+"_yearly_weather.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                cols = ['ymd', 'bWendu', 'yWendu', 'tianqi', \
                        'fengxiang', 'fengli', 'aqi', 'aqiInfo', 'aqiLevel']
                writer.writerow(cols)
                for data in all_data:
                    writer.writerow([data[col] for col in cols])

if __name__ == "__main__":
    weather_mine()
