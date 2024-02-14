import streamlit as st

from LocalApps.SharedLayout import layout_class

st.markdown("""
            持續開發中，敬請期待!""")


def main():
    # with open(pkl_file_path, 'rb') as pkl_file:
    #     # Load the data from the Pickle file
    #     a_dic = pickle.load(pkl_file)
    if 'class_groups' in st.session_state:
        layout_class()

    else:
        st.warning("請回到前一步驟，上傳Excel文件")


if __name__ == '__main__':
    main()
    # st.sidebar.write('版本 V1.1222_2023')
