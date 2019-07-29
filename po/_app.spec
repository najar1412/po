# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['D:\\code\\po\\po'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

artwork =  [('heart.png', 'D:\\code\\po\\po\\artwork\\heart.png', 'DATA')]
artwork +=  [('loadingWheel.gif', 'D:\\code\\po\\po\\artwork\\loadingWheel.gif', 'DATA')]

uis =  [('main_res.ui', 'D:\\code\\po\\po\\main_res.ui', 'DATA')]
uis +=  [('new_client_dialog.ui', 'D:\\code\\po\\po\\new_client_dialog.ui', 'DATA')]
uis +=  [('new_job_dialog.ui', 'D:\\code\\po\\po\\new_job_dialog.ui', 'DATA')]
uis +=  [('new_project_dialog.ui', 'D:\\code\\po\\po\\new_project_dialog.ui', 'DATA')]
uis +=  [('project_checker_dialog.ui', 'D:\\code\\po\\po\\project_checker_dialog.ui', 'DATA')]
uis +=  [('settings_dialog.ui', 'D:\\code\\po\\po\\settings_dialog.ui', 'DATA')]
uis +=  [('project_upload_dialog.ui', 'D:\\code\\po\\po\\project_upload_dialog.ui', 'DATA')]
uis +=  [('wrong_folder_structure_dialog.ui', 'D:\\code\\po\\po\\wrong_folder_structure_dialog.ui', 'DATA')]
uis +=  [('aws_not_installed_dialog.ui', 'D:\\code\\po\\po\\aws_not_installed_dialog.ui', 'DATA')]
uis +=  [('first_time_run_dialog.ui', 'D:\\code\\po\\po\\first_time_run_dialog.ui', 'DATA')]

files = [('default_config.json', 'D:\\code\\po\\po\\default_config.json', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas + uis + artwork + files,
          [],
          name='app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
