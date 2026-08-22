import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# --------------------------------------------------
# LINE CHART
# --------------------------------------------------

def line_chart(
    df: pd.DataFrame,
    x_col: str,
    value_col: str,
    title: str,
    aggfunc: str = "sum",
    freq: str = None
):
    # Date-based line chart
    if freq is not None:
        data = (
            df.groupby(
                pd.Grouper(
                    key=x_col,
                    freq=freq
                )
            )[value_col]
            .agg(aggfunc)
            .reset_index()
        )

    # Normal categorical/numeric line chart
    else:
        data = (
            df.groupby(x_col)[value_col]
            .agg(aggfunc)
            .reset_index()
        )

    fig = px.line(
        data,
        x=x_col,
        y=value_col,
        title=title,
        markers=True
    )

    return fig

# --------------------------------------------------
# MULTI LINE CHART
# --------------------------------------------------

def multi_line_chart(
    df: pd.DataFrame,
    date_col: str,
    value_cols: list,
    title: str,
    freq: str = "M"
):
    data = (
        df.groupby(
            pd.Grouper(key=date_col, freq=freq)
        )[value_cols]
        .sum()
        .reset_index()
    )

    fig = px.line(
        data,
        x=date_col,
        y=value_cols,
        title=title,
        markers=True
    )

    return fig


# --------------------------------------------------
# UNIVERSAL BAR CHART
# --------------------------------------------------

def bar_chart(
    df: pd.DataFrame,
    group_col: str,
    value_col: str | None,
    title: str,
    top_n: int = None,
    aggfunc: str = "sum"
):

    # Count rows when no value column is supplied
    if value_col is None:

        data = (
            df.groupby(group_col)
            .size()
            .reset_index(name="value")
        )

        sort_col = "value"


    # Sum
    elif aggfunc == "sum":

        data = (
            df.groupby(group_col)[value_col]
            .sum()
            .reset_index(name=value_col)
        )

        sort_col = value_col


    # Mean / Average / Rate
    elif aggfunc == "mean":

        data = (
            df.groupby(group_col)[value_col]
            .mean()
            .reset_index(name="value")
        )

        sort_col = "value"


    # Count
    elif aggfunc == "count":

        data = (
            df.groupby(group_col)[value_col]
            .count()
            .reset_index(name="value")
        )

        sort_col = "value"


    # Unique count
    elif aggfunc == "nunique":

        data = (
            df.groupby(group_col)[value_col]
            .nunique()
            .reset_index(name="value")
        )

        sort_col = "value"


    else:

        raise ValueError(
            "aggfunc must be: sum, mean, count, or nunique"
        )


    # Sort
    data = data.sort_values(
        sort_col,
        ascending=False
    )


    # Top N
    if top_n:
        data = data.head(top_n)


    # Create chart
    fig = px.bar(
        data,
        x=group_col,
        y=sort_col,
        title=title,
        text=sort_col
    )

    return fig


# --------------------------------------------------
# HORIZONTAL BAR CHART
# --------------------------------------------------

def horizontal_bar_chart(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    title: str,
    top_n: int = None,
    aggfunc: str = "sum"
):

    if aggfunc == "sum":

        data = (
            df.groupby(group_col)[value_col]
            .sum()
            .reset_index(name=value_col)
        )

    elif aggfunc == "mean":

        data = (
            df.groupby(group_col)[value_col]
            .mean()
            .reset_index(name=value_col)
        )

    elif aggfunc == "count":

        data = (
            df.groupby(group_col)[value_col]
            .count()
            .reset_index(name=value_col)
        )

    elif aggfunc == "nunique":

        data = (
            df.groupby(group_col)[value_col]
            .nunique()
            .reset_index(name=value_col)
        )

    else:

        raise ValueError(
            "aggfunc must be: sum, mean, count, or nunique"
        )


    data = data.sort_values(
        value_col,
        ascending=True
    )


    if top_n:
        data = data.tail(top_n)


    fig = px.bar(
        data,
        y=group_col,
        x=value_col,
        title=title,
        orientation="h"
    )

    return fig


# --------------------------------------------------
# SCATTER CHART
# --------------------------------------------------

def scatter_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: str | None,
    title: str
):

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title
    )

    return fig


# --------------------------------------------------
# HISTOGRAM
# --------------------------------------------------

def histogram(
    df: pd.DataFrame,
    column: str,
    title: str,
    nbins: int = 30
):

    fig = px.histogram(
        df,
        x=column,
        nbins=nbins,
        title=title
    )

    return fig


# --------------------------------------------------
# PIE CHART
# --------------------------------------------------

def pie_chart(
    df: pd.DataFrame,
    values_col: str,
    names_col: str,
    title: str
):

    data = (
        df.groupby(names_col)[values_col]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        data,
        values=values_col,
        names=names_col,
        title=title
    )

    return fig


# --------------------------------------------------
# BOX PLOT
# --------------------------------------------------

def box_plot(
    df: pd.DataFrame,
    y_col: str,
    x_col: str | None,
    title: str
):

    fig = px.box(
        df,
        y=y_col,
        x=x_col,
        title=title
    )

    return fig


# --------------------------------------------------
# HEATMAP
# --------------------------------------------------

def heatmap(
    data: pd.DataFrame,
    title: str
):

    fig = go.Figure(
        data=go.Heatmap(
            z=data.values,
            x=data.columns,
            y=data.index
        )
    )

    fig.update_layout(
        title=title
    )

    return fig


# --------------------------------------------------
# WATERFALL CHART
# --------------------------------------------------

def waterfall_chart(
    df: pd.DataFrame,
    category_col: str,
    value_col: str,
    title: str
):

    data = (
        df.groupby(category_col)[value_col]
        .sum()
        .reset_index()
    )
 
    fig = go.Figure(
        go.Waterfall(
            x=data[category_col],
            y=data[value_col],
            textposition="outside",
            text=data[value_col]
        )
    )

    fig.update_layout(
        title=title
    )

    return fig