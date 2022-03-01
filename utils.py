"""
Utils

"""
def prefilter_items(data, item_features, take_n_popular=5000):
    # Уберем самые популярные товары (их и так купят)
    popularity = data.groupby('item_id')['user_id'].nunique().reset_index() / data['user_id'].nunique()
    popularity.rename(columns={'user_id': 'share_unique_users'}, inplace=True)
    
    top_popular = popularity[popularity['share_unique_users'] > 0.5].item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]
    
    # Уберем самые НЕ популярные товары (их и так НЕ купят)
    top_notpopular = popularity[popularity['share_unique_users'] < 0.01].item_id.tolist()
    data = data[~data['item_id'].isin(top_notpopular)]
    
    # Уберем товары, которые не продавались за последние 12 месяцев
    data = data[data['day'] < 366]
    
    # Уберем не интересные для рекоммендаций категории (department)
    # А что для нас не интересно?
    data = data[~data['item_id'].isin(item_features[item_features['department'] == 'GROCERY']['item_id'])] 
    
    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб. 
    data = data[data['sales_value'] * 75 > 60] # Посчитал, что прайс в долларах
    
    # Уберем слишком дорогие товары
    data = data[data['sales_value'] < data['sales_value'].quantile(0.975)]
    
    # Оставим топ 5000 товаров
    popularity = data.groupby('item_id')['quantity'].sum().reset_index()
    popularity.rename(columns={'quantity': 'n_sold'}, inplace=True)

    top_5000 = popularity.sort_values('n_sold', ascending=False).head(take_n_popular).item_id.tolist()
    data.loc[~data['item_id'].isin(top_5000), 'item_id'] = 999999
    
    return data
    
def postfilter_items(user_id, recommednations):
    pass