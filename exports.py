

import pandas as pd
from io import BytesIO

def export_orders_excel(results):
    output = BytesIO()

    orders_df = pd.DataFrame(results.order_log)

    # تنظيف الداتا
    orders_df = orders_df.replace("—", "")
    orders_df = orders_df.fillna("")

    # تحويل لأرقام
    numeric_cols = ["Arrival", "Prep Wait", "Prep Time", "Driver Wait", "Travel Time", "Total Time"]
    for col in numeric_cols:
        orders_df[col] = pd.to_numeric(orders_df[col], errors='coerce')

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        # ───────── Orders Sheet ─────────
        orders_df.to_excel(writer, sheet_name="Orders", index=False)
        ws = writer.sheets["Orders"]

        # ✔ Delay (H)
        for i in range(2, len(orders_df) + 2):
            ws[f"H{i}"] = f'=IF(G{i}>45,"Yes","No")'

        # ✔ Speed Category (J)
        ws["J1"] = "Speed Category"
        for i in range(2, len(orders_df) + 2):
            ws[f"J{i}"] = f'=IF(G{i}="","",IF(G{i}<=30,"Fast",IF(G{i}<=45,"Normal",IF(G{i}<=60,"Late","Very Late"))))'

        # ───────── Summary Sheet ─────────
        summary_data = [
            ["Metric", "Value"],
            ["Total Orders", "=COUNTA(Orders!A2:A1000)"],
            ["Delayed Orders", '=COUNTIF(Orders!H2:H1000,"Yes")'],
            ["Delay Rate (%)", '=IFERROR(COUNTIF(Orders!H2:H1000,"Yes")/COUNTA(Orders!A2:A1000)*100,0)'],
            ["Avg Delivery Time", '=IFERROR(AVERAGEIF(Orders!G2:G1000,">0"),0)'],
            ["Max Delivery Time", '=IFERROR(MAX(Orders!G2:G1000),0)'],
            ["Min Delivery Time", '=IFERROR(MIN(Orders!G2:G1000),0)'],
        ]

        summary_df = pd.DataFrame(summary_data[1:], columns=summary_data[0])
        summary_df.to_excel(writer, sheet_name="Summary", index=False)

        # ───────── Queue Log ─────────
        if results.queue_log:
            queue_df = pd.DataFrame(
                results.queue_log,
                columns=["Time", "Restaurant Queue", "Driver Queue"]
            )
            queue_df.to_excel(writer, sheet_name="Queue Log", index=False)

    output.seek(0)
    return output