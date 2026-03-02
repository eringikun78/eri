import streamlit as st
import pandas as pd

# ページ設定（スマホで見やすく）
st.set_page_config(page_title="異常診断システム", layout="centered")

@st.cache_data
def load_data(file_path):
    # 全シート読み込み
    all_sheets = pd.read_excel(file_path, sheet_name=None)
    chart = {}
    for df in all_sheets.values():
        df = df.fillna('')
        # 列固定
        df.columns = ['ID', 'Question', 'Options', 'NextID'] + list(df.columns[4:])
        for _, row in df.iterrows():
            node_id = str(row['ID']).strip()
            if not node_id or node_id.lower() == 'id': continue
            
            if row['Options']:
                chart[node_id] = {
                    "q": str(row['Question']),
                    "btns": [{"t": t.strip(), "n": n.strip()} 
                             for t, n in zip(str(row['Options']).split(','), str(row['NextID']).split(','))]
                }
            else:
                chart[node_id] = {"res": str(row['Question'])}
    return chart

def main():
    st.title("🛠 異常診断ツール")
    
    # データの読み込み（hokusho.xlsxが同じフォルダにある前提）
    chart = load_data("hokusho.xlsx")
    
    # セッション状態（現在のID）の管理
    if 'current_id' not in st.session_state:
        st.session_state.current_id = "start"

    node = chart.get(st.session_state.current_id)

    # 診断結果
    if "res" in node:
        st.success(f"📌 診断結果:\n\n{node['res']}")
        if st.button("最初からやり直す", use_container_width=True):
            st.session_state.current_id = "start"
            st.rerun()
    # 質問
    else:
        st.subheader(node["q"])
        for btn in node["btns"]:
            if st.button(btn["t"], key=f"{st.session_state.current_id}_{btn['t']}", use_container_width=True):
                st.session_state.current_id = btn["n"]
                st.rerun()

if __name__ == "__main__":
    main()