"""
シンプルな音声テストスクリプト
"""

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from speech.recognizer import SpeechRecognizer

def simple_test():
    """シンプルな音声認識テスト"""
    print("=== Azure Speech Service テスト ===")
    print("話しかけてください...")
    
    try:
        recognizer = SpeechRecognizer()
        success, text = recognizer.recognize_once()
        
        if success:
            print(f"認識結果: {text}")
        else:
            print(f"エラー: {text}")
            
    except Exception as e:
        print(f"例外エラー: {str(e)}")

if __name__ == "__main__":
    simple_test()