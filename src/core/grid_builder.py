import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode


class InteractiveTable:
    """
    Ag-Grid 高级表格构建器
    支持：分页、排序、筛选、多选、可编辑
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.builder = GridOptionsBuilder.from_dataframe(df)

    def build_options(self, selection_mode="multiple", editable=False):
        """配置表格选项"""
        # 1. 基础配置：允许分页、侧边栏工具栏
        self.builder.configure_pagination(
            enabled=True, paginationAutoPageSize=False, paginationPageSize=10
        )
        self.builder.configure_side_bar()  # 启用右侧筛选栏

        # 2. 默认列配置：所有列都可排序、可拖拽调整宽窄
        self.builder.configure_default_column(
            groupable=True,
            value=True,
            enableRowGroup=True,
            aggFunc="sum",
            editable=editable,  # 是否允许直接修改单元格
        )

        # 3. 选择模式：多选(multiple) 或 单选(single)
        self.builder.configure_selection(selection_mode, use_checkbox=True)

        return self.builder.build()

    def show(self, key_prefix="grid"):
        """在 Streamlit 中渲染表格"""
        options = self.build_options(editable=True)

        response = AgGrid(
            self.df,
            gridOptions=options,
            enable_enterprise_modules=False,  # 使用免费版
            update_mode=GridUpdateMode.MODEL_CHANGED,  # 数据一改，马上同步回 Python
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            fit_columns_on_grid_load=True,  # 自动调整列宽
            height=400,
            theme="streamlit",  # 风格适配
            key=key_prefix,
        )
        return response
