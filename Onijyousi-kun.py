# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 13:01:57 2021

@author: keisu
"""

import tkinter as tk#Python標準のライブラリのためエラーを想定しなくてよい
from tkinter import messagebox as mbox
import tkinter.ttk as ttk
import sys
import subprocess
import threading as th
import json
import os

#エラークラス作成
class Errors():
    def library_import_error(self,):
        pass
    def file_import_error(self,file_name):
        self.file_name = file_name
        mbox.showerror('エラー','ファイルが見つかりません。\n見つからないファイル：'+self.file_name)
        sys.exit()
        
error_instance = Errors()#エラー実体化

#Python標準以外のライブラリ、ファイル読み込み
try:
    import Config
except:
    error_instance.file_import_error('Config.py')
#try:
test_file = open(Config.MONITOR_APP_SAVEDATA_PATH,'r',encoding='utf-8')
test_json_data = json.load(test_file)
test_file.close()
#except:
 #   error_instance.file_import_error('MonitorAppSaveData.json')


class JsonReadAndWrite():
    def __init__(self,):
        pass
    def MonitorAppSaveDataRead(self,):
        #jsonfile読み込み
        Config.monitor_app_save_data_file = open(Config.MONITOR_APP_SAVEDATA_PATH,'r',encoding='utf-8')
        #リストにする
        Config.monitor_app_save_data = None
        Config.monitor_app_save_data = json.load(Config.monitor_app_save_data_file)
        #nthでn番目という意味になる
        Config.nth = 0
        #表示
        for i in Config.monitor_app_save_data:
            for j in i:
                #設定取得
                #リストのまま残しておく
                Config.monitor_app_list_settings_save_data = Config.monitor_app_save_data[j]['settings'].copy()
                Config.monitor_app_settings_save_data = str(Config.monitor_app_save_data[j]['settings'].copy())#文字列に変える
                Config.monitor_app_settings_save_data = Config.monitor_app_settings_save_data.strip('[')
                Config.monitor_app_settings_save_data = Config.monitor_app_settings_save_data.strip(']')
                Config.monitor_app_settings_save_data = Config.monitor_app_settings_save_data.strip()
                #パス名取得
                Config.monitor_app_path_save_data = str(Config.monitor_app_save_data[i]['path'])
                Config.monitor_app_path_save_data = Config.monitor_app_path_save_data.strip('[')
                Config.monitor_app_path_save_data = Config.monitor_app_path_save_data.strip(']')
                Config.monitor_app_path_save_data = Config.monitor_app_path_save_data.strip()
                yield (Config.monitor_app_path_save_data,Config.monitor_app_settings_save_data)
                Config.nth += 1
        Config.monitor_app_save_data_file.close()
    def MonitorAppDataWrite(self,write_data):
        self.write_data = write_data
        #jsonfile書き込み
        Config.monitor_app_save_data_file = open(Config.MONITOR_APP_SAVEDATA_PATH,'w',encoding='utf-8')
        #書き込み
        json.dump(self.write_data,Config.monitor_app_save_data_file,ensure_ascii=False,indent=4)
        #閉じる
        Config.monitor_app_save_data_file.close()


#json読み込み＆書き込みファイルクラス実体化
Config.json_read_and_write_instance = JsonReadAndWrite()

class MainWindow(object):
    def __init__(self,):
        #作成
        Config.main_window = tk.Tk()
        #サイズ設定
        Config.main_window.geometry(str(Config.MAIN_WINDOW_WIDTH)+'x'+str(Config.MAIN_WINDOW_HEIGHT))
        #背景
        Config.main_window.configure(bg=Config.SECOAND_COLOR)
        #タイトル
        Config.main_window.title('鬼上司くん')
        #メインウィンドウ変数
        Config.main_window_on = True
        #閉じたら
        Config.main_window.protocol('WM_DELETE_WINDOW',self.MainWindowClose)
    def MainWindowClose(self,):
        Config.main_window.destroy()#メインウィンドウ削除(他のウィンドウはToplevelのため勝手に消される)
        Config.main_window_on = False
        sys.exit()

class AddMonitorWindow(object):
    def __init__(self,):
        Config.add_monitor_window = tk.Toplevel(Config.main_window)
        Config.add_monitor_window.geometry(str(Config.ADD_MONITOR_WINDOW_WIDTH)+'x'+str(Config.ADD_MONITOR_WINDOW_HEIGHT))
        Config.add_monitor_window.title('監視対象を追加')
        Config.add_monitor_window.configure(bg=Config.SECOAND_COLOR)
        self.add_monitor_screen_instance = AddMonitorScreen()
        #add_monitor_window変数
        Config.add_monitor_window_on = True
        #
        Config.add_monitor_window.protocol('WM_DELETE_WINDOW',self.AddMonitorWindowClose)
    def AddMonitorWindowClose(self,):
        Config.add_monitor_window.destroy()
        Config.add_monitor_window_on = False
class AddMonitorScreen(AddMonitorWindow):
    def __init__(self,):
        Config.add_monitor_main_frame = tk.Frame(Config.add_monitor_window,height=250,width=300,relief='ridge',bd=5)
        Config.add_monitor_main_frame.propagate(0)
        Config.add_monitor_main_frame.pack(side='bottom')
        Config.add_monitor_window_label = tk.Label(Config.add_monitor_window,text='監視対象を追加',bg=Config.SECOAND_COLOR,fg=Config.THIRD_COLOR,font=(u'游ゴシック',25,'bold'))
        Config.add_monitor_window_label.pack()
        self.AddMonitorMainFrame()
    def AddMonitorMainFrame(self,):
        self.WhatIsAddMonitorText()
        self.WhatIsAddSettingsTextFrame()
        self.DeterminationSettingsSaveButtons()
    def WhatIsAddMonitorText(self,):
        Config.what_is_add_monitor_text = tk.Label(Config.add_monitor_main_frame,text='インターネットアドレスまたはファイルパス',font=(u'游ゴシック',10,'bold'))
        Config.what_is_add_monitor_text.place(x=0,y=0)
        #
        Config.what_is_add_monitor_text_box = tk.Entry(Config.add_monitor_main_frame,font=(u'游ゴシック',12,'bold'))
        Config.what_is_add_monitor_text_box.place(x=0,y=20,width=290,height=40)
    def WhatIsAddSettingsTextFrame(self,):
        Config.what_is_add_settings_text_frame = tk.LabelFrame(Config.add_monitor_main_frame,text='監視設定',font=(u'游ゴシック',10,'bold'),width=290,height=130,relief='solid',bd=2)
        Config.what_is_add_settings_text_frame.propagate(0)
        Config.what_is_add_settings_text_frame.place(x=0,y=60)
        #チェックボックス追加
        #監視を有効にするか
        Config.do_monitor_check_button_bool = tk.BooleanVar()
        Config.do_monitor_check_button = tk.Checkbutton(Config.what_is_add_settings_text_frame,text='監視を有効にするか',font=(u'游ゴシック',9,'bold'),variable=Config.do_monitor_check_button_bool)
        Config.do_monitor_check_button.place(x=5,y=0)
        #該当するソフト、IPにアクセスしたら注意するか
        Config.do_mindful_check_button_bool = tk.BooleanVar()
        Config.do_mindful_check_button = tk.Checkbutton(Config.what_is_add_settings_text_frame,text='違反したら通知ボックスで警告するか',font=(u'游ゴシック',9,'bold'),variable=Config.do_mindful_check_button_bool)
        Config.do_mindful_check_button.place(x=5,y=25)
        #30秒以内に閉じなかったら注意
        Config.do_mindful_within_30_seconds_check_button_bool = tk.BooleanVar()
        Config.do_mindful_within_30_seconds_check_button = tk.Checkbutton(Config.what_is_add_settings_text_frame,text='違反して30秒以内に終了しないと警告するか',font=(u'游ゴシック',9,'bold'),variable=Config.do_mindful_within_30_seconds_check_button_bool)
        Config.do_mindful_within_30_seconds_check_button.place(x=5,y=50)
        #強制終了
        Config.do_forced_end_app_check_button_bool = tk.BooleanVar()
        Config.do_forced_end_app_check_button = tk.Checkbutton(Config.what_is_add_settings_text_frame,text='違反したら強制終了するか(アプリ限定)',font=(u'游ゴシック',9,'bold'),variable=Config.do_forced_end_app_check_button_bool)
        Config.do_forced_end_app_check_button.place(x=5,y=75)
    def DeterminationSettingsSaveButtons(self,):
        Config.determination_save_settings_button = tk.Button(Config.add_monitor_main_frame,text='保存',font=(u'游ゴシック',10,'bold'),fg=Config.THIRD_COLOR,bg=Config.SECOAND_COLOR,width=16,height=2,command=AddMonitor)
        Config.determination_save_settings_button.place(x=150,y=193)
        Config.do_not_determination_save_settings_button = tk.Button(Config.add_monitor_main_frame,text='保存しない',font=(u'游ゴシック',10,'bold'),fg=Config.THIRD_COLOR,bg=Config.SECOAND_COLOR,width=16,height=2,command=self.DonotDeterminationSettingsSave)
        Config.do_not_determination_save_settings_button.place(x=2,y=193)
    def DonotDeterminationSettingsSave(self,):
        if mbox.askyesno('確認','本当に保存しなくていいですか?'):
            #ウィンドウ削除
            Config.add_monitor_window.destroy()
        else:
            pass
class MainScreen(MainWindow):
    def __init__(self,):
        Config.main_window_frame = tk.Frame(Config.main_window,height=240,width=400,bd=5,relief='ridge')
        Config.main_window_frame.propagate(0)
        Config.main_window_frame.pack(side='bottom')
        Config.main_window_label = tk.Label(Config.main_window,text='鬼上司くん Ver'+str(Config.APP_VERSION),bg=Config.SECOAND_COLOR,fg=Config.THIRD_COLOR,font=(u'游ゴシック',29,'bold'))
        Config.main_window_label.pack()
    def MainFrame(self,):
        self.MainFrameTreeView()
        self.MainFrameTreeviewUpdate()
        self.MainFrameAngerLevelFrame()
        self.MainFrameIsMonitor()
    def OnMainFrameTreeView(self,event_name):
            self.edit_monitor_settings_window_instance = EditMonitorSettingsWindow()
    def MainFrameTreeView(self,):
        #ツリービューのテキストフレーム
        Config.main_tree_view_label_frame = tk.LabelFrame(Config.main_window_frame,text='監視させるもの',height=160,width=360,relief='solid',bd=2)
        Config.main_tree_view_label_frame.place(x=5,y=5)
        #ツリービュー作成
        #ツリービューの大きさ調整のためにフレーム追加
        Config.main_tree_view_frame = tk.Frame(Config.main_tree_view_label_frame,height=150,width=350,relief='flat')
        Config.main_tree_view_frame.propagate(0)
        Config.main_tree_view_frame.pack(fill='x',padx='2')
        #ツリービュー定義
        Config.main_frame_tree_view = ttk.Treeview(Config.main_tree_view_frame,height=6)
        Config.main_frame_tree_view['columns'] = (1,2)#列は何行か(これは2行)
        Config.main_frame_tree_view['show'] = 'headings'#表のデザイン
        #列の設定
        Config.main_frame_tree_view.heading(1,text='パスまたはアドレス')
        Config.main_frame_tree_view.heading(2,text='設定')
        #列の幅を設定
        Config.main_frame_tree_view.column(1,width=200)
        Config.main_frame_tree_view.column(2,width=150)
        #表を選択したときの設定
        Config.main_frame_tree_view.bind('<<TreeviewSelect>>',self.OnMainFrameTreeView)
        #貼り付け
        Config.main_frame_tree_view.grid(row=1, column=1, sticky='nsew')
        #ツリービューのスクロールバー
        #縦
        #orientは縦ならtk.VERTICAL、横ならtk.HORIZONTALを使う。command=Config.main_frame_tree_view.yviewでツリービューのY軸に紐付いたことになる
        Config.main_frame_tree_view_scroll_bar_y = tk.Scrollbar(Config.main_tree_view_frame,orient=tk.VERTICAL,command=Config.main_frame_tree_view.yview)
        Config.main_frame_tree_view.configure(yscrollcommand=Config.main_frame_tree_view_scroll_bar_y.set)
        Config.main_frame_tree_view_scroll_bar_y.grid(row=1, column=2, sticky='nsew')
    def MainFrameTreeviewUpdate(self,):
        #ツリービューをいったん消す(アップデートするときに前のデータが残らないようにするため)
        Config.main_frame_tree_view.pack_forget()
        #ツリービュー作成
        self.MainFrameTreeView()
        #
        self.read_data = Config.json_read_and_write_instance.MonitorAppSaveDataRead()
        for read_data in self.read_data:#ジェネレータオブジェクトのためfor文で回転させる
            #ツリービューに出力
            read_data = (read_data[0],read_data[1][:-3])
            Config.main_frame_tree_view.insert('','end',values=read_data,tags=Config.nth)
    def MainFrameAngerLevelFrame(self,):
        #テキストフレーム
        Config.main_frame_anger_level_text_frame = tk.LabelFrame(Config.main_window_frame,text='上司の怒りレベル',height=50,width=180,relief='solid',bd=2)
        Config.main_frame_anger_level_text_frame.propagate(0)
        Config.main_frame_anger_level_text_frame.place(x=202,y=170)
        #上司の怒りレベルは..テキスト
        Config.main_frame_anger_label_text = tk.Label(Config.main_frame_anger_level_text_frame,text='上司の怒りレベルは...')
        Config.main_frame_anger_label_text.place(x=5,y=3)
    def MainFrameIsMonitor(self,):
        #テキストフレーム
        Config.main_frame_is_monitor_label_text_frame = tk.LabelFrame(Config.main_window_frame,text='監視されるか',height=50,width=180,relief='solid',bd=2)
        Config.main_frame_is_monitor_label_text_frame.propagate(0)
        Config.main_frame_is_monitor_label_text_frame.place(x=5,y=170)
        #ラジオボタン
        Config.main_frame_is_monitor_radio_buttom_int_var = tk.IntVar()
        Config.main_frame_is_monitor_radio_buttom_y = tk.Radiobutton(Config.main_frame_is_monitor_label_text_frame,variable=Config.main_frame_is_monitor_radio_buttom_int_var,value=0,text='される')
        Config.main_frame_is_monitor_radio_buttom_n = tk.Radiobutton(Config.main_frame_is_monitor_label_text_frame,variable=Config.main_frame_is_monitor_radio_buttom_int_var,value=1,text='されない')
        Config.main_frame_is_monitor_radio_buttom_y.place(x=20,y=3)
        Config.main_frame_is_monitor_radio_buttom_n.place(x=100,y=3)
    def MainScreenMenuber(self,):
        #メニューバー作成
        Config.main_screen_menu_ber = tk.Menu(Config.main_window)
        #メニューバーとウィンドウを紐づけ
        Config.main_window.config(menu=Config.main_screen_menu_ber)
        #メニュー追加(監視対象を追加)
        Config.main_screen_menu_ber.add_command(label='監視対象を追加する',command=self.MainScreenAddMonitorMenuCommand)
    def MainScreenAddMonitorMenuCommand(self,):
        self.add_monitor_window_instance = AddMonitorWindow()
        
        
class EditMonitorSettingsWindow(object):
    def __init__(self,):
        #ウィンドウ作成
        Config.edit_monitor_settings_window = tk.Toplevel(Config.main_window)
        #ウィンドウのタイトル変更
        Config.edit_monitor_settings_window.title('監視対象を編集')
        #ウィンドウの大きさ
        Config.edit_monitor_settings_window.geometry(str(Config.EDIT_MONITOR_SETTINGS_WINDOW_WEIGHT)+'x'+str(Config.EDIT_MONITOR_SETTINGS_WINDOW_HEIGHT))
        #背景
        Config.edit_monitor_settings_window.configure(bg=Config.SECOAND_COLOR)
        #画面描画へ
        self.edit_monitor_settings_screen_instance = EditMonitorSettingsScreen()
        #edit_monitor_settings_window変数
        Config.edit_monitor_settings_window_on = True
        #
        Config.edit_monitor_settings_window.protocol('WM_DELETE_WINDOW',self.EditMonitorSettingsWindowClose)
    def EditMonitorSettingsWindowClose(self,):
        Config.edit_monitor_settings_window.destroy()
        Config.edit_monitor_settings_window_on = False
class EditMonitorSettingsScreen(EditMonitorSettingsWindow):
    def __init__(self,):
        #テキスト表示
        Config.edit_monitor_settings_text = tk.Label(Config.edit_monitor_settings_window,text='監視対象を編集',bg=Config.SECOAND_COLOR,fg=Config.THIRD_COLOR,font=(u'游ゴシック',25,'bold'))
        Config.edit_monitor_settings_text.pack()
        #フレーム表示
        Config.edit_monitor_settings_main_frame = tk.Frame(Config.edit_monitor_settings_window,height=250,width=300,relief='ridge',bd=5)
        Config.edit_monitor_settings_main_frame.propagate(0)
        Config.edit_monitor_settings_main_frame.pack()
        #データ取得(選択しているところの)
        self.monitor_app_save_data = Config.main_frame_tree_view.selection()[0]
        Config.monitor_app_save_deta_tags = Config.main_frame_tree_view.item(self.monitor_app_save_data)['tags']
        self.monitor_app_save_data = Config.main_frame_tree_view.item(self.monitor_app_save_data)['values']
        #settings項目をリスト化
        Config.monitor_app_settings_save_data = str(self.monitor_app_save_data[1]).split(',')
        #数値化
        Config.monitor_app_settings_save_data = list(map(int,Config.monitor_app_settings_save_data))
        #メインフレーム描画
        self.EditMonitorSettingsMainFrame()
    def EditMonitorSettingsMainFrame(self,):
        self.WhatIsNewMonitorAppText()
        self.WhatIsNewMonitorSettingsTextFrame()
        self.DeterminationNewSettingsSaveButtons()
    def WhatIsNewMonitorAppText(self,):
        Config.what_is_new_monitor_app_text = tk.Label(Config.edit_monitor_settings_main_frame,text='新たなインターネットアドレスまたはファイルパス',font=(u'游ゴシック',9,'bold'))
        Config.what_is_new_monitor_app_text.place(x=0,y=0)
        Config.what_is_new_monitor_app_text_box = tk.Entry(Config.edit_monitor_settings_main_frame,font=(u'游ゴシック',12,'bold'))
        #テキストボックスに入れる
        Config.what_is_new_monitor_app_text_box.insert(tk.END,self.monitor_app_save_data[0])
        #
        Config.what_is_new_monitor_app_text_box.place(x=0,y=20,width=290,height=40)
    def WhatIsNewMonitorSettingsTextFrame(self,):
        Config.what_is_new_monitor_settings_text_frame = tk.LabelFrame(Config.edit_monitor_settings_main_frame,text='新しい監視設定',font=(u'游ゴシック',10,'bold'),width=290,height=130,relief='solid',bd=2)
        Config.what_is_new_monitor_settings_text_frame.propagate(0)
        Config.what_is_new_monitor_settings_text_frame.place(x=0,y=60)
        #
        #チェックボックス追加
        #監視を有効にするか
        Config.new_settings_do_monitor_check_button_bool = tk.BooleanVar()
        Config.new_settings_do_monitor_check_button = tk.Checkbutton(Config.what_is_new_monitor_settings_text_frame,text='監視を有効にするか',font=(u'游ゴシック',9,'bold'),variable=Config.new_settings_do_monitor_check_button_bool)
        Config.new_settings_do_monitor_check_button.place(x=5,y=0)
        #該当するソフト、IPにアクセスしたら注意するか
        Config.new_settings_do_mindful_check_button_bool = tk.BooleanVar()
        Config.new_settings_do_mindful_check_button = tk.Checkbutton(Config.what_is_new_monitor_settings_text_frame,text='違反したら通知ボックスで警告するか',font=(u'游ゴシック',9,'bold'),variable=Config.new_settings_do_mindful_check_button_bool)
        Config.new_settings_do_mindful_check_button.place(x=5,y=25)
        #30秒以内に閉じなかったら注意
        Config.new_settings_do_mindful_within_30_seconds_check_button_bool = tk.BooleanVar()
        Config.new_settings_do_mindful_within_30_seconds_check_button = tk.Checkbutton(Config.what_is_new_monitor_settings_text_frame,text='違反して30秒以内に終了しないと警告するか',font=(u'游ゴシック',9,'bold'),variable=Config.new_settings_do_mindful_within_30_seconds_check_button_bool)
        Config.new_settings_do_mindful_within_30_seconds_check_button.place(x=5,y=50)
        #強制終了
        Config.new_settings_do_forced_end_app_check_button_bool = tk.BooleanVar()
        Config.new_settings_do_forced_end_app_check_button = tk.Checkbutton(Config.what_is_new_monitor_settings_text_frame,text='違反したら強制終了するか(アプリ限定)',font=(u'游ゴシック',9,'bold'),variable=Config.new_settings_do_forced_end_app_check_button_bool)
        Config.new_settings_do_forced_end_app_check_button.place(x=5,y=75)
        #チェックボックスをオンにする
        for settings in Config.monitor_app_settings_save_data:
            if settings == 0:
                Config.new_settings_do_monitor_check_button_bool.set(True)
            elif settings == 1:
                Config.new_settings_do_mindful_check_button_bool.set(True)
            elif settings == 2:
                Config.new_settings_do_mindful_within_30_seconds_check_button_bool.set(True)
            elif settings == 3:
                Config.new_settings_do_forced_end_app_check_button_bool.set(True)
    def DeterminationNewSettingsSaveButtons(self,):
        Config.determination_save_new_settings_button = tk.Button(Config.edit_monitor_settings_main_frame,text='保存',font=(u'游ゴシック',10,'bold'),fg=Config.THIRD_COLOR,bg=Config.SECOAND_COLOR,width=16,height=2,command=EditMonitor)
        Config.determination_save_new_settings_button.place(x=150,y=193)
        Config.do_not_save_new_settings_button = tk.Button(Config.edit_monitor_settings_main_frame,text='削除する',font=(u'游ゴシック',10,'bold'),fg=Config.THIRD_COLOR,bg=Config.SECOAND_COLOR,width=16,height=2,command=self.DeleteSettings)
        Config.do_not_save_new_settings_button.place(x=2,y=193)
    def DeleteSettings(self,):
        Config.monitor_app_save_deta_tags = str(Config.monitor_app_save_deta_tags)
        Config.monitor_app_save_deta_tags = Config.monitor_app_save_deta_tags.replace('[','')
        Config.monitor_app_save_deta_tags = Config.monitor_app_save_deta_tags.replace(']','')
        Config.monitor_app_save_deta_tags = int(Config.monitor_app_save_deta_tags)
        l = 0#lは辞書の変数名をなずける時に使う
        self.settings_delate = False
        for read_data in Config.json_read_and_write_instance.MonitorAppSaveDataRead():
            if l == 0:
                Config.tamp_monitor_app_save_data = {}
            if l == Config.monitor_app_save_deta_tags:
                l += 2#消したのは保存しないから2個飛ばしにする。
                self.settings_delate = True
            else:
                if self.settings_delate == True:
                    Config.tamp_monitor_app_save_data[str(l-2)] = {'path':Config.monitor_app_path_save_data,'settings':Config.monitor_app_list_settings_save_data}
                else:
                    Config.tamp_monitor_app_save_data[str(l)] = {'path':Config.monitor_app_path_save_data,'settings':Config.monitor_app_list_settings_save_data}
                l += 1
        #書き込み
        Config.json_read_and_write_instance.MonitorAppDataWrite(Config.tamp_monitor_app_save_data)
        #ツリービュー更新
        Config.main_screen_instance.MainFrameTreeviewUpdate()
        #ウィンドウを閉じる
        Config.edit_monitor_settings_window.destroy()
        #ダイアログ
        mbox.showinfo('削除完了','削除しました')
        
        
class EditMonitor():
    def __init__(self,):
        self.is_not_ping_normal = False
        #監視対象追加処理の進み具合の変数
        Config.edit_monitor_process_progress_progress_progress = 0
        Config.edit_monitor_text_box_data = Config.what_is_new_monitor_app_text_box.get()
        Config.new_settings_do_monitor_check_button_data = Config.new_settings_do_monitor_check_button_bool.get()
        Config.new_settings_do_mindful_check_button_data = Config.new_settings_do_mindful_check_button_bool.get()
        Config.new_settings_do_mindful_within_30_seconds_check_button_data = Config.new_settings_do_mindful_within_30_seconds_check_button_bool.get()
        Config.new_settings_do_forced_end_app_check_button_data = Config.new_settings_do_forced_end_app_check_button_bool.get()
        self.ProgressVar()
        self.IsEditMonitorTextBoxDataNormal()
    def IsEditMonitorTextBoxDataNormal(self,):
        #進捗バー30
        Config.edit_monitor_progress_ber.configure(value=30)
        Config.edit_monitor_progress_ber.update()
        #もし何も入力されていなかったら
        if not bool(Config.edit_monitor_text_box_data):
            #進捗バー削除
            Config.edit_monitor_progress_ber_window.destroy()
            mbox.showwarning('警告','パスまたはIPを入力してください。')
            return 0;
        #ファイルパスかIPか
        self.is_file_path = False
        if not os.path.isfile(Config.edit_monitor_text_box_data):
            self.is_ping_normal_threading = th.Thread(target=self.IsPingNormal)
            self.is_ping_normal_threading.setDaemon(True)
            self.is_ping_normal_threading.start()
        else:
            #進捗バー60
            Config.edit_monitor_progress_ber.configure(value=60)
            Config.edit_monitor_progress_ber.update()
            self.is_file_path = True
            self.IsCheckBoxNormal()
            self.save_edit_monitor_threading = th.Thread(target=self.SaveEditMonitor)
            self.save_edit_monitor_threading.setDaemon(True)
            self.save_edit_monitor_threading.start()
            #進捗バー80
            Config.edit_monitor_progress_ber.configure(value=80)
            Config.edit_monitor_progress_ber.update()
        #進捗バー50
        Config.edit_monitor_progress_ber.configure(value=50)
        Config.edit_monitor_progress_ber.update()
    
    def IsPingNormal(self,):
        self.is_int_only = False
        #IPアドレスか
        for i in Config.edit_monitor_text_box_data:
            if i != '0' or i != '1' or i != '2' or i != '3' or i != '4' or i != '5' or i != '6' or i != '7' or i != '8' or i != '9' or i != '.':
                self.is_int_only = False
                break
            else:
                self.is_int_only = True
        #pingは正常か
        #ipとwwwは分ける必要がない(pingの時にwwwだと自動的にIPに変換してくれる)
        self.is_ping_normal = subprocess.run(['ping',Config.edit_monitor_text_box_data,'-n','1'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #進捗バー60
        Config.edit_monitor_progress_ber.configure(value=60)
        Config.edit_monitor_progress_ber.update()
        #ping実行結果をcp932コードに直す
        self.is_ping_normal = self.is_ping_normal.stdout.decode('cp932')
        #進捗バー70
        Config.edit_monitor_progress_ber.configure(value=70)
        Config.edit_monitor_progress_ber.update()
        #もしpingが正常でなかったら
        if '要求がタイムアウトしました。' in self.is_ping_normal or 'ping: 転送に失敗しました。一般エラーです。' in self.is_ping_normal or 'が見つかりませんでした。ホスト名を確認してもう一度実行してください。' in self.is_ping_normal:
            self.is_not_ping_normal = True
            #進捗バー100
            Config.edit_monitor_progress_ber.configure(value=100)
            Config.edit_monitor_progress_ber.update()
            #進捗バー削除
            Config.edit_monitor_progress_ber_window.destroy()
            mbox.showwarning('警告','パスまたはIPが正しくありません。')
            return 0;
        else:
            #進捗バー80
            Config.edit_monitor_progress_ber.configure(value=80)
            Config.edit_monitor_progress_ber.update()
            #チェックボックスは正常か
            self.is_check_box_normal_threading = th.Thread(target=self.IsCheckBoxNormal)
            if self.check_box_is_normal == False:
                return 0;
            #進捗バー90
            Config.edit_monitor_progress_ber.configure(value=90)
            Config.edit_monitor_progress_ber.update()
            #セーブする
            self.save_edit_monitor_threading = th.Thread(target=self.SaveEditMonitor)
            self.save_edit_monitor_threading.setDaemon(True)
            self.save_edit_monitor_threading.start()
    def IsCheckBoxNormal(self,):
        self.check_box_is_normal = False
        #
        for check_box_data in [Config.new_settings_do_monitor_check_button_data,Config.new_settings_do_mindful_check_button_data,Config.new_settings_do_forced_end_app_check_button_data,Config.new_settings_do_mindful_within_30_seconds_check_button_data]:
            if check_box_data:
                self.check_box_is_normal = True
            else:
                pass
        if self.check_box_is_normal == False:
            #進捗バー削除
            Config.edit_monitor_progress_ber_window.destroy()
            mbox.showwarning('警告','チェックボックスにチェックを入れてください。')
            return 0;
        else:
            pass
    def ProgressVar(self,):
        #ウィンドウ
        Config.edit_monitor_progress_ber_window = tk.Toplevel(Config.edit_monitor_settings_window)
        Config.edit_monitor_progress_ber_window.title('保存の進捗状況')
        Config.edit_monitor_progress_ber_window.geometry('100x50')
        #テキスト
        Config.edit_monitor_progress_ber_window_text = tk.Label(Config.edit_monitor_progress_ber_window,text='保存の進捗状況')
        Config.edit_monitor_progress_ber_window_text.pack()
        #進捗バー作成
        Config.edit_monitor_progress_ber = ttk.Progressbar(Config.edit_monitor_progress_ber_window)
        Config.edit_monitor_progress_ber.pack()
        #value=0は進捗バーの値,max=最高値,determinateは右端に一直線に行く。indeterminateは左右を行ったり来たりする。
        Config.edit_monitor_progress_ber.configure(value=Config.edit_monitor_process_progress,mode='determinate',maximum=100)
    def SaveEditMonitor(self,):
        #インスタンス初期化
        Config.json_read_and_write_instance = JsonReadAndWrite()
        #読み込み＆編集
        Config.json_read_and_write_instance.MonitorAppSaveDataRead()
        #チェックボックスをリスト化
        i = 0
        Config.monitor_app_settings_save_data = []
        for check_box_data in [Config.new_settings_do_monitor_check_button_data,Config.new_settings_do_mindful_check_button_data,Config.new_settings_do_mindful_within_30_seconds_check_button_data,Config.new_settings_do_forced_end_app_check_button_data]:
            if check_box_data:
                Config.monitor_app_settings_save_data.append(i)
            else:
                pass
            i += 1
        #テキストボックスに入っているのがファイルパスなら4,ではないなら5を入れる
        if self.is_file_path == True:
            Config.monitor_app_settings_save_data.append(4)
        else:
            Config.monitor_app_settings_save_data.append(5)
        #タグはリストなので[]をはぐ
        Config.monitor_app_save_deta_tags = str(Config.monitor_app_save_deta_tags)
        Config.monitor_app_save_deta_tags = Config.monitor_app_save_deta_tags.strip('[')
        Config.monitor_app_save_deta_tags = Config.monitor_app_save_deta_tags.strip(']')
        #
        Config.monitor_app_save_data[Config.monitor_app_save_deta_tags] = {'path':Config.edit_monitor_text_box_data,'settings':Config.monitor_app_settings_save_data}
        #保存
        Config.json_read_and_write_instance.MonitorAppDataWrite(Config.monitor_app_save_data)
        #ツリービュー更新
        Config.main_screen_instance.MainFrameTreeviewUpdate()
        #ウィンドウ削除
        Config.edit_monitor_settings_window.destroy()
        #ダイアログ
        mbox.showinfo('編集完了','編集しました')


class AddMonitor():
    def __init__(self,):
        self.is_not_ping_normal = False
        #監視対象追加処理の進み具合の変数
        Config.add_monitor_process_progress = 0
        Config.add_monitor_text_box_data = Config.what_is_add_monitor_text_box.get()
        Config.do_monitor_check_button_data = Config.do_monitor_check_button_bool.get()
        Config.do_mindful_check_button_data = Config.do_mindful_check_button_bool.get()
        Config.do_mindful_within_30_seconds_check_button_data = Config.do_mindful_within_30_seconds_check_button_bool.get()
        Config.do_forced_end_app_check_button_data = Config.do_forced_end_app_check_button_bool.get()
        self.ProgressVar()
        self.IsAddMonitorTextBoxDataNormal()
    def IsAddMonitorTextBoxDataNormal(self,):
        #進捗バー30
        Config.add_monitor_progress_ber.configure(value=30)
        Config.add_monitor_progress_ber.update()
        #もし何も入力されていなかったら
        if not bool(Config.add_monitor_text_box_data):
            #進捗バー削除
            Config.add_monitor_progress_ber_window.destroy()
            mbox.showwarning('警告','パスまたはIPを入力してください。')
            return 0;
        #ファイルパスかIPか
        Config.is_file_path = False
        if not os.path.isfile(Config.add_monitor_text_box_data):
            self.is_ping_normal_threading = th.Thread(target=self.IsPingNormal)
            self.is_ping_normal_threading.setDaemon(True)
            self.is_ping_normal_threading.start()
        else:
            #進捗バー60
            Config.add_monitor_progress_ber.configure(value=60)
            Config.add_monitor_progress_ber.update()
            Config.is_file_path = True
            self.IsCheckBoxNormal()
            #進捗バー80
            Config.add_monitor_progress_ber.configure(value=80)
            Config.add_monitor_progress_ber.update()
            self.SaveAddMonitor()
        #進捗バー50
        Config.add_monitor_progress_ber.configure(value=50)
        Config.add_monitor_progress_ber.update()
    
    def IsPingNormal(self,):
        self.is_int_only = False
        #IPアドレスか
        for i in Config.add_monitor_text_box_data:
            if i != '0' or i != '1' or i != '2' or i != '3' or i != '4' or i != '5' or i != '6' or i != '7' or i != '8' or i != '9' or i != '.':
                self.is_int_only = False
                break
            else:
                self.is_int_only = True
        #pingは正常か
        #ipとwwwは分ける必要がない(pingの時にwwwだと自動的にIPに変換してくれる)
        self.is_ping_normal = subprocess.run(['ping',Config.add_monitor_text_box_data,'-n','1'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #進捗バー60
        Config.add_monitor_progress_ber.configure(value=60)
        Config.add_monitor_progress_ber.update()
        #ping実行結果をcp932コードに直す
        self.is_ping_normal = self.is_ping_normal.stdout.decode('cp932')
        #進捗バー70
        Config.add_monitor_progress_ber.configure(value=70)
        Config.add_monitor_progress_ber.update()
        #もしpingが正常でなかったら
        if '要求がタイムアウトしました。' in self.is_ping_normal or 'ping: 転送に失敗しました。一般エラーです。' in self.is_ping_normal or 'が見つかりませんでした。ホスト名を確認してもう一度実行してください。' in self.is_ping_normal:
            self.is_not_ping_normal = True
            #進捗バー100
            Config.add_monitor_progress_ber.configure(value=100)
            Config.add_monitor_progress_ber.update()
            #進捗バー削除
            Config.add_monitor_progress_ber_window.destroy()
            mbox.showwarning('警告','パスまたはIPが正しくありません。')
            return 0;
        else:
            #進捗バー80
            Config.add_monitor_progress_ber.configure(value=80)
            Config.add_monitor_progress_ber.update()
            #チェックボックスは正常か
            self.is_check_box_normal_threading = th.Thread(target=self.IsCheckBoxNormal)
            if Config.check_box_is_normal == False:
                return 0;
            #進捗バー90
            Config.add_monitor_progress_ber.configure(value=90)
            Config.add_monitor_progress_ber.update()
            #セーブする
            self.save_add_monitor_threading = th.Thread(target=self.SaveAddMonitor)
            self.save_add_monitor_threading.setDaemon(True)
            self.save_add_monitor_threading.start()
    def IsCheckBoxNormal(self,):
        Config.check_box_is_normal = False
        #
        for check_box_data in [Config.do_monitor_check_button_data,Config.do_mindful_check_button_data,Config.do_mindful_within_30_seconds_check_button_data,Config.do_forced_end_app_check_button_data]:
            if check_box_data:
                Config.check_box_is_normal = True
            else:
                pass
        if Config.check_box_is_normal == False:
            #進捗バー削除
            Config.add_monitor_progress_ber_window.destroy()
            mbox.showwarning('警告','チェックボックスにチェックを入れてください。')
            return 0;
        else:
            pass
    def ProgressVar(self,):
        #ウィンドウ,
        Config.add_monitor_progress_ber_window = tk.Toplevel(Config.add_monitor_window)
        Config.add_monitor_progress_ber_window.title('保存の進捗状況')
        Config.add_monitor_progress_ber_window.geometry('100x50')
        #テキスト
        Config.add_monitor_progress_ber_window_text = tk.Label(Config.add_monitor_progress_ber_window,text='保存の進捗状況')
        Config.add_monitor_progress_ber_window_text.pack()
        #進捗バー作成
        Config.add_monitor_progress_ber = ttk.Progressbar(Config.add_monitor_progress_ber_window)
        Config.add_monitor_progress_ber.pack()
        #value=0は進捗バーの値,max=最高値,determinateは右端に一直線に行く。indeterminateは左右を行ったり来たりする。
        Config.add_monitor_progress_ber.configure(value=Config.add_monitor_process_progress,mode='determinate',maximum=100)
    def SaveAddMonitor(self,):
        #json読み込み
        Config.json_read_and_write_instance = JsonReadAndWrite()
        Config.json_read_and_write_instance.MonitorAppSaveDataRead()
        #データに入力されたものを加える
        #チェックボックスを数値化
        i = 0
        Config.monitor_app_settings_data = []
        for check_box_data in [Config.do_monitor_check_button_data,Config.do_mindful_check_button_data,Config.do_mindful_within_30_seconds_check_button_data,Config.do_forced_end_app_check_button_data]:
            if check_box_data:
                Config.monitor_app_settings_data.append(i)
            i += 1
        #ファイルパスかIPか
        Config.monitor_app_settings_data.append(4) if Config.is_file_path == True else Config.monitor_app_settings_data.append(5)
        #Config.monitor_app_save_data[Config.nth+1] = {'path':Config.add_monitor_text_box_data,'settings':Config.monitor_app_settings_data}
        Config.monitor_app_save_data[len(Config.monitor_app_save_data)] = {'path':Config.add_monitor_text_box_data,'settings':Config.monitor_app_settings_data}
        #書き込み
        Config.json_read_and_write_instance.MonitorAppDataWrite(Config.monitor_app_save_data)
        #進捗バー100
        Config.add_monitor_progress_ber.configure(value=100)
        Config.add_monitor_progress_ber.update()
        #ツリービュー更新
        Config.main_screen_instance.MainFrameTreeviewUpdate()
        #ウィンドウ削除
        Config.add_monitor_window.destroy()
        #通知する
        mbox.showinfo('保存完了','保存しました。')
class DoMonitor():
    def __init__(self,):
        pass
    def MonitorIP(self,):
        pass
    def MonitorFilePath(self,):
        subprocess.run(['tasklist'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
if __name__ == '__main__':
    main_window_instance = MainWindow()
    Config.main_screen_instance = MainScreen()
    Config.main_screen_instance.MainFrame()
    Config.main_screen_instance.MainScreenMenuber()
    Config.main_window.mainloop()
    