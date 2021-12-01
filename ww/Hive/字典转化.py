"""
author:cai
project:learn_python
date:2021/11/29
"""
# coding=utf8

table_strategy = {
    'dws.dws_pms_transaction_stat_df': ['keep_last_n_by_dt_hotel', {'fl': "~df['dt'].str.endswith('-01')", 'n': 7}],
    'edw.t_edw_ors_stay_record_act_ful': ['keep_last_n', {'fl': "~df['dt'].str.endswith('-01')", 'n': 30}],
    'tmp.t_tmp_upsell_pod_update_inc': ['keep_last_n', {'n': 300}],
}

if __name__ == '__main__':
    for k, v in table_strategy.items():
        table_name = k
        partition_type = 1 if v[0] == 'keep_last_n' else 2
        save_dd_01_yn = 'N' if v[1].get('fl', 'NoneType') == 'NoneType' else 'Y'
        save_num = v[1].get('n')

        print(f"INSERT INTO test.hive_data_life_cycle_management (table_name, partition_type, save_dd_01_yn, "
              f"save_partition_num) VALUES ('{table_name}',{partition_type},'{save_dd_01_yn}',{save_num}); ")
