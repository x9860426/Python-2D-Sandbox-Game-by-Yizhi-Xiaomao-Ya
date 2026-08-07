# F1帮助页面管理类

class HelpPageManager:
    """
    管理游戏帮助页面的内容和逻辑
    集中控制帮助页面的所有文本内容
    """
    
    def __init__(self):
        # 初始化帮助内容
        self.help_content = self._create_help_content()
    
    def _create_help_content(self):
        """创建帮助页面的内容结构"""
        return [
            ["部分按键说明", [
                "F1 - 打开/关闭,帮助说明页面",
                "F2 - 打开/关闭,提升玩家属性页面",
                "F3 - 打开/关闭,创造背包页面",  
                "F3 - 打开/关闭,开发者调试页面",
                "c - 打开/关闭,合成页面",
                "b - 打开/关闭,背包页面",                                                                
                "ESC - 关闭页面和打开菜单页面",             
                "鼠标左键 - 挖掘方块和攻击",
                "鼠标右键 - 放置方块和交互",
                "数字键1-8 - 切换快捷栏物品",
                "鼠标滚轮 - 切换物品或滚动帮助页面",
                "a,d,空格 - 移动玩家跳跃",
                
            ]],
            ["游戏特色", [
                "挖掘方块击败生物获取资源",
                "可以合成物品",
                "探索随机生成的世界",
                "收集星星提升属性或复活",
                "时间系统",
                "武器装备系统",
                "怪物系统"
            ]],

        ]
    
    def get_help_content(self):
        """获取帮助页面内容"""
        return self.help_content
    
    def update_content(self, new_content):
        """更新帮助页面内容"""
        self.help_content = new_content
    
    def add_section(self, section_title, section_items):
        """添加新的帮助章节"""
        self.help_content.append([section_title, section_items])
    
    def remove_section(self, section_index):
        """移除指定索引的章节"""
        if 0 <= section_index < len(self.help_content):
            del self.help_content[section_index]
            return True
        return False
    
    def modify_section(self, section_index, new_title=None, new_items=None):
        """修改指定索引的章节"""
        if 0 <= section_index < len(self.help_content):
            if new_title is not None:
                self.help_content[section_index][0] = new_title
            if new_items is not None:
                self.help_content[section_index][1] = new_items
            return True
        return False

# 创建全局实例供其他模块使用
help_manager = HelpPageManager()