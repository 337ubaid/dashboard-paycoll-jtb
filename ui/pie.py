import plotly.express as px

from services.utip_service import agg_keterangan

KET_COLOR_MAP = {
    "belum teridentifikasi": "#eeeeee",  # grey
    "proses flagging": "#0068C9",  # blue
    "over payment": "#FF2B2B",  # red
    "billing account": "#FFABAB",  # red
}

DEFAULT_COLOR = "#bdbdbd"


def plot_pie_utip(df, col_ket="KET 2", value_type="saldo"):

    data = agg_keterangan(df, col_ket, value_type)
    colors = [KET_COLOR_MAP.get(v.lower(), DEFAULT_COLOR) for v in data[col_ket]]

    fig = px.pie(data, names=col_ket, values="total", hole=0.4)

    fig.update_traces(
        marker=dict(colors=colors),
        texttemplate="%{label}<br>%{value}",
        # textinfo="label+value",
    )

    return fig
