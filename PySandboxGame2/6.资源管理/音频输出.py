import pygame
import os
import sys
import json

# 初始化pygame的音频模块
pygame.mixer.init()

class AudioManager:
    # 单例模式实现
    _instance = None
    
    def __new__(cls):
        """确保只有一个音频管理器实例"""
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        # 防止重复初始化
        if hasattr(self, '_initialized') and self._initialized:
            return
            
        # 存储所有加载的音频
        self.sounds = {}
        # 存储正在播放的音效通道
        self.playing_channels = {}
        # 获取当前目录，兼容EXE打包模式和脚本运行模式
        # 判断程序是否被打包为EXE
        is_frozen = getattr(sys, 'frozen', False)
        if is_frozen:
            # EXE模式：使用sys._MEIPASS获取资源所在目录
            self.script_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        else:
            # 脚本模式：获取项目根目录（向上两级，因为音频输出.py在6.资源管理文件夹中）
            self.script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 音频文件夹路径（不使用os.chdir，避免影响其他模块）
        self.audio_folder = os.path.join(self.script_dir, '资源', '音效')
        
        # 音效设置
        self.sound_enabled = True  # 默认启用音效
        self.music_enabled = True  # 默认启用音乐
        self.volume = 0.83  # 默认音量（83%）
        # 是否已加载所有音频的标志
        self._all_audio_loaded = False
        
        # 加载设置
        self.load_settings()
        
        # 标记初始化完成
        self._initialized = True
        
        print("音频管理器初始化完成")
        
        print(f"当前工作目录: {os.getcwd()}")
        print(f"音频文件夹相对路径: {self.audio_folder}")
        print(f"音频文件夹完整路径: {os.path.abspath(self.audio_folder)}")
        print(f"音效开关状态: {'开启' if self.sound_enabled else '关闭'}")
        print(f"音量设置: {int(self.volume * 100)}%")
    
    def load_settings(self):
        """从设置_数据库.json加载音效和音乐设置"""
        try:
            # 设置文件路径
            settings_file = os.path.join(self.script_dir, "设置_数据库.json")
            
            if os.path.exists(settings_file):
                with open(settings_file, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    # 读取音效开关设置
                    if "音效开关" in settings:
                        self.sound_enabled = settings["音效开关"]
                    # 读取音乐开关设置
                    if "音乐开关" in settings:
                        self.music_enabled = settings["音乐开关"]
                    # 读取音量设置（将0-100的整数转换为0.0-1.0的浮点数）
                    if "音量" in settings:
                        self.volume = max(0.0, min(1.0, settings["音量"] / 100.0))
                    print(f"成功从{settings_file}加载设置")
            else:
                print(f"警告: 未找到设置文件{settings_file}，使用默认设置")
        except Exception as e:
            print(f"加载设置时出错: {str(e)}，使用默认设置")
    
    def load_all_audio(self, loading_window=None):
        """加载音频文件夹中的所有音频文件
        
        参数:
            loading_window: 可选，加载窗口实例，用于显示加载进度和具体文件名
        
        返回:
            bool: 是否成功加载至少一个音频文件
        """
        # 检查是否已经加载过所有音频，如果是则直接返回
        if self._all_audio_loaded and len(self.sounds) > 0:
            print("音频资源已加载，无需重复加载")
            return True
            
        if not os.path.exists(self.audio_folder):
            print(f"错误: 音频文件夹 '{self.audio_folder}' 不存在!")
            return False
        
        # 支持的音频格式
        supported_formats = ['.mp3', '.wav', '.ogg', '.flac']
        loaded_count = 0
        failed_count = 0
        
        # 先获取所有音频文件列表以计算总数
        audio_files = []
        for filename in os.listdir(self.audio_folder):
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext in supported_formats:
                audio_files.append(filename)
        
        total_files = len(audio_files)
        print(f"开始加载音频文件... 总计: {total_files} 个文件")
        
        # 遍历音频文件列表
        for index, filename in enumerate(audio_files):
            # 构建完整的文件路径
            file_path = os.path.join(self.audio_folder, filename)
            # 获取音频名称（不包含扩展名）
            sound_name = os.path.splitext(filename)[0]
            
            # 检查音频是否已经加载，如果已加载则跳过
            if sound_name in self.sounds:
                print(f"✓ 已加载: {filename}")
                loaded_count += 1
                continue
            
            try:
                # 加载音频文件
                sound = pygame.mixer.Sound(file_path)
                self.sounds[sound_name] = sound
                print(f"✓ 成功加载: {filename}")
                loaded_count += 1
                
                # 更新加载窗口
                if loading_window and total_files > 0:
                    # 计算相对进度（0-100%）
                    relative_progress = ((index + 1) / total_files) * 100
                    # 映射到主程序中分配的音频加载进度范围（10-20%）
                    progress = 10 + int((relative_progress / 100) * 10)
                    # 限制进度在10-20之间
                    progress = max(10, min(20, progress))
                    loading_window.update_progress(progress, f"正在加载音频:{filename}")
                    
                    # 处理事件以防止界面冻结
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
            except Exception as e:
                print(f"✗ 加载失败: {filename}, 错误: {str(e)}")
                failed_count += 1
        
        # 标记已加载所有音频
        self._all_audio_loaded = True
        print(f"音频加载完成! 成功: {loaded_count}, 失败: {failed_count}, 总计: {loaded_count + failed_count}")
        return loaded_count > 0
    
    def play_sound(self, sound_name, volume=None, loop=False):
        """
        播放指定名称的音效
        参数:
            sound_name: 音频名称（不包含扩展名）
            volume: 音量(0.0-1.0)，如果为None则使用默认音量
            loop: 是否循环播放，默认为False
        返回:
            bool: 播放是否成功
        """
        # 特殊处理：神秘音乐受音乐开关控制，不受音效开关控制
        if sound_name == "神秘音乐":
            if not self.music_enabled:
                return False
        else:
            # 其他音效受音效开关控制
            if not self.sound_enabled:
                return False
        
        # 检查音频是否已加载
        if sound_name not in self.sounds:
            print(f"警告: 音频 '{sound_name}' 未加载!")
            return False
        
        # 设置音量
        final_volume = self.volume if volume is None else volume
        final_volume = max(0.0, min(1.0, final_volume))
        
        # 设置并播放音频
        sound = self.sounds[sound_name]
        sound.set_volume(final_volume)
        
        # 确定循环参数
        loop_count = -1 if loop else 0
        
        # 播放音频并记录通道
        channel = sound.play(loops=loop_count)
        if channel is not None:
            self.playing_channels[sound_name] = channel
        
        return True
        
    def play_sound_loop_when_finished(self, sound_name, volume=None):
        """
        播放指定名称的音效，播放完成后再重新播放（播放完在播放）
        参数:
            sound_name: 音频名称（不包含扩展名）
            volume: 音量(0.0-1.0)，如果为None则使用默认音量
        返回:
            bool: 播放是否成功
        """
        # 特殊处理：神秘音乐受音乐开关控制，不受音效开关控制
        if sound_name == "神秘音乐":
            if not self.music_enabled:
                return False
        else:
            # 其他音效受音效开关控制
            if not self.sound_enabled:
                return False
        
        # 检查音频是否已加载
        if sound_name not in self.sounds:
            print(f"警告: 音频 '{sound_name}' 未加载!")
            return False
        
        # 设置音量
        final_volume = self.volume if volume is None else volume
        final_volume = max(0.0, min(1.0, final_volume))
        
        # 设置音频
        sound = self.sounds[sound_name]
        sound.set_volume(final_volume)
        
        # 如果音频不在播放中，则播放一次
        if sound_name not in self.playing_channels or not self.playing_channels[sound_name].get_busy():
            channel = sound.play(loops=0)  # 只播放一次
            if channel is not None:
                self.playing_channels[sound_name] = channel
        
        return True
    
    def is_playing(self, sound_name):
        """
        检查指定名称的音频是否正在播放
        参数:
            sound_name: 音频名称（不包含扩展名）
        返回:
            bool: 如果音频正在播放返回True，否则返回False
        """
        if sound_name in self.playing_channels:
            channel = self.playing_channels[sound_name]
            # 检查通道是否仍在播放
            if channel.get_busy():
                return True
            # 如果通道不再播放，从记录中移除
            else:
                del self.playing_channels[sound_name]
        return False
    
    def stop_sound(self, sound_name):
        """
        停止指定名称的音频播放
        参数:
            sound_name: 音频名称（不包含扩展名）
        """
        if sound_name in self.playing_channels:
            channel = self.playing_channels[sound_name]
            channel.stop()
            del self.playing_channels[sound_name]
    
    def play_click_sound(self):
        """
        播放点击音效，专门用于开始游戏页面、设置和创建世界等场景的按钮点击
        """
        return self.play_sound("点击")
    
    def update_settings(self):
        """
        更新设置（当设置_数据库.json可能被其他程序修改时调用）
        更新后会根据新的设置停止相应的音频
        """
        # 保存之前的设置状态
        old_sound_enabled = self.sound_enabled
        old_music_enabled = self.music_enabled
        
        # 加载新设置
        self.load_settings()
        
        # 如果音效开关被关闭，则停止所有非音乐类音频
        if not self.sound_enabled and old_sound_enabled:
            for sound_name, channel in list(self.playing_channels.items()):
                if sound_name != "神秘音乐":
                    channel.stop()
                    if sound_name in self.playing_channels:
                        del self.playing_channels[sound_name]
        
        # 如果音乐开关被关闭，则停止神秘音乐
        if not self.music_enabled and old_music_enabled:
            if "神秘音乐" in self.playing_channels:
                self.playing_channels["神秘音乐"].stop()
                del self.playing_channels["神秘音乐"]
    
    def stop_all_sounds(self):
        """停止所有正在播放的音频"""
        pygame.mixer.stop()
    
    def get_loaded_sounds(self):
        """获取所有已加载的音频名称列表"""
        return list(self.sounds.keys())
    
    def is_sound_loaded(self, sound_name):
        """检查指定名称的音频是否已加载"""
        return sound_name in self.sounds

# 创建全局音频管理器实例
audio_manager = AudioManager()

# 测试加载函数（可选）
def test_audio_loading():
    print("=== 音频管理器测试 ===")
    audio_manager.load_all_audio()
    print(f"已加载的音频列表: {audio_manager.get_loaded_sounds()}")
    
    # 测试点击音效播放功能
    print("\n=== 测试点击音效播放 ===")
    print(f"当前音效开关状态: {'开启' if audio_manager.sound_enabled else '关闭'}")
    print(f"当前音量设置: {int(audio_manager.volume * 100)}%")
    
    # 尝试播放点击音效
    success = audio_manager.play_click_sound()
    if success:
        print("点击音效播放成功")
    else:
        print("点击音效播放失败（可能是因为音效开关关闭或音频未加载）")
    
    # 提示如何使用
    print("\n=== 使用说明 ===")
    print("1. 在游戏中导入音频管理器: from 音频输出 import audio_manager")
    print("2. 加载音频: audio_manager.load_all_audio()")
    print("3. 播放点击音效: audio_manager.play_click_sound()")
    print("4. 在设置更改后更新设置: audio_manager.update_settings()")

# 如果直接运行此文件，则进行测试
if __name__ == "__main__":
    test_audio_loading()