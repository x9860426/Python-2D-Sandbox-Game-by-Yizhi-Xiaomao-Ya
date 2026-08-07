import os
import json

class SaveHelper:
    # 装备基础属性值
    头盔_伤害 = 0
    头盔_防御 = 0
    盔甲_防御 = 0
    靴子_摔伤 = 0
    靴子_防御 = 0
    特殊_移速 = 0
    特殊_防御 = 0
    
    @staticmethod
    def load_save_data(file_name):
        """加载存档数据，支持文件夹形式和传统JSON文件形式"""
        # 构建存档路径
        save_folder_path = os.path.join(os.getcwd(), '存档', file_name)

        # 检查是文件夹还是文件
        if os.path.isdir(save_folder_path):
            # 文件夹形式存档：读取多个数据文件
            save_data = {}
            
            try:
                # 读取地形数据
                terrain_file = os.path.join(save_folder_path, 'terrain_data.json')
                if os.path.exists(terrain_file):
                    with open(terrain_file, 'r', encoding='utf-8') as f:
                        save_data['terrain'] = json.load(f)
                
                # 读取玩家数据
                player_file = os.path.join(save_folder_path, 'player_data.json')
                if os.path.exists(player_file):
                    with open(player_file, 'r', encoding='utf-8') as f:
                        save_data['player'] = json.load(f)
                
                # 读取世界数据
                world_file = os.path.join(save_folder_path, 'world_data.json')
                if os.path.exists(world_file):
                    with open(world_file, 'r', encoding='utf-8') as f:
                        save_data['world'] = json.load(f)
                
                return save_data
            except Exception as e:
                print(f"加载文件夹存档失败: {e}")
                return None
        else:
            # 传统JSON文件形式
            save_path = os.path.join('存档', file_name)
            if not save_path.endswith('.json'):
                save_path += '.json'
                
            if os.path.exists(save_path):
                try:
                    with open(save_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception as e:
                    print(f"加载存档失败: {e}")
            return None