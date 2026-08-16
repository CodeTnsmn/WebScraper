import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "src"))
sys.path.insert(0, str(_ROOT))

import streamlit as st  # noqa: E402

from dashboard.data import build_chart_dataframe, latest_snapshot  # noqa: E402
from webscraper import config, store  # noqa: E402


def _db_path() -> str:
    return os.environ.get("WEBSCRAPER_DB", config.DEFAULT_DB_PATH)


def render() -> None:
    st.set_page_config(page_title="WebScraper — Fiyat Takibi", layout="wide")
    st.title("Fiyat Trendi ve Rakip Karşılaştırma")

    conn = store.connect(_db_path())
    targets = store.list_targets(conn)

    if not targets:
        st.info("Henüz takip edilen hedef yok. `python -m webscraper.cli add-target` ile hedef ekleyin.")
        return

    options = {f"{t.name} ({t.default_currency})": t.id for t in targets}
    labels = list(options.keys())
    selected_labels = st.multiselect("Karşılaştırılacak hedef(ler)", labels, default=labels[:1])

    if not selected_labels:
        st.info("Grafiği görmek için en az bir hedef seçin.")
        return

    histories = {label: store.get_history(conn, options[label]) for label in selected_labels}

    if all(len(history) == 0 for history in histories.values()):
        st.info("Seçilen hedef(ler) için henüz toplanmış veri yok.")
        return

    chart_df = build_chart_dataframe(histories)
    if not chart_df.empty:
        st.line_chart(chart_df)
    else:
        st.info("Seçilen hedef(ler) için sayısallaştırılmış fiyat verisi yok.")

    if len(selected_labels) == 1:
        latest = latest_snapshot(histories[selected_labels[0]])
        if latest is not None:
            col1, col2 = st.columns(2)
            price_text = f"{latest.price} {latest.currency}" if latest.price is not None else latest.raw_price
            stock_text = "Bilinmiyor" if latest.in_stock is None else ("Stokta" if latest.in_stock else "Tükendi")
            col1.metric("Güncel Fiyat", price_text)
            col2.metric("Stok Durumu", stock_text)


render()
