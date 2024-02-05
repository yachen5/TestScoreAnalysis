import plotly_express as px
import streamlit as st


def by_class_summary(df, s_c):
    st.markdown('### 各班成績分布與排名')
    col1, col2 = st.columns(2)
    # st.dataframe(df)
    df_box = df.groupby(['班級', '學號'], as_index=False).agg({'Question': 'count'})
    df_box = df_box.merge(s_c, on=['學號'], how='left')
    df_desc = df_box.groupby(['班級'])['Percentage'].describe()
    col1.dataframe(df_desc)
    # Find the top category by mean and median (50%)
    top_categories_mean = df_desc['mean'].nlargest(3).index
    top_categories_median = df_desc['50%'].nlargest(3).index
    # Generate the text summary for mean
    text_summary_mean = f"平均前三名的班級: {', '.join(top_categories_mean)} 各自平均為 {', '.join([f'{mean:.2f}' for mean in df_desc.loc[top_categories_mean, 'mean']])}"
    # Generate the text summary for median (50%)
    text_summary_median = f"中位數前三名的班級: {', '.join(top_categories_median)} 各自中位數為 {', '.join([f'{median:.2f}' for median in df_desc.loc[top_categories_median, '50%']])}"
    # Print the text summaries
    col2.write("\n歸納總結:\n")
    col2.write(text_summary_mean)
    col2.write(text_summary_median)
    fig = px.box(df_box, x='班級', y='Percentage', points='all', color='班級')
    st.markdown('### 箱型圖')
    fig.update_traces(boxmean=True)
    return fig
    # st.plotly_chart(fig)
