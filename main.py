# %%
# import pandas as pd
# import os

# %%
# %%
import streamlit as st
import pandas as pd
# # import numpy as np


# -- Set page config
apptitle = '战国策·君临'
st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

path_stage1 = "stage1.xlsx"
path_stage2 = "stage2.xlsx"


def get_damage_stage1(soldier,energy,stage_path):
    # energy = energy
    df = pd.read_excel(stage_path)
    df.index=  df['Unnamed: 0'].tolist()#.reset_index()
    del df['Unnamed: 0']

    if soldier > max(list(df)): # 如果超出了
        soldier = max(list(df))
    
    if energy > max(df.index):
        energy = max(df.index)

    return df[soldier][energy]

# %%
def get_dice_energy(throw_dice,battle_type):

    # throw_dice = [2,4,6]
    # battle_type = "野战"

    st.write(f'【投出骰子】 {throw_dice} 点 ')

    throw_dice = sorted(throw_dice,reverse=1)
    value_max,value_middle,value_min = throw_dice[0],throw_dice[1],throw_dice[2]
    #       野战	攻城战
    # 攻	上	    中
    # 守	中	    上
    if battle_type == "野战":
        # st.write('攻方取上,守方取中')
        energy_attack,energy_defense = value_max,value_middle
    if battle_type == "攻城战":
        # st.write('攻方取中,守方取上')
        energy_attack,energy_defense = value_middle,value_max
    st.write(f'【掷点士气】 攻方 {energy_attack} , 守方 {energy_defense}')
    return energy_attack,energy_defense


# 计算攻守伤害
def get_turn_1(soldier_attack,soldier_defense,battle_type,throw_dice,add_ene_attack,add_ene_defense,path_stage):
    # st.write(f'投掷出  { throw_dice }  点!')
    energy_attack,energy_defense = get_dice_energy(throw_dice,battle_type)
    st.write(f'【士气加成】 攻方 {add_ene_attack} , 守方 {add_ene_defense}')
    energy_attack,energy_defense = energy_attack+add_ene_attack,energy_defense+add_ene_defense
    damage_attack = get_damage_stage1(soldier_attack,energy_attack,path_stage)
    damage_defense = get_damage_stage1(soldier_defense,energy_defense,path_stage)
    return damage_attack,damage_defense



# 判断溃败
def check_kuibai(soldier,maintain):
    if maintain <= soldier * 0.5 :
        return 1
    else:
        return 0


# 计算是否被歼灭
def check_quanjian(maintain):
    if maintain <=0:
        return 1
    else:
        return 0



# %%
def get_routine(throw_dice,battle_type,soldier_attack,soldier_defense,path_stage,add_ene_attack=0,add_ene_defense=0):
    st.header(f'【攻方{soldier_attack}万人】  VS  【守方{soldier_defense}万人】'  )
    st.header(f'开启 {battle_type} !')
    st.write(f' ')

    # st.write(f'士气加成')
    # 算伤害
    damage_attack,damage_defense = get_turn_1(soldier_attack,soldier_defense,battle_type,throw_dice,add_ene_attack,add_ene_defense,path_stage)
    st.write(f' ')
    st.write(f'【攻方消灭】{damage_attack}万人 !')
    st.write(f'【守方消灭】{damage_defense}万人 !')
    # 算剩余兵力
    sol_maintain_attack = soldier_attack - damage_defense
    sol_maintain_defense = soldier_defense - damage_attack
    st.write(f'【剩余兵力】 攻方 {sol_maintain_attack} 万人 , 守方 {sol_maintain_defense} 万人')

    is_kuibai_attack = check_kuibai(soldier_attack,sol_maintain_attack)
    is_kuibai_defense = check_kuibai(soldier_defense,sol_maintain_defense)
    is_quanjian_attack = check_quanjian(sol_maintain_attack)
    is_quanjian_defense = check_quanjian(sol_maintain_defense)
    
    st.write(f' ')

    st.header(f'【战斗结果】')
    if (is_quanjian_attack==1) & (is_quanjian_defense==1):
        st.write('【同归于尽】 双方兵力清零 [同归于尽（都被全歼）]')
    elif (is_quanjian_attack==1) & (is_kuibai_defense == 1):
        st.write(f'攻方被全歼! 守方剩余{sol_maintain_defense}万人')
        st.write('触发原因 : [一方崩溃（但没死光），但另一方被全歼]')
    elif (is_quanjian_defense==1) & (is_kuibai_attack == 1):
        st.write(f'守方被全歼! 攻方剩余{sol_maintain_attack}万人')
        st.write('触发原因 : 一方崩溃（但没死光），但另一方被全歼')
    elif (is_quanjian_attack==1) & (is_kuibai_defense == 1):
        st.write(f'攻方{sol_maintain_attack}万人已崩溃 守方剩余{sol_maintain_defense}万人')
        st.write('触发团员 : [ 利守原则 ] 两方均崩溃（但都没死光）')
    elif is_quanjian_attack == 1:
        st.write(f'攻方被全歼! 守方剩余{sol_maintain_defense}万人')
    elif is_quanjian_defense == 1:
        st.write(f'守方被全歼! 攻方剩余{sol_maintain_attack}万人')
    elif is_kuibai_attack == 1:
        st.write(f'攻方{sol_maintain_attack}万人已崩溃 ! 守方剩余{sol_maintain_defense}万人')
    elif is_kuibai_defense == 1:
        st.write(f'守方{sol_maintain_defense}万人已崩溃 ! 攻方剩余{sol_maintain_attack}万人')
        if battle_type == '攻城战':
            st.write("触发规则 [ 攻城战守方永不崩溃 ]")
            st.write('【战斗不止】')
            st.write(f'【剩余兵力】 攻方 : {sol_maintain_attack} 万人 , 守方 : {sol_maintain_defense} 万人')
    else:
        st.write('【战斗不止】')
        st.write(f'【剩余兵力】 攻方 : {sol_maintain_attack} 万人 , 守方 : {sol_maintain_defense} 万人')

# %%
# throw_dice = [6,4,6]
# battle_type = "攻城战"
# soldier_attack =  4
# soldier_defense = 3
# add_ene_attack,add_ene_defense = 0,0
# from gwosc.api import fetch_event_json
with st.sidebar:
    st.image("logo.jpg",width = 250, caption= '薄荷猫版权所有')

    # with col0:
    map = st.selectbox('选择地图',
                                        ['地图1', '地图2'])
    if map =='地图1':
        path_stage = path_stage1
    if  map =='地图2':
        path_stage = path_stage2

    col1, col2 = st.columns(2)
    with col1:
        st.header("攻方")
        soldier_attack = st.slider("原始兵力-攻", 1, 12)
        add_ene_attack = st.slider("士气加成-攻", 0, 6)
    with col2:
        st.header("守方")
        soldier_defense = st.slider("原始兵力-守", 1, 12)
        add_ene_defense = st.slider("士气加成-守", 0, 6)

    col0, col163 = st.columns(2)
    with col0:
        battle_type = st.selectbox('选择作战类型',
                                            ['野战', '攻城战'])

    col4, col5, col6 = st.columns(3)
    with col4:
        value1=  st.text_input("投掷点数1")
    with col5:
        value2=  st.text_input("投掷点数2")
    with col6:
        value3=  st.text_input("投掷点数3")

        
    # jsoninfo = fetch_event_json(battle_type)
    # st.write('Mass 1:', battle_type, 'M$_{\odot}$')

    b = st.button("开始战斗")


if b == 1:
    throw_dice = [int(value1),int(value2),int(value3)]
    get_routine(throw_dice,battle_type,soldier_attack,soldier_defense,path_stage,add_ene_attack,add_ene_defense)

# import setuptools
# with open('requirements.txt', 'w') as f:
#     f.write(''.join(map(str, setuptools.find_packages())))
# st.title('Uber pickups in NYC')
# streamlit run .py
    