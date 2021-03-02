from ceshi.Hotel_Info import main

# file_path = 'D:\工作\需求\hotel_info 1030.xlsx'
# sheet_name = ['Hotel Info', 'Hotel Wing Mapping']
# table_name = ['odc.odc_file_hotel_info_df', 'odc.odc_file_hotel_wing_df']


# file_path = 'D:\工作\需求\Room Mapping Relationship_dev 20191105.xlsx'
# sheet_name = ['OLAP Results']
# table_name = ['odc.odc_file_hotel_info_df']


# file_path='D:\工作\需求\market segment V3.2.xlsx'
# sheet_name=['sheet']
# table_name=['aaa']

# file_path = 'D:\工作\需求\Country - Continent - Dev.xlsx'
# sheet_name = ['OLAP Results']
# table_name = ['odc.odc_file_hotel_info_df']




file_path = 'D:\工作\手工文件\hotel_info 0721 v2.0.xlsx'
sheet_name = ['Hotel Info']
table_name = ['odc.odc_file_hotel_info_df']


main(file_path,sheet_name,table_name)

