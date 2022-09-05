import datetime as dt
import pandas as pd
from libs.mysqldb import BaseTable, CarsTable, PriceHistoryTable, FeaturesTable, PhotosTable

def get_available_makes() -> list[str]:
    SQL = f"SELECT DISTINCT make FROM {CarsTable.TABLE_NAME}"
    df = CarsTable.get_data_from_query(SQL)
    
    return df['make'].tolist()

def get_make_distinct(make_list: list[str], column: str) -> list:
    SQL = (f"""
        SELECT DISTINCT {column} 
        FROM {CarsTable.TABLE_NAME}
        WHERE 1 = 1
    """
    + (f""" AND make IN ({', '.join(["'"+m+"'" for m in make_list])})""" if 'All' not in make_list else ''))
    
    df = CarsTable.get_data_from_query(SQL)
    
    return df[column].sort_values().tolist()

def get_model_distinct(model_list: list[str], column: str) -> list:
    SQL = (f"""
        SELECT DISTINCT {column} 
        FROM {CarsTable.TABLE_NAME}
        WHERE 1 = 1
    """
    + (f""" AND model IN ({', '.join(["'"+m+"'" for m in model_list])})""" if 'All' not in model_list else ''))
    
    df = CarsTable.get_data_from_query(SQL)
    
    return df[column].sort_values().tolist()

def get_model_min_max_model_mileage(model_list: list[str]) -> tuple[int]:
    SQL = (f"""
        SELECT
            MIN(mileage) as min_mileage,
            MAX(mileage) as max_mileage
        FROM {CarsTable.TABLE_NAME}
        WHERE 1 = 1
    """
    + (f""" AND model IN ({', '.join(["'"+m+"'" for m in model_list])})""" if 'All' not in model_list else ''))
    
    df = CarsTable.get_data_from_query(SQL)
    
    return df['min_mileage'].iloc[0], df['max_mileage'].iloc[0]

def get_model_min_max_price(model_list: list[str]) -> tuple[int]:
    SQL = (f"""
        SELECT
            MIN(pht.price) as min_price,
            MAX(pht.price) as max_price
        FROM {CarsTable.TABLE_NAME} AS ct
        INNER JOIN {PriceHistoryTable.TABLE_NAME} AS pht
        ON ct.id = pht.id
        WHERE 1 = 1
    """
    + (f""" AND ct.model IN ({', '.join(["'"+m+"'" for m in model_list])})""" if 'All' not in model_list else ''))
    
    df = BaseTable.get_data_from_query(SQL)
    
    return int(df['min_price'].iloc[0]), int(df['max_price'].iloc[0])

def get_model_features(model_list: list[str]) -> list[str]:
    SQL = (f"""
        SELECT
            DISTINCT(ft.feature) as feature
        FROM {CarsTable.TABLE_NAME} AS ct
        INNER JOIN {FeaturesTable.TABLE_NAME} AS ft
        ON ct.id = ft.id
        WHERE 1 = 1
    """
    + (f""" AND ct.model IN ({', '.join(["'"+m+"'" for m in model_list])})""" if 'All' not in model_list else ''))
    
    df = BaseTable.get_data_from_query(SQL)
    
    return df['feature'].sort_values().tolist()

def get_summary_stats_data(
        make_list: list, 
        model_list: list, 
        color_list: list,
        interior_color_list: list,
        power_list: list,
        drive_type_list: list,
        features_list: list,
        mileage_range: list,
        price_range: list,
        start_date: dt.date,
        end_date: dt.date) -> pd.DataFrame:
    
    SQL = (f"""
    SELECT 
        DATE(ph.datetime) as date,
        AVG(ph.price) as average_price,
        MIN(ph.price) as min_price,
        MAX(ph.price) as max_price,
        COUNT(DISTINCT(ct.id)) as count_offers
    FROM {CarsTable.TABLE_NAME} AS ct
    INNER JOIN {PriceHistoryTable.TABLE_NAME} AS ph
        ON ct.id = ph.id
    """
    + (f"""
    INNER JOIN (
        SELECT 
            id
        FROM {FeaturesTable.TABLE_NAME}
        WHERE feature IN ({', '.join(["'"+f+"'" for f in features_list])})
        GROUP BY id
        HAVING COUNT(feature) = {len(features_list)}
    ) as features
    ON ct.id = features.id
    """ if features_list else '')
    + (f""" WHERE ct.registration BETWEEN '{start_date}' AND '{end_date}'""")
    + (f""" AND ct.mileage BETWEEN {mileage_range[0]} AND {mileage_range[1]}""")
    + (f""" AND ph.price BETWEEN {price_range[0]} AND {price_range[1]}""")
    + (f""" AND ct.make IN ({', '.join(["'"+m+"'" for m in make_list])})""" if 'All' not in make_list else '')
    + (f""" AND ct.model IN ({', '.join(["'"+m+"'" for m in model_list])})""" if 'All' not in model_list else '')
    + (f""" AND ct.color IN ({', '.join(["'"+m+"'" for m in color_list])})""" if 'All' not in color_list else '')
    + (f""" AND ct.interior_colour IN ({', '.join(["'"+m+"'" for m in interior_color_list])})""" if 'All' not in interior_color_list else '')
    + (f""" AND ct.power IN ({', '.join(["'"+str(m)+"'" for m in power_list])})""" if 'All' not in power_list else '')
    + (f""" AND ct.drive_type IN ({', '.join(["'"+m+"'" for m in drive_type_list])})""" if 'All' not in drive_type_list else '')
    + (""" GROUP BY DATE(datetime)
        ORDER BY 1 DESC""")   
    )

    df = BaseTable.get_data_from_query(SQL)

    return df

def get_latest_cars_data(
        make_list: list, 
        model_list: list, 
        color_list: list,
        interior_color_list: list,
        power_list: list,
        drive_type_list: list,
        features_list: list,
        mileage_range: list,
        price_range: list
        ) -> pd.DataFrame:

    SQL = (f"""
    SELECT 
        ct.*,
        latest_records.price
    FROM {CarsTable.TABLE_NAME} as ct
    INNER JOIN (
        SELECT 
            id,
            price
        FROM {PriceHistoryTable.TABLE_NAME}
        WHERE DATE(datetime) = (SELECT MAX(DATE(datetime)) FROM {PriceHistoryTable.TABLE_NAME})
        ) as latest_records
    ON ct.id = latest_records.id
    """
    + (f"""
    INNER JOIN (
        SELECT 
            id
        FROM {FeaturesTable.TABLE_NAME}
        WHERE feature IN ({', '.join(["'"+f+"'" for f in features_list])})
        GROUP BY id
        HAVING COUNT(feature) = {len(features_list)}
    ) as features
    ON ct.id = features.id
    """ if features_list else '')
    + (f""" WHERE ct.mileage BETWEEN {mileage_range[0]} AND {mileage_range[1]}""")
    + (f""" AND latest_records.price BETWEEN {price_range[0]} AND {price_range[1]}""")
    + (f""" AND ct.make IN ({', '.join(["'"+m+"'" for m in make_list])})""" if 'All' not in make_list else '')
    + (f""" AND ct.model IN ({', '.join(["'"+m+"'" for m in model_list])})""" if 'All' not in model_list else '')
    + (f""" AND ct.color IN ({', '.join(["'"+m+"'" for m in color_list])})""" if 'All' not in color_list else '')
    + (f""" AND ct.interior_colour IN ({', '.join(["'"+m+"'" for m in interior_color_list])})""" if 'All' not in interior_color_list else '')
    + (f""" AND ct.power IN ({', '.join(["'"+str(m)+"'" for m in power_list])})""" if 'All' not in power_list else '')
    + (f""" AND ct.drive_type IN ({', '.join(["'"+m+"'" for m in drive_type_list])})""" if 'All' not in drive_type_list else '')
    )

    df = BaseTable.get_data_from_query(SQL)

    return df

def get_car_price_history(car_id: str) -> list:
    SQL = f"""
        SELECT 
            DATE(datetime) as date,
            AVG(price) as price
        FROM {PriceHistoryTable.TABLE_NAME}
        WHERE id = '{car_id}'
        GROUP BY 1
    """
    
    df = PriceHistoryTable.get_data_from_query(SQL)
    
    return df.sort_values('date')

