import os
import json
import shutil
import urllib.parse
import difflib
import platform
from datetime import datetime
from collections import defaultdict

# --- İŞLETİM SİSTEMİNE GÖRE YOL AYARLARI ---
def get_vscode_history_path():
    system = platform.system()
    if system == "Windows":
        # Windows: %APPDATA%\Code\User\History
        return os.path.join(os.environ.get('APPDATA', ''), 'Code', 'User', 'History')
    elif system == "Darwin":
        # macOS: ~/Library/Application Support/Code/User/History
        return os.path.expanduser('~/Library/Application Support/Code/User/History')
    else:
        # Linux: ~/.config/Code/User/History
        return os.path.expanduser('~/.config/Code/User/History')

HISTORY_PATH = get_vscode_history_path()
CWD = os.getcwd()

# --- RENKLER VE SİMGELER (Windows CMD uyumluluğu için kontrol ekledik) ---
if platform.system() == "Windows":
    os.system('color') # Windows terminalinde renkleri aktif et

C = {"reset": "\033[0m", "bold": "\033[1m", "cyan": "\033[96m", "green": "\033[92m", 
     "yellow": "\033[93m", "red": "\033[91m", "magenta": "\033[95m", "blue": "\033[94m"}

LOGO = f"""
{C['magenta']}    🔧  KODUĞUM KODUNU KURTAR (UNIVERSAL V4) 🔧
{C['cyan']}    ==========================================
           ____  ____  ____
          ||K ||||K ||||K ||
          ||__||||__||||__||
          |/__\||/__\||/__\|
{C['reset']}    ==========================================
    🏠 Sistem: {C['green']}{platform.system()}{C['reset']}
    📂 Proje:  {C['bold']}{C['yellow']}{CWD}{C['reset']}
"""

def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def decode_path(uri):
    # URI formatını (file:///...) yerel dosya yoluna çevirir
    path = uri.replace("file://", "")
    # Windows'ta file:///C:/ formatını temizle
    if platform.system() == "Windows":
        if path.startswith("/"): path = path[1:]
        path = path.replace("/", "\\")
    else:
        if path.startswith("//"): path = path[2:]
        if path.startswith("/"): pass # Linux yolları / ile başlar
    
    decoded = urllib.parse.unquote(path)
    # Windows'ta bazen drive letter sonrası : karakteri %3A kalabilir
    if ":" in decoded and "|" in decoded: # Bazı garip formatlar için
         decoded = decoded.replace("|", ":")
    return decoded

def get_history_data(only_current=False):
    if not os.path.exists(HISTORY_PATH):
        print(f"{C['red']}HATA: VS Code History yolu bulunamadı!{C['reset']}")
        print(f"Aranan yol: {HISTORY_PATH}")
        return {}, []

    history = {}
    all_ts = []
    for folder in os.listdir(HISTORY_PATH):
        f_path = os.path.join(HISTORY_PATH, folder)
        if not os.path.isdir(f_path): continue
        j_path = os.path.join(f_path, "entries.json")
        if not os.path.exists(j_path): continue
        try:
            with open(j_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                o_path = decode_path(data['resource'])
                
                # Filtreleme
                if only_current and CWD.lower() not in o_path.lower(): continue
                
                history[o_path] = {
                    'folder': f_path, 
                    'entries': sorted(data['entries'], key=lambda x: x['timestamp'])
                }
                for e in data['entries']: all_ts.append(e['timestamp'])
        except: continue
    return history, sorted(list(set(all_ts)), reverse=True)

def diff_ozeti(eski_dosya, yeni_dosya):
    try:
        with open(eski_dosya, 'r', encoding='utf-8', errors='ignore') as f1, \
             open(yeni_dosya, 'r', encoding='utf-8', errors='ignore') as f2:
            diff = list(difflib.ndiff(f1.readlines(), f2.readlines()))
            plus = sum(1 for l in diff if l.startswith('+ '))
            minus = sum(1 for l in diff if l.startswith('- '))
            return f"{C['green']}+{plus}{C['reset']} / {C['red']}-{minus}{C['reset']} satır"
    except: return "---"

def content_search():
    clear_screen()
    print(LOGO)
    query = input(f"{C['yellow']}🔍 Kod içinde ne arıyoruz? (Örn: 'class Motor'): {C['reset']}")
    print(f"{C['blue']}Tüm geçmiş taranıyor, bu biraz sürebilir...{C['reset']}")
    
    results = []
    history, _ = get_history_data(only_current=False)
    
    for path, info in history.items():
        for entry in reversed(info['entries']):
            v_path = os.path.join(info['folder'], entry['id'])
            if os.path.exists(v_path):
                try:
                    with open(v_path, 'r', encoding='utf-8', errors='ignore') as f:
                        if query in f.read():
                            dt = datetime.fromtimestamp(entry['timestamp']/1000.0)
                            results.append({
                                'path': path, 'time': dt, 'src': v_path, 'id': entry['id']
                            })
                            if len(results) >= 20: break
                except: continue
        if len(results) >= 20: break

    if not results:
        print(f"{C['red']}Eşleşen kod parçası bulunamadı.{C['reset']}")
        input("\nDevam etmek için Enter..."); return

    print(f"\n{C['green']}Eşleşen Versiyonlar (Son 20):{C['reset']}")
    for i, res in enumerate(results):
        print(f"[{i:<2}] {res['time'].strftime('%Y-%m-%d %H:%M:%S')} | {os.path.basename(res['path'])}")
    
    choice = input(f"\n{C['cyan']}Kurtarmak istediğiniz ID (veya q): {C['reset']}")
    if choice.isdigit():
        target = results[int(choice)]
        bak_path = target['path'] + ".bak"
        shutil.copy2(target['path'], bak_path)
        shutil.copy2(target['src'], target['path'])
        print(f"{C['green']}✔ Dosya canlandırıldı: {target['path']}{C['reset']}")
        input()

def global_timeline_mode():
    history, all_ts = get_history_data(only_current=True)
    save_points = []
    if all_ts:
        curr = [all_ts[0]]
        for i in range(1, len(all_ts)):
            if abs(all_ts[i] - curr[-1]) < 10000: curr.append(all_ts[i])
            else: save_points.append(max(curr)); curr = [all_ts[i]]
        save_points.append(max(curr))

    page, per_page = 0, 15
    while True:
        clear_screen()
        print(LOGO)
        print(f"{C['magenta']}--- GLOBAL TIMELINE (Sadece Bu Proje) ---{C['reset']}\n")
        start, end = page * per_page, (page + 1) * per_page
        for i, ts in enumerate(save_points[start:end]):
            dt_obj = datetime.fromtimestamp(ts/1000.0)
            dt = dt_obj.strftime('%H:%M:%S')
            dt_full = dt_obj.strftime('%Y-%m-%d')
            count = sum(1 for f in history.values() if any(e['timestamp'] <= ts for e in f['entries']))
            print(f"[{start+i:<2}] {dt_full} {C['bold']}{dt}{C['reset']} | {count} dosya yedekli")
        
        print(f"\n{C['blue']}[n] Sonraki | [p] Önceki | [ID] Geri Yükle | [q] Ana Menü{C['reset']}")
        cmd = input("\nSeçim: ").lower()
        if cmd == 'q': break
        if cmd == 'n' and end < len(save_points): page += 1
        if cmd == 'p' and page > 0: page -= 1
        if cmd.isdigit():
            idx = int(cmd)
            if idx < 0 or idx >= len(save_points): continue
            ts = save_points[idx]
            confirm = input(f"{C['red']}TÜM PROJE bu ana döndürülsün mü? (y/n): {C['reset']}")
            if confirm.lower() == 'y':
                for path, info in history.items():
                    best = next((e for e in reversed(info['entries']) if e['timestamp'] <= ts), None)
                    if best and os.path.exists(path):
                        shutil.copy2(os.path.join(info['folder'], best['id']), path)
                print(f"{C['green']}✔ Tüm proje ışınlandı!{C['reset']}"); input(); break

def file_search_mode():
    history, _ = get_history_data(only_current=False)
    clear_screen()
    print(LOGO)
    query = input(f"{C['yellow']}Aranacak dosya adı: {C['reset']}").lower()
    matches = [p for p in history.keys() if query in p.lower()]
    
    if not matches: print("Bulunamadı."); input(); return
    
    for i, p in enumerate(matches[:15]): print(f"[{i}] {p}")
    f_choice = input(f"\n{C['cyan']}Dosya ID: {C['reset']}")
    if f_choice.isdigit():
        idx = int(f_choice)
        if idx < 0 or idx >= len(matches): return
        path = matches[idx]
        entries = sorted(history[path]['entries'], key=lambda x: x['timestamp'], reverse=True)
        clear_screen()
        print(f"{C['magenta']}--- {os.path.basename(path)} Geçmişi ---{C['reset']}\n")
        for i, e in enumerate(entries[:20]):
            dt = datetime.fromtimestamp(e['timestamp']/1000.0).strftime('%Y-%m-%d %H:%M:%S')
            diff = diff_ozeti(path, os.path.join(history[path]['folder'], e['id']))
            print(f"[{i}] {dt} | {diff}")
        
        v_choice = input(f"\n{C['cyan']}Versiyon ID: {C['reset']}")
        if v_choice.isdigit():
            v_idx = int(v_choice)
            if v_idx < 0 or v_idx >= len(entries): return
            src = os.path.join(history[path]['folder'], entries[v_idx]['id'])
            shutil.copy2(src, path)
            print(f"{C['green']}✔ Dosya kurtarıldı!{C['reset']}"); input()

def main():
    if not os.path.exists(HISTORY_PATH):
        clear_screen()
        print(LOGO)
        print(f"{C['red']}HATA: VS Code yerel geçmiş yolu bulunamadı!{C['reset']}")
        print(f"Lütfen VS Code'un yüklü ve Local History özelliğinin aktif olduğundan emin olun.")
        return

    while True:
        clear_screen()
        print(LOGO)
        print(f"1) {C['bold']}Global Timeline{C['reset']} (Tüm projeyi aynı ana döndür)")
        print(f"2) {C['bold']}Dosya Ara{C['reset']} (İsme göre geçmişi gör)")
        print(f"3) {C['bold']}Kod İçinde Ara{C['reset']} (Hatırladığın bir cümleden bul)")
        print(f"q) {C['red']}Çıkış{C['reset']}")
        
        choice = input(f"\n{C['cyan']}Yapılacak işlem: {C['reset']}")
        if choice == '1': global_timeline_mode()
        elif choice == '2': file_search_mode()
        elif choice == '3': content_search()
        elif choice == 'q': break

if __name__ == "__main__":
    main()