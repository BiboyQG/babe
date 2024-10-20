from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGroupBox
from PyQt5.QtCore import QTimer, QDateTime
from WindPy import w
import pandas as pd
import threading
import datetime
import sys

# 产品列表和DataFrame初始化
products = ["AU2406.SHF", "XAUCNY.IDC"]
columns = (
    ["Time"]
    + [f"{prod}_Bid" for prod in products]
    + [f"{prod}_Ask" for prod in products]
    + [f"{prod}_Latest" for prod in products]
    + ["Bid_Difference", "Ask_Difference", "Latest_Difference"]
)
df = pd.DataFrame(columns=columns)
current_data = {prod: {"Bid": None, "Ask": None, "Latest": None} for prod in products}
current_week = datetime.datetime.now().isocalendar()[1]


def find_week_start_end(date):
    """给定日期，返回所在周的开始和结束日期（周一和周日）。"""
    start = date - datetime.timedelta(days=date.weekday())
    end = start + datetime.timedelta(days=6)
    return start, end


def check_trading_hours(now):
    """检查当前时间是否在指定的交易时段内。"""
    if now.weekday() == 5 or now.weekday() == 6:
        return False
    morning_session = now.time() >= datetime.time(9, 0) and now.time() <= datetime.time(
        11, 30
    )
    afternoon_session = now.time() >= datetime.time(
        13, 30
    ) and now.time() <= datetime.time(15, 0)
    night_session = now.time() >= datetime.time(21, 0) or now.time() <= datetime.time(
        2, 30
    )
    return morning_session or afternoon_session or night_session


def update_dataframe():
    global df
    now = datetime.datetime.now()
    if check_trading_hours(now):
        new_data = pd.DataFrame({"Time": [now]})
        for product in products:
            new_data[f"{product}_Bid"] = [current_data[product]["Bid"]]
            new_data[f"{product}_Ask"] = [current_data[product]["Ask"]]
            new_data[f"{product}_Latest"] = [current_data[product]["Latest"]]

        new_data["Bid_Difference"] = (
            new_data["AU2406.SHF_Bid"] - new_data["XAUCNY.IDC_Bid"]
        )
        new_data["Ask_Difference"] = (
            new_data["AU2406.SHF_Ask"] - new_data["XAUCNY.IDC_Ask"]
        )
        new_data["Latest_Difference"] = (
            new_data["AU2406.SHF_Latest"] - new_data["XAUCNY.IDC_Latest"]
        )

        df = pd.concat([df, new_data], ignore_index=True)


def save_weekly_data():
    global df
    if df.empty:
        print("没有数据可保存。")
        return
    # 获取DataFrame中的最小和最大日期
    min_date = df["Time"].min().strftime("%Y-%m-%d")
    max_date = df["Time"].max().strftime("%Y-%m-%d")
    filename = f"market_data_{min_date}_to_{max_date}.csv"
    df.to_csv(filename, index=False)
    print(f"数据已保存到 {filename}")
    df = pd.DataFrame(columns=columns)


def schedule_data_updates():
    """定时调度数据更新任务。"""
    global current_week
    threading.Timer(1.0, schedule_data_updates).start()
    update_dataframe()

    new_week = datetime.datetime.now().isocalendar()[1]
    if new_week != current_week:
        save_weekly_data()
        current_week = new_week


def myCallback(indata):
    """处理从WindPy接收的实时数据。"""
    if indata.ErrorCode != 0:
        print("Error code:", indata.ErrorCode)
        return
    for i, code in enumerate(indata.Codes):
        latest_price = indata.Data[indata.Fields.index("RT_LATEST")][i]
        bid_price = indata.Data[indata.Fields.index("RT_BID1")][i]
        ask_price = indata.Data[indata.Fields.index("RT_ASK1")][i]
        current_data[code]["Latest"] = latest_price
        current_data[code]["Bid"] = bid_price
        current_data[code]["Ask"] = ask_price


def run_wsq():
    """启动WindPy实时数据订阅。"""
    if w.start().ErrorCode != 0:
        print("WindPy start failed")
        return
    w.wsq(
        "AU2406.SHF,XAUCNY.IDC", "rt_latest,rt_bid1,rt_ask1", func=myCallback
    )


class MarketDataDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("实时市场数据展示")
        self.setGeometry(300, 300, 800, 600)
        layout = QVBoxLayout(self)
        self.current_time_label = QLabel("")
        layout.addWidget(self.current_time_label)
        self.bid_group = QGroupBox("Bid")
        self.ask_group = QGroupBox("Ask")
        self.latest_group = QGroupBox("Latest Price")
        self.bid_layout = QVBoxLayout()
        self.ask_layout = QVBoxLayout()
        self.latest_layout = QVBoxLayout()
        self.bid_group.setLayout(self.bid_layout)
        self.ask_group.setLayout(self.ask_layout)
        self.latest_group.setLayout(self.latest_layout)
        self.bid_group.setStyleSheet(
            "QGroupBox { background-color: white; border: 1px solid gray; border-radius: 5px; margin-top: 10px;}"
        )
        self.ask_group.setStyleSheet(
            "QGroupBox { background-color: white; border: 1px solid gray; border-radius: 5px; margin-top: 10px;}"
        )
        self.latest_group.setStyleSheet(
            "QGroupBox { background-color: white; border: 1px solid gray; border-radius: 5px; margin-top: 10px;}"
        )
        layout.addWidget(self.bid_group)
        layout.addWidget(self.ask_group)
        layout.addWidget(self.latest_group)
        self.labels_bid = {}
        self.labels_ask = {}
        self.labels_latest = {}
        for product in products:
            label_bid = QLabel(f"{product}: 等待数据...")
            label_ask = QLabel(f"{product}: 等待数据...")
            label_latest = QLabel(f"{product}: 等待数据...")
            self.labels_bid[product] = label_bid
            self.labels_ask[product] = label_ask
            self.labels_latest[product] = label_latest
            self.bid_layout.addWidget(label_bid)
            self.ask_layout.addWidget(label_ask)
            self.latest_layout.addWidget(label_latest)

        self.labels_bid["Difference"] = QLabel("AU2406.SHF - XAUCNY.IDC: 等待数据...")
        self.labels_ask["Difference"] = QLabel("AU2406.SHF - XAUCNY.IDC: 等待数据...")
        self.labels_latest["Difference"] = QLabel(
            "AU2406.SHF - XAUCNY.IDC: 等待数据..."
        )
        self.bid_layout.addWidget(self.labels_bid["Difference"])
        self.ask_layout.addWidget(self.labels_ask["Difference"])
        self.latest_layout.addWidget(self.labels_latest["Difference"])

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(1000)

    def update_labels(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.current_time_label.setText(f"当前时间: {current_time}")
        if not df.empty:
            latest_data = df.iloc[-1]
            for product in products:
                bid_price = latest_data.get(f"{product}_Bid")
                ask_price = latest_data.get(f"{product}_Ask")
                latest_price = latest_data.get(f"{product}_Latest")
                text_bid = (
                    f"{product}: {bid_price:.2f}"
                    if bid_price is not None
                    else f"{product}: 等待数据..."
                )
                text_ask = (
                    f"{product}: {ask_price:.2f}"
                    if ask_price is not None
                    else f"{product}: 等待数据..."
                )
                text_latest = (
                    f"{product}: {latest_price:.2f}"
                    if latest_price is not None
                    else f"{product}: 等待数据..."
                )

                self.labels_bid[product].setText(text_bid)
                self.labels_ask[product].setText(text_ask)
                self.labels_latest[product].setText(text_latest)
            
            bid_diff = latest_data.get("Bid_Difference")
            ask_diff = latest_data.get("Ask_Difference")
            latest_diff = latest_data.get("Latest_Difference")

            self.labels_bid["Difference"].setText(
                f"AU2406.SHF - XAUCNY.IDC: {bid_diff:.2f}"
                if bid_diff is not None
                else "AU2406.SHF - XAUCNY.IDC: 等待数据..."
            )
            self.labels_ask["Difference"].setText(
                f"AU2406.SHF - XAUCNY.IDC: {ask_diff:.2f}"
                if ask_diff is not None
                else "AU2406.SHF - XAUCNY.IDC: 等待数据..."
            )
            self.labels_latest["Difference"].setText(
                f"AU2406.SHF - XAUCNY.IDC: {latest_diff:.2f}"
                if latest_diff is not None
                else "AU2406.SHF - XAUCNY.IDC: 等待数据..."
            )

    def closeEvent(self, event):
        """重写closeEvent以在程序关闭时保存数据。"""
        if df.empty:
            print("没有数据可保存。")
            event.accept()  # 确认关闭
            return

        # 获取DataFrame中的最小和最大日期
        min_date = df["Time"].min().strftime("%Y-%m-%d")
        max_date = df["Time"].max().strftime("%Y-%m-%d")
        filename = f"final_data_{min_date}_to_{max_date}.csv"
        df.to_csv(filename, index=False)
        print(f"数据已保存到 {filename}")
        event.accept()  # 确认关闭


if __name__ == "__main__":
    app = QApplication(sys.argv)
    md_display = MarketDataDisplay()
    md_display.show()
    schedule_data_updates()
    run_wsq()
    sys.exit(app.exec_())
